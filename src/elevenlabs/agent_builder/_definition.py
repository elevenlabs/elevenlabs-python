import inspect
import json
import typing

import pydantic
import typing_extensions
from ..agent_tools.tool import Tool
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..types.tool_request_model_tool_config import (
    ToolRequestModelToolConfig_Client,
    ToolRequestModelToolConfig_System,
    ToolRequestModelToolConfig_Webhook,
)

_MODELS: typing.Dict[str, typing.Type[pydantic.BaseModel]] = {
    "webhook": ToolRequestModelToolConfig_Webhook,
    "client": ToolRequestModelToolConfig_Client,
    "system": ToolRequestModelToolConfig_System,
}


def tool_definition(tool: Tool) -> typing.Optional[str]:
    """
    A tool's definition as this SDK models it, as a string to compare: its wire config without the fields the
    generated models don't declare. The tool builder keeps such fields from a loaded config, but a tool written in
    code can't have them, so they don't count when telling whether two definitions are the same tool. `None` if the
    tool is invalid.
    """
    try:
        wire = tool.to_json()
    except Exception:
        return None
    model = _MODELS.get(tool.kind)
    return json.dumps(wire if model is None else _modeled(wire, model), sort_keys=True)


def _modeled(value: typing.Any, annotation: typing.Any) -> typing.Any:
    """`value` with the keys `annotation` doesn't declare left out, at every level the annotation describes."""
    annotation = _unwrap(annotation)
    origin = typing_extensions.get_origin(annotation)
    models = _models(annotation)
    if models and isinstance(value, dict):
        # For a union of models (such as the kinds of schema property), a key any of them declares is modeled. Its
        # value is narrowed further only when a single member declares it, so no modeled field is ever dropped.
        declared: typing.Dict[str, typing.List[typing.Any]] = {}
        for model in models:
            for key, field_type in _fields(model).items():
                declared.setdefault(key, []).append(field_type)
        return {
            key: _modeled(item, declared[key][0]) if len(declared[key]) == 1 else item
            for key, item in value.items()
            if key in declared
        }
    if origin in (list, typing.List) and isinstance(value, list):
        (item_type,) = typing_extensions.get_args(annotation) or (typing.Any,)
        return [_modeled(item, item_type) for item in value]
    if origin in (dict, typing.Dict) and isinstance(value, dict):
        args = typing_extensions.get_args(annotation)
        item_type = args[1] if len(args) == 2 else typing.Any
        return {key: _modeled(item, item_type) for key, item in value.items()}
    # Unions of several types, `Any` and plain values: kept as they are.
    return value


def _resolve(annotation: typing.Any) -> typing.Any:
    """
    A forward reference to a generated type as that type. Older Pythons keep the generated models' string
    annotations, such as `Optional["ArrayJsonSchemaPropertyInputItems"]`, unresolved; every generated type is exported
    from `elevenlabs.types`, so it's looked up there. Anything else is returned as it is.
    """
    if isinstance(annotation, typing.ForwardRef):
        from .. import types

        return getattr(types, annotation.__forward_arg__, annotation)
    return annotation


def _unwrap(annotation: typing.Any) -> typing.Any:
    """`Optional[X]` and `Annotated[X, ...]` as `X`, with forward references resolved."""
    while True:
        annotation = _resolve(annotation)
        origin = typing_extensions.get_origin(annotation)
        args = typing_extensions.get_args(annotation)
        if origin is typing_extensions.Annotated:
            annotation = args[0]
        elif origin is typing.Union and len([arg for arg in args if arg is not type(None)]) == 1:
            annotation = next(arg for arg in args if arg is not type(None))
        else:
            return annotation


def _models(annotation: typing.Any) -> typing.List[typing.Type[pydantic.BaseModel]]:
    """
    The generated model `annotation` is, or the models of a union made only of models, optional or not (`Optional`
    of a union of several models is a union that includes `None`); else nothing.
    """
    members = (
        [_unwrap(arg) for arg in typing_extensions.get_args(annotation) if arg is not type(None)]
        if typing_extensions.get_origin(annotation) is typing.Union
        else [annotation]
    )
    if members and all(inspect.isclass(member) and issubclass(member, pydantic.BaseModel) for member in members):
        return members
    return []


def _fields(model: typing.Type[pydantic.BaseModel]) -> typing.Dict[str, typing.Any]:
    """The model's fields by wire name (alias), with their types."""
    if IS_PYDANTIC_V2:
        return {
            (info.alias or name): info.annotation
            for name, info in model.model_fields.items()  # type: ignore[attr-defined]
        }
    return {field.alias: field.outer_type_ for field in model.__fields__.values()}  # type: ignore[attr-defined]
