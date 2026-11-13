import json
import typing

# The tool builder keeps its state in API wire format, like the workflow builder, and shares its helpers.
from ..agent_workflows._wire import WireDict, canonical, deep_copy, to_wire

__all__ = ["WireDict", "canonical", "deep_copy", "to_wire", "parse", "strip_nulls"]

# Free-form JSON values, where `null` is data rather than an unset field.
_FREE_FORM_KEYS = frozenset({"constant_value", "dynamic_variable_placeholders"})


def parse(data: typing.Union[str, bytes, typing.Mapping[str, typing.Any]]) -> WireDict:
    """A JSON string, or a parsed mapping, as a fresh dict with the API's `null` (unset) fields removed."""
    parsed = json.loads(data) if isinstance(data, (str, bytes)) else data
    return typing.cast(WireDict, strip_nulls(to_wire(parsed)))


def strip_nulls(value: typing.Any) -> typing.Any:
    """
    Drops `null` fields at every level, except inside free-form values such as constants. A `null` constant is
    kept: on a literal it's a real constant (the API's unset value is `""`). Loading a schema drops it from a
    container, where it means unset.
    """
    if isinstance(value, dict):
        return {
            key: (deep_copy(item) if key in _FREE_FORM_KEYS else strip_nulls(item))
            for key, item in value.items()
            if item is not None or key == "constant_value"
        }
    if isinstance(value, list):
        return [strip_nulls(item) for item in value]
    return value
