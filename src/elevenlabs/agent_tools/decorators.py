from __future__ import annotations

import functools
import inspect
import re
import types
import typing

import typing_extensions
from .schema import Schema
from .tool import ClientTool, Tool

_UNION_TYPES: typing.Tuple[typing.Any, ...] = tuple(
    t for t in (typing.Union, getattr(types, "UnionType", None)) if t is not None
)
_MISSING: typing.Any = object()


def _forms(name: str) -> typing.Tuple[typing.Any, ...]:
    """`typing` and `typing_extensions` can hold different objects for the same special form (on Python 3.8 and
    3.9 `typing_extensions.Literal` is not `typing.Literal`), so match against both."""
    return tuple({id(f): f for f in (getattr(typing, name, None), getattr(typing_extensions, name)) if f}.values())


_LITERAL = _forms("Literal")
_ANNOTATED = _forms("Annotated")
_REQUIRED = _forms("Required")
_NOT_REQUIRED = _forms("NotRequired")


class Param:
    """Schema details for one param of a `@client_tool` function, given with `Annotated[T, Param(...)]`.

    The param's value comes from the LLM (`description`, which overrides the docstring), a dynamic variable
    (`from_variable`) or a `constant`. For anything else, edit the builder on `fn.tool`.
    """

    def __init__(
        self,
        description: typing.Optional[str] = None,
        *,
        from_variable: typing.Optional[str] = None,
        constant: typing.Any = _MISSING,
    ) -> None:
        self.description = description
        self.from_variable = from_variable
        self.constant = constant

    def __repr__(self) -> str:
        fields = {"description": self.description, "from_variable": self.from_variable}
        if self.constant is not _MISSING:
            fields["constant"] = self.constant
        shown = ", ".join(f"{k}={v!r}" for k, v in fields.items() if v is not None)
        return f"Param({shown})"


class ClientToolFunction:
    """A function decorated with `@client_tool`.

    Calling it calls the function. `tool` is its `ClientTool` builder, for `build()`, `to_json_string()` or any
    setting a signature can't express. `handler` is what `ClientTools.register()` runs when the agent calls it.
    """

    __name__: str
    __qualname__: str

    def __init__(self, fn: typing.Callable[..., typing.Any], tool: ClientTool) -> None:
        functools.update_wrapper(self, fn)
        self.fn = fn
        self.tool = tool
        self.is_async = inspect.iscoroutinefunction(fn)
        params = inspect.signature(fn).parameters.values()
        self._takes_kwargs = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params)
        self._names = frozenset(p.name for p in params if p.kind is not inspect.Parameter.VAR_KEYWORD)

    @property
    def name(self) -> str:
        """The tool's name: the function's name unless `@client_tool(name=...)` set another."""
        return self.tool.name

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self.fn(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<client tool {self.name!r}>"

    @property
    def handler(self) -> typing.Callable[[typing.Dict[str, typing.Any]], typing.Any]:
        """Takes the params dict the agent sends and calls the function with them as keyword arguments.

        Keys the function doesn't declare, such as `tool_call_id`, are dropped unless it takes `**kwargs`.
        """

        def kwargs_from(params: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
            if self._takes_kwargs:
                return dict(params)
            return {k: v for k, v in params.items() if k in self._names}

        if self.is_async:

            async def run_async(params: typing.Dict[str, typing.Any]) -> typing.Any:
                return await self.fn(**kwargs_from(params))

            return run_async

        def run(params: typing.Dict[str, typing.Any]) -> typing.Any:
            return self.fn(**kwargs_from(params))

        return run


@typing.overload
def client_tool(fn: typing.Callable[..., typing.Any], /) -> ClientToolFunction: ...


@typing.overload
def client_tool(
    *, name: typing.Optional[str] = None, description: typing.Optional[str] = None, **options: typing.Any
) -> typing.Callable[[typing.Callable[..., typing.Any]], ClientToolFunction]: ...


def client_tool(
    fn: typing.Optional[typing.Callable[..., typing.Any]] = None,
    /,
    *,
    name: typing.Optional[str] = None,
    description: typing.Optional[str] = None,
    **options: typing.Any,
) -> typing.Any:
    """Turns a function into a client tool. The function's signature becomes the tool's params.

    Use it bare (`@client_tool`) or with arguments (`@client_tool(name=..., expects_response=True)`). `name`
    defaults to the function's name and `description` to its docstring's first paragraph. Other keyword arguments
    go to `ClientTool.options()`.

    Each param needs a type hint: `str`, `int`, `float`, `bool`, `Literal["a", "b"]` (string choices),
    `List[T]`, a `TypedDict`, or `Optional[T]` of one of those. A param with a default or an `Optional` type is
    optional. Descriptions come from the docstring's `Args:` section (or `:param name:` lines), or from
    `Annotated[T, Param("...")]`, which also sets other value sources.

    The tool is checked when it's defined and raises `ToolValidationError` listing every problem, the same as
    `build()`.
    """

    def wrap(f: typing.Callable[..., typing.Any]) -> ClientToolFunction:
        summary, arg_docs = _parse_docstring(f.__doc__)
        tool_name = name or f.__name__
        tool_description = description or summary
        if not tool_description:
            raise TypeError(f"@client_tool {tool_name}: give the function a docstring or pass description=")
        tool = Tool.client(tool_name, tool_description)
        hints = typing_extensions.get_type_hints(f, include_extras=True)
        for p in inspect.signature(f).parameters.values():
            if p.kind is inspect.Parameter.VAR_KEYWORD:
                continue
            if p.kind is inspect.Parameter.VAR_POSITIONAL or p.kind is inspect.Parameter.POSITIONAL_ONLY:
                raise TypeError(f"@client_tool {tool_name}: param '{p.name}' must be passable by keyword")
            if p.name not in hints:
                raise TypeError(f"@client_tool {tool_name}: param '{p.name}' needs a type hint")
            try:
                schema, optional = _schema_for(hints[p.name], arg_docs.get(p.name))
            except TypeError as e:
                raise TypeError(f"@client_tool {tool_name}: param '{p.name}': {e}") from None
            if optional or p.default is not inspect.Parameter.empty:
                schema = schema.optional()
            tool.param(p.name, schema)
        if options:
            tool.options(**options)
        tool.to_json()  # raises ToolValidationError now rather than at build()
        return ClientToolFunction(f, tool)

    return wrap(fn) if fn is not None else wrap


def _schema_for(hint: typing.Any, description: typing.Optional[str]) -> typing.Tuple[Schema, bool]:
    """Maps a type hint to a schema. Returns the schema and whether the type itself makes it optional."""
    optional = False
    origin = typing_extensions.get_origin(hint)
    if origin in _REQUIRED + _NOT_REQUIRED:
        # TypedDict markers. Read them here: __required_keys__ is wrong under `from __future__ import annotations`.
        optional = origin in _NOT_REQUIRED
        (hint,) = typing_extensions.get_args(hint)
        origin = typing_extensions.get_origin(hint)

    param: typing.Optional[Param] = None
    if origin in _ANNOTATED:
        hint, *extras = typing_extensions.get_args(hint)
        param = next((e for e in extras if isinstance(e, Param)), None)
        origin = typing_extensions.get_origin(hint)

    if origin in _UNION_TYPES:
        args = typing_extensions.get_args(hint)
        members = [a for a in args if a is not type(None)]
        if len(members) != 1:
            raise TypeError(f"only Optional[T] unions are supported, got {hint!r}")
        optional = optional or len(members) < len(args)
        # The member gets the docstring text only when no outer Param applies, so an inner Param keeps its own.
        inner = _schema_for(members[0], description if param is None else None)[0]
        return (inner if param is None else _with_param(inner, param, description)), optional

    schema: Schema
    if origin in _LITERAL:
        values = typing_extensions.get_args(hint)
        if not all(isinstance(v, str) for v in values):
            raise TypeError(f"Literal choices must be strings, got {hint!r}")
        schema = Schema.string().choices(list(values))
    elif hint is str:
        schema = Schema.string()
    elif hint is bool:
        schema = Schema.bool()
    elif hint is int:
        schema = Schema.integer()
    elif hint is float:
        schema = Schema.number()
    elif origin is list or hint is list:
        item_args = typing_extensions.get_args(hint)
        if len(item_args) != 1:
            raise TypeError("lists need an item type, such as List[str]")
        schema = Schema.array(_schema_for(item_args[0], None)[0])
    elif typing_extensions.is_typeddict(hint):
        total = getattr(hint, "__total__", True)
        _, field_docs = _parse_docstring(hint.__doc__)
        obj = Schema.object()
        for key, field_hint in typing_extensions.get_type_hints(hint, include_extras=True).items():
            field, type_optional = _schema_for(field_hint, field_docs.get(key))
            marker = typing_extensions.get_origin(field_hint)
            if marker in _REQUIRED:
                field_optional = False
            elif marker in _NOT_REQUIRED:
                field_optional = True
            else:
                field_optional = type_optional or not total
            obj = obj.property(key, field.optional() if field_optional else field)
        schema = obj
    else:
        raise TypeError(f"unsupported type {hint!r}")
    return _with_param(schema, param, description), optional


def _with_param(schema: Schema, param: typing.Optional[Param], description: typing.Optional[str]) -> Schema:
    fixed = param is not None and (param.from_variable is not None or param.constant is not _MISSING)
    # A description makes the LLM fill the value, so a docstring line can't apply to a variable or constant param.
    text = (param.description if param else None) or (None if fixed else description)
    if text:
        schema = schema.describe(text)
    if param is not None and param.from_variable:
        schema = schema.from_variable(param.from_variable)
    if param is not None and param.constant is not _MISSING:
        schema = schema.constant(param.constant)
    return schema


def _parse_docstring(doc: typing.Optional[str]) -> typing.Tuple[str, typing.Dict[str, str]]:
    """Returns the first paragraph and the param descriptions from a Google-style `Args:` section or
    reStructuredText `:param name:` lines."""
    text = inspect.cleandoc(doc or "")
    summary = " ".join(text.split("\n\n", 1)[0].split())
    if summary.startswith((":param", "Args:", "Attributes:")):
        summary = ""
    args: typing.Dict[str, str] = {}

    section = re.search(
        r"^(?:Args|Arguments|Parameters|Attributes):[ \t]*\n((?:[ \t]+\S.*(?:\n|$)|[ \t]*\n)+)", text, re.M
    )
    if section:
        current: typing.Optional[str] = None
        indent: typing.Optional[int] = None
        for line in section.group(1).splitlines():
            if not line.strip():
                continue
            width = len(line) - len(line.lstrip())
            hit = re.match(r"\s*\*{0,2}(\w+)(?:\s*\([^)]*\))?\s*:\s*(.*)", line)
            if hit and (indent is None or width <= indent):
                indent = width
                current = hit.group(1)
                args[current] = hit.group(2).strip()
            elif current:
                args[current] = f"{args[current]} {line.strip()}".strip()

    for hit in re.finditer(r"^:param\s+(?:\S+\s+)?(\w+):\s*((?:.*)(?:\n[ \t]+\S.*)*)", text, re.M):
        args.setdefault(hit.group(1), " ".join(hit.group(2).split()))
    return summary, args
