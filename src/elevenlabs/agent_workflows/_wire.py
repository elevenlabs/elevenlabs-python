import copy
import typing

from ..core.jsonable_encoder import jsonable_encoder

# The builder keeps its state in API wire format (snake_case keys, as the REST API and the CLI's
# agent_configs/*.json use them), which is also what the generated Pydantic models dump to.

WireDict = typing.Dict[str, typing.Any]


def to_wire(value: typing.Any) -> typing.Any:
    """Converts a generated model, or a dict or list holding them, to wire format. `None` values are dropped."""
    return _drop_none(jsonable_encoder(value))


def _drop_none(value: typing.Any) -> typing.Any:
    if isinstance(value, dict):
        return {key: _drop_none(item) for key, item in value.items() if item is not None}
    if isinstance(value, list):
        return [_drop_none(item) for item in value]
    return value


def canonical(value: typing.Any) -> typing.Any:
    """
    Sorts object keys at every level and writes whole floats as integers, so the JSON matches every other SDK's
    byte for byte (JavaScript can't tell `300.0` from `300`).
    """
    if isinstance(value, dict):
        return {key: canonical(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [canonical(item) for item in value]
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def deep_copy(value: typing.Any) -> typing.Any:
    return copy.deepcopy(value)
