import re
import typing

from elevenlabs.agent_workflows import (
    Condition,
    ConditionInput,
    Destination,
    Expr,
    Workflow,
    WorkflowBranch,
    WorkflowChain,
    WorkflowNode,
    WorkflowValidationError,
)
from elevenlabs.core.unchecked_base_model import construct_type
from elevenlabs.types import AstNodeInput, WorkflowToolLocatorSchemaOverridesValue

# Interprets the language-neutral fixtures in fixtures/, copied from the reference SDK
# (elevenlabs-js, docs/agents-as-code). See workflow-spec.md there, "Fixtures".

Op = typing.Dict[str, typing.Any]


def _condition(raw: typing.Any) -> ConditionInput:
    if isinstance(raw, str):
        return raw
    if "llm" in raw:
        return Condition.llm(raw["llm"], label=raw.get("label"))
    # Parse the wire-format AST into the generated model, as callers holding API data would.
    ast = construct_type(type_=AstNodeInput, object_=raw["expr"])  # type: ignore[arg-type]
    return Condition.expr(Expr.from_model(ast), label=raw.get("label"))


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


def _snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _options(op: Op) -> typing.Dict[str, typing.Any]:
    # Option keys are canonical camelCase names; nested values are in API wire format, so parse them.
    opts = {_snake(key): value for key, value in (op.get("options") or {}).items()}
    if "destination" in opts:
        opts["destination"] = _destination(opts["destination"])
    if "schema_overrides" in opts:
        opts["schema_overrides"] = {
            tool_id: {
                path: construct_type(type_=WorkflowToolLocatorSchemaOverridesValue, object_=value)  # type: ignore[arg-type]
                for path, value in paths.items()
            }
            for tool_id, paths in opts["schema_overrides"].items()
        }
    return opts


def _runner(wf: Workflow, ops: typing.List[Op]) -> typing.Callable[[WorkflowChain], typing.Optional[WorkflowNode]]:
    return lambda start: _run(wf, ops, start)


def _run(wf: Workflow, ops: typing.List[Op], first: WorkflowChain) -> typing.Optional[WorkflowNode]:
    previous: WorkflowChain = first
    result: typing.Optional[WorkflowNode] = None
    for op in ops:
        kind = op["op"]
        if kind == "update":
            wf.node(op["node"]).update(**_options(op))
            continue
        if kind == "remove":
            wf.remove(op["node"])
            continue
        if kind == "onResult":
            node = typing.cast(WorkflowNode, previous) if "at" not in op else wf.node(op["at"])
            # Pass the branches in the fixture's key order, so a failure-first fixture reaches the builder that way.
            branches: typing.Dict[str, typing.Callable[[WorkflowBranch], typing.Any]] = {}
            for key in op:
                if key in ("success", "failure"):
                    branches[key] = _runner(wf, op[key])
            node.on_result(**branches)
            continue
        if kind == "insertBetween":
            wf.insert_between(op["source"], op["target"], _runner(wf, op.get("ops", [])))
            continue

        at: typing.Any = previous if "at" not in op else wf if op["at"] == "$start" else wf.node(op["at"])
        if "when" in op:
            at = at.when(_condition(op["when"]), back=_condition(op["back"]) if "back" in op else None)
        elif op.get("onSuccess"):
            at = at.on_success()
        elif op.get("onFailure"):
            at = at.on_failure()

        if kind == "converse":
            result = at.converse(op["id"], op["prompt"], **_options(op))
        elif kind == "tool":
            result = at.tool(op["id"], op["toolIds"], **_options(op))
        elif kind == "transfer":
            result = at.transfer(op["id"], _destination(op["destination"]), **_options(op))
        elif kind == "end":
            result = at.end(**_options(op))
        elif kind == "goTo":
            result = at.go_to(op["target"], back=_condition(op["back"]) if "back" in op else None)
        else:
            raise ValueError(f"Unknown fixture op {kind!r}")
        previous = typing.cast(WorkflowNode, result)
    return result


def run_fixture(fixture: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """Runs a fixture and returns `{"json": ...}` with the canonical JSON string, or `{"errors": [...]}` if build fails."""
    if "from" in fixture:
        wf = Workflow.from_json(fixture["from"])
    else:
        wf = Workflow(prevent_subagent_loops=(fixture.get("workflow") or {}).get("preventSubagentLoops"))
    _run(wf, fixture["ops"], wf)
    try:
        return {"json": wf.to_json_string()}
    except WorkflowValidationError as err:
        return {"errors": [issue.code for issue in err.issues]}
