from __future__ import annotations

import builtins
import dataclasses
import typing

from ._wire import WireDict, canonical, deep_copy, parse

LiteralKind = typing.Literal["string", "integer", "number", "boolean"]
SchemaKind = typing.Literal["string", "integer", "number", "boolean", "object", "array"]

S = typing.TypeVar("S", bound="Schema")

_MODELED_KEYS = frozenset(
    {
        "type",
        "description",
        "dynamic_variable",
        "constant_value",
        "is_system_provided",
        "is_omitted",
        "enum",
        "allowed_values",
        "items",
        "properties",
        "required",
        "required_constraints",
    }
)


@dataclasses.dataclass(frozen=True)
class _SchemaState:
    kind: SchemaKind
    # A loaded literal's `type`, kept as is (the API also allows a list of types).
    literal_type: typing.Any = None
    description: typing.Optional[str] = None
    dynamic_variable: typing.Optional[str] = None
    has_constant: builtins.bool = False
    constant_value: typing.Any = None
    system_provided: builtins.bool = False
    omitted: builtins.bool = False
    optional: builtins.bool = False
    choices: typing.Optional[typing.Tuple[str, ...]] = None
    allowed_from: typing.Optional[str] = None
    items: typing.Optional[Schema] = None
    properties: typing.Tuple[typing.Tuple[str, Schema], ...] = ()
    # A loaded object's `required`, so its order survives edits.
    loaded_required: typing.Optional[typing.Tuple[str, ...]] = None
    any_of: typing.Tuple[typing.Tuple[str, ...], ...] = ()
    all_of: typing.Tuple[typing.Tuple[str, ...], ...] = ()
    # Loaded fields the builder doesn't model, and the API's defaults for unset ones, written back unchanged.
    extra: WireDict = dataclasses.field(default_factory=dict)


def _is_unset(key: str, value: typing.Any, kind: SchemaKind) -> builtins.bool:
    """
    Whether `value` is what the API returns for an unset field. (It also returns `null` for some, which loading
    already drops.) A literal's unset constant is `""`, so `""` can't be a constant.
    """
    if key in ("description", "dynamic_variable"):
        return value == ""
    if key == "constant_value":
        return kind not in ("object", "array") and value == ""
    if key in ("is_system_provided", "is_omitted"):
        return value is False
    if key == "required":
        return isinstance(value, list) and len(value) == 0
    if key == "properties":
        return isinstance(value, dict) and len(value) == 0
    return False


class Schema:
    """
    A tool param's JSON schema, and where its value comes from. Schemas are values: every method returns a new
    schema, so one can be reused across tools and properties.

    Examples
    --------
    Schema.object()
        .property("order_id", Schema.string().from_variable("order_id"))
        .property("reason", Schema.string().describe("Why the caller wants a refund").choices(["damaged", "late"]))
        .property("note", Schema.string().describe("Anything else the caller said").optional())
    """

    def __init__(self, state: _SchemaState) -> None:
        # Use the static constructors.
        self._state = state

    @staticmethod
    def string() -> LiteralSchema:
        """A string."""
        return LiteralSchema(_SchemaState(kind="string"))

    @staticmethod
    def integer() -> LiteralSchema:
        """An integer."""
        return LiteralSchema(_SchemaState(kind="integer"))

    @staticmethod
    def number() -> LiteralSchema:
        """A number."""
        return LiteralSchema(_SchemaState(kind="number"))

    @staticmethod
    def bool() -> LiteralSchema:
        """A boolean. Named `bool` to match the other SDKs (`boolean` is reserved in Java)."""
        return LiteralSchema(_SchemaState(kind="boolean"))

    @staticmethod
    def object() -> ObjectSchema:
        """An object. Add properties with `property()`."""
        return ObjectSchema(_SchemaState(kind="object"))

    @staticmethod
    def array(items: Schema) -> ArraySchema:
        """An array whose elements match `items`."""
        return ArraySchema(_SchemaState(kind="array", items=items))

    @staticmethod
    def from_json(data: typing.Union[str, bytes, typing.Mapping[str, typing.Any]]) -> Schema:
        """Loads a schema in API format (snake_case), given as a JSON string or a parsed dict."""
        return Schema._from_wire(parse(data))

    @staticmethod
    def _from_wire(
        model: WireDict, optional: builtins.bool = False, kind: typing.Optional[SchemaKind] = None
    ) -> Schema:
        """
        Loads a wire-format schema. `optional` is whether its parent leaves it out of `required`. `kind` is given
        where the API only allows one kind (for example a tool's params object), since an empty schema has no `type`.
        """
        kind = kind or _kind_of(model)
        # The API fills unset fields with defaults ("", false). They aren't value sources, but are kept as extra
        # fields so a pulled config writes back unchanged.
        extra = {
            key: deep_copy(value)
            for key, value in model.items()
            if key not in _MODELED_KEYS or _is_unset(key, value, kind)
        }

        def get(key: str) -> typing.Any:
            value = model.get(key)
            return None if value is None or _is_unset(key, value, kind) else value

        base = _SchemaState(
            kind=kind,
            description=get("description"),
            dynamic_variable=get("dynamic_variable"),
            has_constant="constant_value" in model and get("constant_value") is not None,
            constant_value=deep_copy(get("constant_value")),
            omitted=model.get("is_omitted") is True,
            optional=optional,
            extra=extra,
        )
        if kind == "object":
            required = get("required")
            required_list: typing.List[str] = list(required) if isinstance(required, list) else []
            constraints = model.get("required_constraints") or {}
            properties = tuple(
                (name, Schema._from_wire(child, name not in required_list))
                for name, child in (get("properties") or {}).items()
            )
            return ObjectSchema(
                dataclasses.replace(
                    base,
                    properties=properties,
                    loaded_required=tuple(required_list) if isinstance(required, list) else None,
                    any_of=tuple(tuple(c.get("required") or []) for c in constraints.get("any_of") or []),
                    all_of=tuple(tuple(c.get("required") or []) for c in constraints.get("all_of") or []),
                )
            )
        if kind == "array":
            items = get("items")
            return ArraySchema(
                dataclasses.replace(base, items=None if items is None else Schema._from_wire(items, True))
            )
        choices = get("enum")
        allowed = get("allowed_values")
        return LiteralSchema(
            dataclasses.replace(
                base,
                literal_type=deep_copy(model.get("type")),
                system_provided=model.get("is_system_provided") is True,
                choices=None if choices is None else tuple(choices),
                allowed_from=None if allowed is None else allowed.get("dynamic_variable"),
            )
        )

    @builtins.property
    def kind(self) -> SchemaKind:
        """`"string"`, `"integer"`, `"number"`, `"boolean"`, `"object"` or `"array"`."""
        return self._state.kind

    @builtins.property
    def is_optional(self) -> builtins.bool:
        """Whether the parent leaves this property out of `required`."""
        return self._state.optional

    def describe(self: S, text: str) -> S:
        """The LLM provides the value, guided by `text`. On an object or array, documents the container."""
        return self._with(description=text)

    def from_variable(self: S, name: str) -> S:
        """The value is read from the dynamic variable `name` when the tool runs."""
        return self._with(dynamic_variable=name)

    def constant(self: S, value: typing.Any) -> S:
        """The value is always `value`, a JSON value matching the schema's type."""
        return self._with(has_constant=True, constant_value=deep_copy(value))

    def omit(self: S) -> S:
        """The param is left out of the request. Only allowed on an optional property."""
        return self._with(omitted=True)

    def optional(self: S) -> S:
        """Leaves this property out of its parent's `required`. Properties are required unless marked optional."""
        return self._with(optional=True)

    def to_json(self) -> WireDict:
        """The schema in API format (snake_case keys, sorted). Doesn't validate."""
        return typing.cast(WireDict, canonical(self._to_wire()))

    def _to_wire(self) -> WireDict:
        s = self._state
        # Modeled fields that are unset leave the matching extra field (an API default) in place.
        wire: WireDict = deep_copy(s.extra)
        if s.description is not None:
            wire["description"] = s.description
        if s.dynamic_variable is not None:
            wire["dynamic_variable"] = s.dynamic_variable
        if s.omitted:
            wire["is_omitted"] = True
        if s.has_constant:
            wire["constant_value"] = deep_copy(s.constant_value)
        if s.kind == "object":
            wire["type"] = "object"
            if s.properties:
                wire["properties"] = {name: child._to_wire() for name, child in s.properties}
            required = _required_of(s)
            if required:
                wire["required"] = required
            constraints: WireDict = {}
            if s.any_of:
                constraints["any_of"] = [{"required": list(names)} for names in s.any_of]
            if s.all_of:
                constraints["all_of"] = [{"required": list(names)} for names in s.all_of]
            if constraints:
                wire["required_constraints"] = constraints
            return wire
        if s.kind == "array":
            wire["type"] = "array"
            if s.items is not None:
                wire["items"] = s.items._to_wire()
            return wire
        wire["type"] = deep_copy(s.literal_type) if s.literal_type is not None else s.kind
        if s.system_provided:
            wire["is_system_provided"] = True
        if s.choices is not None:
            wire["enum"] = list(s.choices)
        if s.allowed_from is not None:
            wire["allowed_values"] = {"dynamic_variable": s.allowed_from}
        return wire

    def _with(self: S, **changes: typing.Any) -> S:
        return type(self)(dataclasses.replace(self._state, **changes))

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._to_wire()!r})"


class LiteralSchema(Schema):
    """A string, integer, number or boolean."""

    def choices(self, values: typing.Sequence[str]) -> LiteralSchema:
        """The values the LLM may choose from (`enum`). Strings only. Named `choices` to match the other SDKs."""
        return self._with(choices=tuple(values))

    def system_provided(self) -> LiteralSchema:
        """The value is filled in by the system at runtime."""
        return self._with(system_provided=True)

    def allowed_from(self, variable: str) -> LiteralSchema:
        """
        Rejects an LLM value that isn't in the list held by the dynamic variable `variable`. The list isn't shown
        to the LLM. Needs `describe()`.
        """
        return self._with(allowed_from=variable)


class ObjectSchema(Schema):
    """An object with named properties."""

    @builtins.property
    def property_names(self) -> typing.List[str]:
        """Property names, in order."""
        return [name for name, _ in self._state.properties]

    def property_schema(self, name: str) -> typing.Optional[Schema]:
        """The schema of property `name`, if there is one."""
        return next((child for existing, child in self._state.properties if existing == name), None)

    def property(self, name: str, schema: Schema) -> ObjectSchema:
        """Adds the property `name`, or replaces it in place if it exists."""
        properties = list(self._state.properties)
        index = next((i for i, (existing, _) in enumerate(properties) if existing == name), None)
        if index is None:
            properties.append((name, schema))
        else:
            properties[index] = (name, schema)
        return self._with(properties=tuple(properties))

    def without(self, name: str) -> ObjectSchema:
        """Removes the property `name`."""
        return self._with(properties=tuple(entry for entry in self._state.properties if entry[0] != name))

    def require_any_of(self, names: typing.Sequence[str]) -> ObjectSchema:
        """Requires at least one of these sets of properties: appends `names` to `required_constraints.any_of`."""
        return self._with(any_of=(*self._state.any_of, tuple(names)))

    def require_all_of(self, names: typing.Sequence[str]) -> ObjectSchema:
        """Requires all of these sets of properties: appends `names` to `required_constraints.all_of`."""
        return self._with(all_of=(*self._state.all_of, tuple(names)))


class ArraySchema(Schema):
    """A list whose elements match one schema."""

    @builtins.property
    def items(self) -> typing.Optional[Schema]:
        """The element schema."""
        return self._state.items


def _kind_of(model: WireDict) -> SchemaKind:
    kind = model.get("type")
    if isinstance(kind, list):
        # A literal's type can be a list such as ["integer", "null"]; its kind is the non-null member.
        kind = next((t for t in kind if t != "null"), None)
    if kind == "object" or (kind is None and "properties" in model):
        return "object"
    if kind == "array" or (kind is None and "items" in model):
        return "array"
    if kind in ("integer", "number", "boolean"):
        return typing.cast(SchemaKind, kind)
    return "string"


def _required_of(state: _SchemaState) -> typing.List[str]:
    """A loaded object's `required` order for the required properties it still has, then new ones in order."""
    required = [name for name, child in state.properties if not child.is_optional]
    kept = [name for name in state.loaded_required or () if name in required]
    return [*kept, *(name for name in required if name not in kept)]
