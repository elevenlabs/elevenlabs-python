import json
import re
import typing

from elevenlabs.agent_tools import AuthConnection, Destination, Header, Schema, SystemTool, Tool, ToolValidationError

# Interprets the language-neutral tool fixtures in fixtures/, copied from the reference SDK
# (elevenlabs-js, docs/agents-as-code/fixtures/tools). See tool-spec.md there, "Fixtures".

Op = typing.Dict[str, typing.Any]

_SYSTEM_CONSTRUCTORS: typing.Dict[str, typing.Callable[..., SystemTool]] = {
    "end_call": SystemTool.end_call,
    "skip_turn": SystemTool.skip_turn,
    "language_detection": SystemTool.language_detection,
    "play_keypad_touch_tone": SystemTool.play_keypad_touch_tone,
    "voicemail_detection": SystemTool.voicemail_detection,
    "knowledge_base": SystemTool.knowledge_base,
    "transfer_to_number": SystemTool.transfer_to_number,
    "transfer_to_agent": SystemTool.transfer_to_agent,
}

# Which positional argument is a schema, for the ops that take one.
_SCHEMA_ARG = {"pathParam": 1, "queryParam": 1, "body": 0, "response": 0, "param": 1, "property": 1}


def _snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _destination(raw: typing.Dict[str, typing.Any]) -> Destination:
    if "phone" in raw:
        return Destination.phone(raw["phone"])
    if "phoneVariable" in raw:
        return Destination.phone_variable(raw["phoneVariable"])
    if "sip" in raw:
        return Destination.sip(raw["sip"])
    if "sipVariable" in raw:
        return Destination.sip_variable(raw["sipVariable"])
    return Destination.agent(raw["agent"], node_id=raw.get("nodeId"))


def _header(raw: typing.Dict[str, str]) -> Header:
    if "value" in raw:
        return Header.value(raw["value"])
    if "secret" in raw:
        return Header.secret(raw["secret"])
    if "variable" in raw:
        return Header.variable(raw["variable"])
    return Header.env_var(raw["envVar"])


def _schema_arg(raw: typing.Dict[str, typing.Any]) -> Schema:
    # Wire-format JSON, or `{"build": [ops]}` for a schema built with Schema methods (e.g. `optional()`).
    return _build_schema(raw["build"]) if "build" in raw else Schema.from_json(raw)


def _call(target: typing.Any, op: Op) -> typing.Any:
    args = list(op.get("args") or [])
    name = op["op"]
    if name in _SCHEMA_ARG:
        args[_SCHEMA_ARG[name]] = _schema_arg(args[_SCHEMA_ARG[name]])
    if name == "header":
        args[1] = _header(args[1])
    if name == "auth":
        args[0] = AuthConnection.id(args[0]["id"]) if "id" in args[0] else AuthConnection.env_var(args[0]["envVar"])
    if name == "transfer":
        args[1] = _destination(args[1])
    # A trailing options object (camelCase keys) becomes keyword arguments.
    kwargs: typing.Dict[str, typing.Any] = {}
    if name in ("options", "assign", "transfer") and args and isinstance(args[-1], dict):
        kwargs = {_snake(key): value for key, value in args.pop().items()}
    return getattr(target, _snake(name))(*args, **kwargs)


def _build_schema(ops: typing.List[Op]) -> Schema:
    first, rest = ops[0], ops[1:]
    if first["op"] == "array":
        schema: typing.Any = Schema.array(_schema_arg(first["args"][0]))
    elif first["op"] == "fromJSON":
        schema = Schema.from_json(first["args"][0])
    else:
        schema = getattr(Schema, first["op"])()
    for op in rest:
        schema = _call(schema, op)
    return typing.cast(Schema, schema)


def run_fixture(fixture: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """Runs a fixture and returns `{"json": ...}` with the canonical JSON string, or `{"errors": [...]}`."""
    if "schema" in fixture:
        return {"json": json.dumps(_build_schema(fixture["schema"]).to_json(), indent=2, ensure_ascii=False) + "\n"}
    spec = fixture.get("tool") or {}
    tool: Tool
    if "from" in fixture:
        tool = Tool.from_json(fixture["from"])
    elif "webhook" in spec:
        tool = Tool.webhook(*spec["webhook"])
    elif "client" in spec:
        tool = Tool.client(*spec["client"])
    else:
        options = {_snake(key): value for key, value in (spec.get("systemOptions") or {}).items()}
        tool = _SYSTEM_CONSTRUCTORS[spec["system"]](**options)
    for op in fixture.get("ops") or []:
        _call(tool, op)
    try:
        return {"json": tool.to_json_string()}
    except ToolValidationError as err:
        return {"errors": [issue.code for issue in err.issues]}
