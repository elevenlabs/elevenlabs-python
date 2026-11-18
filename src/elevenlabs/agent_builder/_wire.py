import typing

import pydantic
from ..agent_workflows._wire import WireDict, canonical, deep_copy, to_wire
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import IS_PYDANTIC_V2

# Helpers for agent configs in API wire format (snake_case JSON), shared with the tool and workflow builders.

__all__ = [
    "WireDict",
    "canonical",
    "deep_copy",
    "deep_merge",
    "delete_path",
    "get_path",
    "is_object",
    "is_subset",
    "response_wire",
    "set_path",
    "to_wire",
]


def is_object(value: typing.Any) -> bool:
    return isinstance(value, dict)


def get_path(target: typing.Any, path: typing.Sequence[str]) -> typing.Any:
    """The value at `path`, or `None` if any step is missing."""
    current = target
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def has_path(target: typing.Any, path: typing.Sequence[str]) -> bool:
    """Whether `path` is set, even to `null`."""
    current = target
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return False
        current = current[key]
    return True


def set_path(target: WireDict, path: typing.Sequence[str], value: typing.Any) -> None:
    """Sets the value at `path`, creating dicts along the way."""
    current = target
    for key in path[:-1]:
        if not isinstance(current.get(key), dict):
            current[key] = {}
        current = current[key]
    current[path[-1]] = value


def delete_path(target: WireDict, path: typing.Sequence[str]) -> None:
    """Removes the key at `path`, if it's there."""
    current: typing.Any = target
    for key in path[:-1]:
        current = current.get(key) if isinstance(current, dict) else None
    if isinstance(current, dict):
        current.pop(path[-1], None)


def deep_merge(target: WireDict, source: typing.Mapping[str, typing.Any]) -> WireDict:
    """
    Merges `source` into `target`: dicts merge key by key, anything else (lists included) replaces. Values are
    copied, so later edits to `source` don't reach `target`.
    """
    for key, value in source.items():
        existing = target.get(key)
        if isinstance(value, dict) and isinstance(existing, dict):
            deep_merge(existing, value)
        else:
            target[key] = deep_copy(value)
    return target


def is_subset(local: typing.Any, remote: typing.Any) -> bool:
    """
    Whether every value in `local` is in `remote` at the same place. Extra keys in `remote` (server defaults) are
    fine, and a `null` in `local` matches anything.
    """
    if isinstance(local, list):
        return (
            isinstance(remote, list)
            and len(local) == len(remote)
            and all(is_subset(item, other) for item, other in zip(local, remote))
        )
    if isinstance(local, dict):
        return isinstance(remote, dict) and all(
            value is None or is_subset(value, remote.get(key)) for key, value in local.items()
        )
    if isinstance(local, bool) or isinstance(remote, bool):
        return type(local) is type(remote) and local == remote
    if isinstance(local, (int, float)) and isinstance(remote, (int, float)):
        # JSON can't tell 1 from 1.0, and a parsed response may hold either.
        return float(local) == float(remote)
    return type(local) is type(remote) and local == remote


def response_wire(model: typing.Any) -> typing.Any:
    """
    A parsed API response model back in wire format, with only the fields the response had: unlike `to_wire()`,
    fields the server left out aren't filled in with the model's defaults. Unknown fields are kept.
    """
    if not isinstance(model, pydantic.BaseModel):
        return to_wire(model)
    if IS_PYDANTIC_V2:
        return pydantic.BaseModel.model_dump(  # type: ignore[attr-defined]
            model, by_alias=True, exclude_unset=True, mode="json", warnings=False
        )
    return jsonable_encoder(pydantic.BaseModel.dict(model, by_alias=True, exclude_unset=True))
