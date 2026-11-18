"""Compares `@client_tool` functions with the client tools stored on the server, so a schema mismatch shows up at
startup rather than mid-conversation."""

import dataclasses
import typing
import warnings

from ..types.tool_response_model import ToolResponseModel
from ._wire import WireDict, strip_nulls, to_wire
from .decorators import ClientToolFunction
from .schema import _kind_of


class ToolSchemaDriftWarning(UserWarning):
    """Issued by `tools.check_client_tools()` for each difference between a function and the tool on the server."""


class ToolSchemaDriftError(Exception):
    """Raised by `tools.check_client_tools(..., strict=True)` when a function doesn't match the tool on the server."""

    def __init__(self, drift: typing.Sequence["ToolSchemaDrift"]) -> None:
        super().__init__(
            "Client tools don't match the agent's tools on the server:\n" + "\n".join(f"  - {d}" for d in drift)
        )
        self.drift = list(drift)


@dataclasses.dataclass(frozen=True)
class ToolSchemaDrift:
    """One difference between a `@client_tool` function and the client tool the agent has on the server."""

    tool: str
    """The tool's name."""
    message: str
    """What differs, and what happens when the agent calls the tool."""
    path: typing.Optional[str] = None
    """The param it's about, e.g. `"address.city"`, or `None` for the tool as a whole."""

    def __str__(self) -> str:
        return f"{self.tool}: {self.message}"


def compare_client_tools(
    functions: typing.Sequence[ClientToolFunction], server_tools: typing.Sequence[ToolResponseModel]
) -> typing.List[ToolSchemaDrift]:
    """
    Compares each function with the client tool of the same name in `server_tools`. Only what decides whether the
    function can handle the agent's calls is compared: param names, types, choices and which are required.
    Descriptions and value sources don't matter to the function, so they're ignored.
    """
    remote: typing.Dict[str, WireDict] = {}
    for response in server_tools:
        config = typing.cast(WireDict, strip_nulls(to_wire(response.tool_config)))
        if config.get("type") == "client" and isinstance(config.get("name"), str):
            remote.setdefault(config["name"], config)

    drift: typing.List[ToolSchemaDrift] = []
    for fn in functions:
        server = remote.get(fn.name)
        if server is None:
            drift.append(
                ToolSchemaDrift(fn.name, "the agent has no client tool with this name, so it never calls the function")
            )
            continue
        local = fn.tool.to_json().get("parameters")
        for path, message in _compare(server.get("parameters"), local, ""):
            drift.append(ToolSchemaDrift(fn.name, message, path or None))
    return drift


def report(drift: typing.List[ToolSchemaDrift], strict: bool) -> typing.List[ToolSchemaDrift]:
    if strict and drift:
        raise ToolSchemaDriftError(drift)
    for item in drift:
        warnings.warn(str(item), ToolSchemaDriftWarning, stacklevel=3)
    return drift


def _compare(
    server: typing.Optional[WireDict], local: typing.Optional[WireDict], path: str
) -> typing.Iterator[typing.Tuple[str, str]]:
    server = server or {"type": "object"}
    local = local or {"type": "object"}
    where = f"param '{path}'" if path else "the params"

    # The API may write a type as a list (["integer", "null"]) or leave it out of an object or array, so compare kinds.
    kind = _kind_of(server)
    if kind != _kind_of(local):
        yield path, f"{where} is {kind} on the server but {_kind_of(local)} in the function"
        return
    if sorted(server.get("enum") or []) != sorted(local.get("enum") or []):
        yield path, (f"{where} allows {_choices(server)} on the server but {_choices(local)} in the function")
    if kind == "array":
        yield from _compare(server.get("items"), local.get("items"), f"{path}[]")
        return
    if kind != "object":
        return

    server_props: WireDict = server.get("properties") or {}
    local_props: WireDict = local.get("properties") or {}
    server_required = set(server.get("required") or [])
    local_required = set(local.get("required") or [])
    for name in local_props:
        child = f"{path}.{name}" if path else name
        if name not in server_props:
            effect = "the call fails because it's required" if name in local_required else "it always gets its default"
            yield child, f"'{child}' is in the function but not on the server, so the agent never sends it: {effect}"
            continue
        if name in local_required and name not in server_required:
            yield child, f"'{child}' is optional on the server but required in the function, so calls without it fail"
        elif name in server_required and name not in local_required:
            yield child, f"'{child}' is required on the server but optional in the function"
        yield from _compare(server_props[name], local_props[name], child)
    for name in server_props:
        if name not in local_props:
            child = f"{path}.{name}" if path else name
            yield child, f"'{child}' is on the server but not in the function, so the function never receives it"


def _choices(schema: WireDict) -> str:
    values = schema.get("enum")
    return ", ".join(repr(v) for v in values) if values else "any value"
