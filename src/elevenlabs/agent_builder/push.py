from __future__ import annotations

import dataclasses
import typing

from ..agent_tools.tool import Tool
from ..core.request_options import RequestOptions
from ..types.tool_request_model import ToolRequestModel
from ..types.tool_response_model import ToolResponseModel
from ._definition import tool_definition
from ._wire import WireDict, canonical, get_path, is_subset, response_wire
from .agent import TOOL_IDS_PATH, Agent, raw_workflow_tool_ids
from .errors import AgentPushError, AgentPushResult, PartialAgentPushResult, ToolPushResult
from .project import AgentProject

# The steps of agents.push() and agents.pull(), written once for the sync and the async client: each step yields the
# API call it needs and gets the result back (or the exception, thrown in), and `run_sync` / `run_async` make the
# calls.


@dataclasses.dataclass
class Call:
    """One call on the generated agents or tools client."""

    client: typing.Literal["agents", "tools"]
    method: str
    args: typing.Tuple[typing.Any, ...]
    kwargs: typing.Dict[str, typing.Any]


T = typing.TypeVar("T")
Steps = typing.Generator[Call, typing.Any, T]


class Clients(typing.NamedTuple):
    agents: typing.Any
    tools: typing.Any


def run_sync(steps: Steps[T], clients: Clients) -> T:
    """Runs push or pull steps on sync clients."""
    try:
        call = next(steps)
        while True:
            try:
                value = getattr(getattr(clients, call.client), call.method)(*call.args, **call.kwargs)
            except Exception as err:
                call = steps.throw(err)
            else:
                call = steps.send(value)
    except StopIteration as done:
        return typing.cast(T, done.value)


async def run_async(steps: Steps[T], clients: Clients) -> T:
    """Runs push or pull steps on async clients."""
    try:
        call = next(steps)
        while True:
            try:
                value = await getattr(getattr(clients, call.client), call.method)(*call.args, **call.kwargs)
            except Exception as err:
                call = steps.throw(err)
            else:
                call = steps.send(value)
    except StopIteration as done:
        return typing.cast(T, done.value)


def push_steps(
    agent: Agent,
    *,
    agent_id: typing.Optional[str],
    project: typing.Optional[AgentProject],
    branch_id: typing.Optional[str],
    version_description: typing.Optional[str],
    request_options: typing.Optional[RequestOptions],
) -> Steps[AgentPushResult]:
    """The steps of `agents.push()`. See `AgentsClient.push` for what it does."""
    if project is not None and agent_id is not None:
        raise ValueError("Pass agent_id or project to agents.push(), not both: the project records the agent's id")
    agent.validate()
    if project is not None:
        project._check_branch(agent, branch_id)

    tools = agent.tools()
    if project is not None:
        agent_id = project.agent_id(agent)
    result = PartialAgentPushResult()
    ids: typing.Dict[str, str] = {}
    step = "Couldn't read the agent's tools"
    try:
        # The tools the agent already uses. With a project they're matched by recorded id; without one, by name
        # among the tools this agent uses, so a same-named tool another agent uses is never touched.
        in_use: typing.List[ToolResponseModel] = []
        if agent_id is not None and branch_id is not None:
            # The tools API's `used_by_agent_id` covers the main branch only, so a branch's tools come from its config.
            branch = yield Call(
                "agents", "get", (agent_id,), {"branch_id": branch_id, "request_options": request_options}
            )
            for id in _tool_ids_in(response_wire(branch)):
                in_use.append((yield Call("tools", "get", (id,), {"request_options": request_options})))
        elif agent_id is not None:
            cursor: typing.Optional[str] = None
            while True:
                page = yield Call(
                    "tools",
                    "list",
                    (),
                    {
                        "used_by_agent_id": agent_id,
                        "page_size": 100,
                        "cursor": cursor,
                        "request_options": request_options,
                    },
                )
                in_use.extend(page.tools)
                if not page.has_more or not page.next_cursor:
                    break
                cursor = page.next_cursor
        used_by_name = {_tool_name(remote): remote for remote in in_use}

        for tool in tools:
            if project is not None:
                known_id = project.tool_id(tool)
            else:
                named = used_by_name.get(tool.name)
                known_id = None if named is None else named.id
            remote: typing.Optional[ToolResponseModel] = None
            if known_id is not None:
                step = f'Couldn\'t read tool "{tool.name}" ({known_id})'
                remote = next((t for t in in_use if t.id == known_id), None)
                if remote is None:
                    remote = yield Call("tools", "get", (known_id,), {"request_options": request_options})
            unchanged = project._unchanged_raw(tool) if project is not None else None
            config = unchanged if unchanged is not None else _tool_wire(tool)
            if remote is not None and _same_tool(remote, tool, config):
                ids[tool.name] = remote.id
                result.tools[tool.name] = ToolPushResult(id=remote.id, action="unchanged")
                # The server already matches, but the project may hold an older definition: bring it up to date.
                if project is not None:
                    project._record_tool(tool, remote.id, config)
                continue
            # The generated client drops fields it doesn't model, so the wire config is sent as the request body.
            request = typing.cast(ToolRequestModel, {"tool_config": config})
            options = _with_body(request_options, {"tool_config": config})
            if remote is not None:
                step = f'Couldn\'t update tool "{tool.name}" ({remote.id})'
                yield Call("tools", "update", (remote.id,), {"request": request, "request_options": options})
                ids[tool.name] = remote.id
                result.tools[tool.name] = ToolPushResult(id=remote.id, action="updated")
            else:
                step = f'Couldn\'t create tool "{tool.name}"'
                created = yield Call("tools", "create", (), {"request": request, "request_options": options})
                ids[tool.name] = created.id
                result.tools[tool.name] = ToolPushResult(id=created.id, action="created")
            if project is not None:
                project._record_tool(tool, ids[tool.name], config)

        # The typed body goes through the generated client; the API-format config, sent as extra body parameters,
        # replaces its top-level fields, so settings this SDK doesn't model reach the API too.
        config = agent.to_json(tool_ids=ids)

        # Every id the new config still uses, wherever it is: the agent's tool_ids and the workflow's nodes.
        prompt_ids = get_path(config, TOOL_IDS_PATH)
        kept = {
            *(prompt_ids if isinstance(prompt_ids, list) else []),
            *raw_workflow_tool_ids(config.get("workflow")),
        }
        for remote in in_use:
            if remote.id not in kept and _tool_name(remote) not in result.tools:
                result.tools[_tool_name(remote)] = ToolPushResult(id=remote.id, action="detached")

        typed = dict(agent.build(tool_ids=ids))
        options = _with_body(request_options, config)
        version_id: typing.Optional[str] = None
        if agent_id is None:
            step = f'Couldn\'t create agent "{agent.name}"'
            created_agent = yield Call("agents", "create", (), {**typed, "request_options": options})
            new_id: str = created_agent.agent_id
            action: typing.Literal["created", "updated"] = "created"
        else:
            step = f'Couldn\'t update agent "{agent.name}" ({agent_id})'
            extra: typing.Dict[str, typing.Any] = {}
            if branch_id is not None:
                extra["branch_id"] = branch_id
            if version_description is not None:
                extra["version_description"] = version_description
            updated = yield Call("agents", "update", (agent_id,), {**typed, **extra, "request_options": options})
            version_id = updated.version_id
            new_id = agent_id
            action = "updated"
        result.agent_id = new_id
        result.action = action
        if project is not None:
            project._record_agent(agent, new_id, config, branch_id=branch_id, version_id=version_id)
    except Exception as err:
        _save_quietly(project)
        raise AgentPushError(step, result, err) from err
    if project is not None and project.dir is not None:
        project.save()
    return AgentPushResult(agent_id=new_id, action=action, tools=result.tools)


def pull_steps(
    agent_id: str,
    *,
    project: typing.Optional[AgentProject],
    branch_id: typing.Optional[str],
    request_options: typing.Optional[RequestOptions],
) -> Steps[Agent]:
    """The steps of `agents.pull()`."""
    if project is not None:
        project._check_branch_by_id(agent_id, branch_id)
    response = yield Call("agents", "get", (agent_id,), {"branch_id": branch_id, "request_options": request_options})
    live = response_wire(response)
    # The CLI's pulled-config shape: these keys only, so ids and server metadata stay out of the file.
    config: WireDict = {
        "name": live.get("name"),
        "conversation_config": _or(live.get("conversation_config"), {}),
        "platform_settings": _or(live.get("platform_settings"), {}),
        "tags": _or(live.get("tags"), []),
    }
    if isinstance(live.get("workflow"), dict):
        config["workflow"] = live["workflow"]

    wanted = _tool_ids_in(config)
    tools_by_id: typing.Dict[str, Tool] = {}
    tool_configs: typing.Dict[str, WireDict] = {}
    for id in wanted:
        remote = yield Call("tools", "get", (id,), {"request_options": request_options})
        wire = response_wire(remote.tool_config)
        tool = Tool.from_json(wire)
        # tools.json lists webhook and client tools; others (MCP...) stay attached by id.
        if tool.kind in ("webhook", "client"):
            tools_by_id[id] = tool
            tool_configs[id] = typing.cast(WireDict, canonical(wire))

    agent = Agent.from_json(config, tools_by_id=tools_by_id)
    if project is not None:
        for id, tool in tools_by_id.items():
            project._record_tool(tool, id, tool_configs[id], "id")
        project._record_agent(
            agent, agent_id, config, branch_id=branch_id, version_id=response.version_id, match_by="id"
        )
        if project.dir is not None:
            project.save()
    return agent


def _tool_ids_in(config: WireDict) -> typing.List[str]:
    """Every tool id an agent config uses, in the agent's `tool_ids` and the workflow's nodes, once each, in order."""
    prompt_ids = get_path(config, TOOL_IDS_PATH)
    return list(
        dict.fromkeys(
            [*(prompt_ids if isinstance(prompt_ids, list) else []), *raw_workflow_tool_ids(config.get("workflow"))]
        )
    )


def _or(value: typing.Any, default: typing.Any) -> typing.Any:
    return default if value is None else value


def _with_body(request_options: typing.Optional[RequestOptions], body: WireDict) -> RequestOptions:
    options = typing.cast(RequestOptions, dict(request_options or {}))
    options["additional_body_parameters"] = body
    return options


def _tool_name(remote: ToolResponseModel) -> str:
    name = getattr(remote.tool_config, "name", None)
    return remote.id if name is None else str(name)


def _tool_wire(tool: Tool) -> WireDict:
    return tool.to_json()


def _same_tool(remote: ToolResponseModel, tool: Tool, config: WireDict) -> bool:
    """
    Whether the server already has this tool as defined. Modeled fields are compared through the builder, so both
    sides normalize alike; the config to send must also be contained in the server's, so a change to a field the
    builder doesn't model still counts.
    """
    try:
        local = tool_definition(tool)
        return (
            local is not None
            and tool_definition(Tool.from_response(remote)) == local
            and is_subset(config, response_wire(remote.tool_config))
        )
    except Exception:
        return False


def _save_quietly(project: typing.Optional[AgentProject]) -> None:
    if project is None or project.dir is None:
        return
    try:
        project.save()
    except Exception:
        pass  # The push error is the one to report; the ids it carries are in the raised result.
