from __future__ import annotations

import json
import typing

import pydantic
import typing_extensions
from ..agent_tools.tool import SystemTool, Tool
from ..agent_workflows.workflow import Workflow
from ..core.pydantic_utilities import IS_PYDANTIC_V2, _get_model_fields, parse_obj_as
from ..core.unchecked_base_model import construct_type
from ..types.agent_config import AgentConfig
from ..types.agent_platform_settings_request_model import AgentPlatformSettingsRequestModel
from ..types.agent_workflow_request_model import AgentWorkflowRequestModel
from ..types.conversational_config import ConversationalConfig
from ..types.llm import Llm
from ..types.prompt_agent_api_model_output import PromptAgentApiModelOutput
from ..types.tts_conversational_config_output import TtsConversationalConfigOutput
from ..types.tts_conversational_model import TtsConversationalModel
from ._wire import WireDict, canonical, deep_copy, deep_merge, delete_path, get_path, has_path, set_path, to_wire
from .errors import AgentIssue, AgentValidationError

OnWarning = typing.Callable[[AgentIssue], typing.Any]

ConversationConfigInput = typing.Union[ConversationalConfig, typing.Mapping[str, typing.Any]]
"""The generated `ConversationalConfig`, or the same settings as a wire-format (snake_case) dict."""

PlatformSettingsInput = typing.Union[AgentPlatformSettingsRequestModel, typing.Mapping[str, typing.Any]]
"""The generated `AgentPlatformSettingsRequestModel`, or the same settings as a wire-format (snake_case) dict."""


class _AgentRequestFields(typing_extensions.TypedDict):
    name: str
    conversation_config: ConversationalConfig
    platform_settings: AgentPlatformSettingsRequestModel
    tags: typing.List[str]


class AgentRequest(_AgentRequestFields, total=False):
    """
    What `Agent.build()` returns: the keyword arguments `agents.create()` takes, so
    `client.conversational_ai.agents.create(**agent.build(tool_ids=...))` works. `agents.update()` takes them too.
    `workflow` is there only if the agent has one.
    """

    workflow: AgentWorkflowRequestModel


# Where each typed option goes, as the piece of the generated `ConversationalConfig` it sets. The pieces are built
# with the generated models, which reject a field they don't declare (see `_check_fields`), and the wire path is read
# off the serialized piece, so a wrong or renamed field fails instead of writing to a hand-typed path.
_TYPED_OPTIONS: typing.Dict[str, typing.Callable[[typing.Any], ConversationalConfig]] = {
    "prompt": lambda prompt: ConversationalConfig(agent=AgentConfig(prompt=PromptAgentApiModelOutput(prompt=prompt))),
    "first_message": lambda first_message: ConversationalConfig(agent=AgentConfig(first_message=first_message)),
    "language": lambda language: ConversationalConfig(agent=AgentConfig(language=language)),
    "llm": lambda llm: ConversationalConfig(agent=AgentConfig(prompt=PromptAgentApiModelOutput(llm=llm))),
    "temperature": lambda temperature: ConversationalConfig(
        agent=AgentConfig(prompt=PromptAgentApiModelOutput(temperature=temperature))
    ),
    "voice_id": lambda voice_id: ConversationalConfig(tts=TtsConversationalConfigOutput(voice_id=voice_id)),
    "tts_model": lambda model_id: ConversationalConfig(tts=TtsConversationalConfigOutput(model_id=model_id)),
}


def _check_fields(model: pydantic.BaseModel) -> None:
    """Rejects fields a generated model doesn't declare, which it would otherwise keep as extras."""
    declared = _get_model_fields(type(model))
    given = model.model_fields_set if IS_PYDANTIC_V2 else model.__fields_set__  # type: ignore[attr-defined]
    unknown = sorted(set(given) - set(declared))
    if unknown:
        raise TypeError(f"{type(model).__name__} has no field {', '.join(unknown)}")
    for field in given:
        value = getattr(model, field)
        if isinstance(value, pydantic.BaseModel):
            _check_fields(value)


def _typed_option(key: str, value: typing.Any) -> typing.Tuple[typing.List[str], typing.Any]:
    """The API-format path a typed option sets, and its value in API format."""
    piece = _TYPED_OPTIONS[key](value)
    _check_fields(piece)
    wire = to_wire(piece)
    path = ["conversation_config"]
    while isinstance(wire, dict) and len(wire) == 1:
        field = next(iter(wire))
        path.append(field)
        wire = wire[field]
    return path, wire


TOOL_IDS_PATH = ("conversation_config", "agent", "prompt", "tool_ids")
BUILT_IN_TOOLS_PATH = ("conversation_config", "agent", "prompt", "built_in_tools")
PROMPT_PATH = tuple(_typed_option("prompt", "")[0])


class Agent:
    """
    An agent, written as code: its settings, its tools and its workflow in one definition. Push it with
    `client.conversational_ai.agents.push(agent)`, which creates or updates the tools and the agent together.

    Examples
    --------
    from elevenlabs.agent_builder import Agent
    from elevenlabs.agent_tools import SystemTool

    agent = Agent(
        "Support line",
        prompt="You are a support agent for Acme.",
        first_message="Hi, how can I help?",
        tools=[SystemTool.end_call(), get_order],
        workflow=wf,
    )
    result = client.conversational_ai.agents.push(agent)
    """

    def __init__(
        self,
        name: str,
        *,
        prompt: typing.Optional[str] = None,
        first_message: typing.Optional[str] = None,
        language: typing.Optional[str] = None,
        llm: typing.Optional[Llm] = None,
        temperature: typing.Optional[float] = None,
        voice_id: typing.Optional[str] = None,
        tts_model: typing.Optional[TtsConversationalModel] = None,
        tags: typing.Optional[typing.Sequence[str]] = None,
        tools: typing.Optional[typing.Sequence[Tool]] = None,
        tool_ids: typing.Optional[typing.Sequence[str]] = None,
        workflow: typing.Optional[Workflow] = None,
        conversation_config: typing.Optional[ConversationConfigInput] = None,
        platform_settings: typing.Optional[PlatformSettingsInput] = None,
    ) -> None:
        """
        `prompt` is the agent's instructions (`conversation_config.agent.prompt.prompt`), `first_message` what it
        says first, `language` e.g. `"en"`, `llm` and `temperature` the model settings, `voice_id` and `tts_model`
        the voice (`conversation_config.tts`).

        `tools` are the tools the agent can use anywhere: webhook and client tools are created or updated by
        `agents.push()` and attached by id; system tools go into `prompt.built_in_tools`. `tool_ids` attaches
        existing tools as they are; `agents.push()` doesn't create or change them. `workflow` is the agent's
        workflow, whose tool nodes can take `Tool` objects that `agents.push()` manages too.

        `conversation_config` and `platform_settings` take any other setting, as the generated models or as
        wire-format dicts, merged under the options above. Setting a field there that an option above also sets
        is reported by `validate()`.
        """
        self._name = name
        self._typed: typing.Dict[str, typing.Any] = {}
        self._tags: typing.Optional[typing.List[str]] = None
        self._tools: typing.List[Tool] = []
        self._tool_ids: typing.List[str] = []
        self._workflow: typing.Optional[Workflow] = None
        # A loaded workflow nobody has edited yet, kept in API format so it round-trips exactly.
        self._raw_workflow: typing.Optional[WireDict] = None
        self._tools_by_id: typing.Dict[str, Tool] = {}
        # The loaded `tool_ids`, so a loaded agent keeps its tool order.
        self._loaded_tool_ids: typing.List[str] = []
        # Whether `tools` or `tool_ids` was given (even empty), so the agent sets `tool_ids` rather than leaving
        # it alone.
        self._tool_list_given = False
        # Loaded system tools with their config as loaded, sent as-is while the tool is unchanged. By `id(tool)`.
        self._loaded_system: typing.Dict[int, typing.Tuple[Tool, typing.Any, typing.Optional[str]]] = {}
        # Settings loaded from a config, in API format. Typed options and raw options are applied on top.
        self._base: WireDict = {}
        self._raw_conversation_config: typing.List[ConversationConfigInput] = []
        self._raw_platform_settings: typing.List[PlatformSettingsInput] = []
        self.update(
            prompt=prompt,
            first_message=first_message,
            language=language,
            llm=llm,
            temperature=temperature,
            voice_id=voice_id,
            tts_model=tts_model,
            tags=tags,
            tools=tools,
            tool_ids=tool_ids,
            workflow=workflow,
            conversation_config=conversation_config,
            platform_settings=platform_settings,
        )

    @staticmethod
    def from_json(
        config: typing.Union[str, bytes, typing.Mapping[str, typing.Any]],
        *,
        tools_by_id: typing.Optional[typing.Mapping[str, Tool]] = None,
    ) -> Agent:
        """
        Loads an agent config in API format (snake_case): a CLI `agent_configs/*.json` file, or the `to_json()` of
        an agent, as a JSON string or a parsed dict. Webhook and client tools found in `tools_by_id` become `Tool`
        objects the agent manages; the other ids, including tools of other kinds such as `mcp`, stay as `tool_ids`.
        Fields this SDK doesn't model are kept, so an unedited agent round-trips exactly.
        """
        parsed = json.loads(config) if isinstance(config, (str, bytes)) else config
        if not isinstance(parsed, typing.Mapping):
            raise TypeError("An agent config must be a JSON object")
        base = typing.cast(WireDict, deep_copy(to_wire(dict(parsed))))
        name = base.pop("name", None)
        tags = base.pop("tags", None)
        workflow = base.pop("workflow", None)
        by_id = dict(tools_by_id or {})

        agent = Agent(name if isinstance(name, str) else "")
        agent._base = base
        agent._tags = list(tags) if isinstance(tags, list) else None
        agent._tools_by_id = by_id
        ids = get_path(base, TOOL_IDS_PATH)
        if isinstance(ids, list):
            delete_path(base, TOOL_IDS_PATH)
            agent._loaded_tool_ids = list(ids)
            agent._tool_list_given = True
            for tool_id in ids:
                # Like pull: kinds push doesn't manage (mcp...) stay attached by id. `_tools_by_id` keeps them, so a
                # workflow node or `add_tool()` can still use the object under that id.
                tool = by_id.get(tool_id)
                if tool is not None and _is_managed(tool):
                    agent._tools.append(tool)
                else:
                    agent._tool_ids.append(tool_id)

        # System tools become SystemTool objects, so replacing `tools` replaces them like on an agent built in code.
        built_in = get_path(base, BUILT_IN_TOOLS_PATH)
        if isinstance(built_in, dict):
            for key, raw in list(built_in.items()):
                if not isinstance(raw, dict):
                    continue
                try:
                    tool = Tool.from_json({"type": "system", **raw})
                except Exception:
                    continue  # Kept in the config as it is.
                system = tool.as_system()
                if system is None or system.system_tool_type != key:
                    continue
                agent._tools.append(tool)
                agent._loaded_system[id(tool)] = (tool, raw, _safe_json(tool))
                del built_in[key]
            if not built_in:
                delete_path(base, BUILT_IN_TOOLS_PATH)

        if isinstance(workflow, dict):
            agent._raw_workflow = workflow
        return agent

    @property
    def name(self) -> str:
        """The agent's name."""
        return self._name

    @property
    def workflow(self) -> typing.Optional[Workflow]:
        """
        The agent's workflow, or `None` if it has none. A loaded workflow is turned into a `Workflow` the first time
        it's read here, with its tool ids swapped for the `Tool` objects the agent knows, so it can be edited.
        """
        if self._workflow is None and self._raw_workflow is not None:
            self._workflow = Workflow.from_json(self._raw_workflow, tools_by_id=self._tools_by_id)
            self._raw_workflow = None
        return self._workflow

    def update(
        self,
        *,
        name: typing.Optional[str] = None,
        prompt: typing.Optional[str] = None,
        first_message: typing.Optional[str] = None,
        language: typing.Optional[str] = None,
        llm: typing.Optional[Llm] = None,
        temperature: typing.Optional[float] = None,
        voice_id: typing.Optional[str] = None,
        tts_model: typing.Optional[TtsConversationalModel] = None,
        tags: typing.Optional[typing.Sequence[str]] = None,
        tools: typing.Optional[typing.Sequence[Tool]] = None,
        tool_ids: typing.Optional[typing.Sequence[str]] = None,
        workflow: typing.Optional[Workflow] = None,
        conversation_config: typing.Optional[ConversationConfigInput] = None,
        platform_settings: typing.Optional[PlatformSettingsInput] = None,
    ) -> Agent:
        """
        Changes the agent. Options left as `None` are unchanged. `name`, the typed options, `tags`, `tools`,
        `tool_ids` and `workflow` replace what was there; `conversation_config` and `platform_settings` merge.
        """
        if name is not None:
            self._name = name
        typed = {
            "prompt": prompt,
            "first_message": first_message,
            "language": language,
            "llm": llm,
            "temperature": temperature,
            "voice_id": voice_id,
            "tts_model": tts_model,
        }
        for key, value in typed.items():
            if value is not None:
                self._typed[key] = value
        if tags is not None:
            self._tags = list(tags)
        if tools is not None:
            self._tools = list(tools)
            self._tool_list_given = True
        if tool_ids is not None:
            self._tool_ids = list(tool_ids)
            self._tool_list_given = True
        if workflow is not None:
            self._workflow = workflow
            self._raw_workflow = None
        if conversation_config is not None:
            self._raw_conversation_config.append(conversation_config)
        if platform_settings is not None:
            self._raw_platform_settings.append(platform_settings)
        return self

    def add_tool(self, tool: Tool) -> Agent:
        """Adds a tool the agent can use anywhere."""
        self._tools.append(tool)
        self._tool_list_given = True
        return self

    def tools(self) -> typing.List[Tool]:
        """
        Every webhook and client tool the agent and its workflow use, each once, in first-use order: the tools
        `agents.push()` creates or updates. System tools aren't included; they live inside the agent's config. Nor
        are tools of other kinds (such as `mcp`): they stay attached by the id the agent was loaded with, as pull
        leaves them.
        """
        seen: typing.Set[int] = set()
        result = []
        for tool in [*self._tools, *self._workflow_tools()]:
            if not _is_managed(tool) or id(tool) in seen:
                continue
            seen.add(id(tool))
            result.append(tool)
        return result

    @property
    def tool_ids(self) -> typing.List[str]:
        """The ids of existing tools attached as they are, which `agents.push()` doesn't manage."""
        return list(self._tool_ids)

    def validate(self, *, on_warning: typing.Optional[OnWarning] = None) -> None:
        """
        Checks everything that doesn't need tool ids: the tools, the workflow, the settings, and that no two tools
        share a name. CI can run this without an API key. `on_warning` is called for each non-fatal problem, such
        as an agent without a prompt.

        Raises
        ------
        AgentValidationError
            Listing every problem, if the agent is invalid.
        """
        self._assemble(None, on_warning)

    def build(
        self,
        *,
        tool_ids: typing.Optional[typing.Mapping[str, str]] = None,
        on_warning: typing.Optional[OnWarning] = None,
    ) -> AgentRequest:
        """
        Validates the agent and returns the keyword arguments `agents.create()` takes (`agents.update()` takes the
        same): `client.conversational_ai.agents.create(**agent.build(tool_ids=...))`. `tool_ids` maps the name of
        each webhook and client tool the agent uses to its id; `agents.push()` passes it after creating or updating
        the tools. Fields this SDK doesn't model are dropped by the generated client; `agents.push()` sends them
        too.

        Raises
        ------
        AgentValidationError
            Listing every problem, if the agent is invalid or a tool has no id.
        """
        config = self.to_json(tool_ids=tool_ids, on_warning=on_warning)
        request: AgentRequest = {
            "name": config["name"],
            "conversation_config": typing.cast(
                ConversationalConfig,
                construct_type(type_=ConversationalConfig, object_=config["conversation_config"]),
            ),
            "platform_settings": typing.cast(
                AgentPlatformSettingsRequestModel,
                construct_type(type_=AgentPlatformSettingsRequestModel, object_=config["platform_settings"]),
            ),
            "tags": list(config["tags"]),
        }
        if "workflow" in config:
            request["workflow"] = typing.cast(
                AgentWorkflowRequestModel,
                construct_type(type_=AgentWorkflowRequestModel, object_=config["workflow"]),
            )
        return request

    def to_json(
        self,
        *,
        tool_ids: typing.Optional[typing.Mapping[str, str]] = None,
        on_warning: typing.Optional[OnWarning] = None,
    ) -> WireDict:
        """
        The agent config in API format (snake_case keys, sorted at every level): the shape of a CLI
        `agent_configs/*.json` file. Validates like `build()`, and also needs every tool's id in `tool_ids`.
        """
        return self._assemble(dict(tool_ids or {}), on_warning)

    def __repr__(self) -> str:
        return f"Agent(name={self._name!r})"

    def _known_id(self, tool: Tool) -> typing.Optional[str]:
        """
        The id the agent was loaded with for `tool` (`tools_by_id`; a project passes its `tools.json` ids this way).
        Tools of kinds push doesn't manage stay attached by it.
        """
        ids = sorted(tool_id for tool_id, known in self._tools_by_id.items() if known is tool)
        return ids[0] if ids else None

    def _workflow_tools(self) -> typing.List[Tool]:
        if self._workflow is not None:
            return self._workflow.tools()
        return [self._tools_by_id[id] for id in raw_workflow_tool_ids(self._raw_workflow) if id in self._tools_by_id]

    def _assemble(
        self, tool_ids: typing.Optional[typing.Mapping[str, str]], on_warning: typing.Optional[OnWarning]
    ) -> WireDict:
        """
        Builds the API-format config. Without `tool_ids` (validation only), tools stand under placeholder ids and
        missing ids aren't reported.
        """
        issues: typing.List[AgentIssue] = []
        config = typing.cast(WireDict, deep_copy(self._base))

        def id_of(tool: Tool) -> str:
            # A kind push doesn't manage keeps the id it was loaded with; a missing one is reported as invalid_tool
            # below.
            if _is_managed(tool):
                known = None if tool_ids is None else tool_ids.get(tool.name)
            else:
                known = self._known_id(tool)
            return f"<tool:{tool.name}>" if known is None else known

        if self._name.strip() == "":
            issues.append(AgentIssue(code="missing_name", severity="error", message="The agent needs a name"))

        # Raw options first, so the typed ones win and can be checked against them.
        raw: WireDict = {}
        for settings in self._raw_conversation_config:
            try:
                deep_merge(raw, {"conversation_config": _raw_wire(settings, ConversationalConfig)})
            except Exception as err:
                issues.append(_invalid_config("conversation_config", err))
        for platform in self._raw_platform_settings:
            try:
                deep_merge(raw, {"platform_settings": _raw_wire(platform, AgentPlatformSettingsRequestModel)})
            except Exception as err:
                issues.append(_invalid_config("platform_settings", err))
        deep_merge(config, raw)

        for key, value in self._typed.items():
            try:
                path, wire = _typed_option(key, value)
            except Exception as err:
                issues.append(_invalid_config(key, err))
                continue
            if has_path(raw, path):
                issues.append(_conflict(key, path))
            set_path(config, path, wire)

        # Tools: every one validates, and no two different tools share a name.
        by_name: typing.Dict[str, Tool] = {}
        for tool in [*self._tools, *self._workflow_tools()]:
            other = by_name.get(tool.name)
            if other is not None and other is not tool:
                issues.append(
                    AgentIssue(
                        code="duplicate_tool_name",
                        severity="error",
                        message=f'Two different tools are named "{tool.name}"',
                        path=f"tools.{tool.name}",
                    )
                )
            if other is None:
                by_name[tool.name] = tool
                try:
                    tool.build_config()
                except Exception as err:
                    issues.append(
                        AgentIssue(code="invalid_tool", severity="error", message=str(err), path=f"tools.{tool.name}")
                    )
                # Push only creates and updates webhook and client tools; any other kind needs an id.
                if tool.kind != "system" and not _is_managed(tool) and self._known_id(tool) is None:
                    issues.append(
                        AgentIssue(
                            code="invalid_tool",
                            severity="error",
                            message=(
                                f'Tool "{tool.name}" has type "{_tool_type(tool)}", which push doesn\'t create or '
                                "update: load it with its id or attach it with tool_ids"
                            ),
                            path=f"tools.{tool.name}",
                        )
                    )

        # Webhook and client tools by their pushed ids, other kinds by the ids they were loaded with. An other-kind
        # tool whose id is already attached (such as a loaded mcp tool added back with add_tool() while its id is
        # still in tool_ids) isn't listed twice.
        attached: typing.List[str] = []
        for tool in self._tools:
            if tool.kind == "system":
                continue
            tool_id = id_of(tool)
            if not _is_managed(tool) and (tool_id in self._tool_ids or tool_id in attached):
                continue
            attached.append(tool_id)
        system = [tool for tool in self._tools if isinstance(tool, SystemTool)]
        if self._tool_list_given:
            if has_path(raw, TOOL_IDS_PATH):
                issues.append(_conflict("tools", TOOL_IDS_PATH))
            set_path(config, TOOL_IDS_PATH, _keep_order([*self._tool_ids, *attached], self._loaded_tool_ids))
        for system_tool in system:
            system_path = (*BUILT_IN_TOOLS_PATH, system_tool.system_tool_type)
            if has_path(raw, system_path):
                issues.append(_conflict("tools", system_path))
            loaded = self._loaded_system.get(id(system_tool))
            if loaded is not None and loaded[2] is not None and _safe_json(system_tool) == loaded[2]:
                set_path(config, system_path, deep_copy(loaded[1]))
                continue
            try:
                set_path(config, system_path, system_tool.to_json())
            except Exception:
                pass  # Reported as invalid_tool above.

        # Workflow: its own checks, plus tool nodes can only run webhook and client tools.
        if self._workflow is not None:
            wf = self._workflow
            for tool in wf.tools():
                if tool.kind == "system":
                    issues.append(
                        AgentIssue(
                            code="system_tool_in_workflow",
                            severity="error",
                            message=(
                                f"System tool \"{tool.name}\" can't be used in a workflow node; add it to the agent's "
                                "tools"
                            ),
                            path=f"workflow.tools.{tool.name}",
                        )
                    )
            ids = {tool.name: id_of(tool) for tool in wf.tools()}
            try:
                config["workflow"] = wf._to_wire(None, ids)
            except Exception as err:
                issues.append(AgentIssue(code="invalid_workflow", severity="error", message=str(err), path="workflow"))
        elif self._raw_workflow is not None:
            # Check the loaded graph without replacing the raw copy, which keeps fields this SDK doesn't model.
            try:
                Workflow.from_json(self._raw_workflow).build()
            except Exception as err:
                issues.append(AgentIssue(code="invalid_workflow", severity="error", message=str(err), path="workflow"))

            # Its managed tools may have new ids, e.g. when pushed as a new agent.
            def new_id(id: str) -> str:
                tool = self._tools_by_id.get(id)
                if tool is None or not _is_managed(tool) or tool_ids is None:
                    return id
                return tool_ids.get(tool.name, id)

            config["workflow"] = map_raw_workflow_tool_ids(deep_copy(self._raw_workflow), new_id)

        if tool_ids is not None:
            for tool in self.tools():
                if tool.name not in tool_ids:
                    issues.append(
                        AgentIssue(
                            code="unresolved_tool",
                            severity="error",
                            message=(
                                f'Tool "{tool.name}" has no id yet. Push the agent with agents.push(), or pass tool_ids'
                            ),
                            path=f"tools.{tool.name}",
                        )
                    )

        if not isinstance(get_path(config, PROMPT_PATH), str):
            issues.append(
                AgentIssue(
                    code="missing_prompt",
                    severity="warning",
                    message="The agent needs a prompt",
                    path=".".join(PROMPT_PATH),
                )
            )

        unique = _dedupe(issues)
        errors = [issue for issue in unique if issue.severity == "error"]
        if errors:
            raise AgentValidationError(self._name, errors)
        if on_warning is not None:
            for warning in unique:
                if warning.severity == "warning":
                    on_warning(warning)

        config["name"] = self._name
        if config.get("conversation_config") is None:
            config["conversation_config"] = {}
        if config.get("platform_settings") is None:
            config["platform_settings"] = {}
        config["tags"] = list(self._tags) if self._tags is not None else []
        return typing.cast(WireDict, canonical(config))


def _is_managed(tool: Tool) -> bool:
    """Whether push creates or updates `tool`: a webhook or client tool."""
    return tool.kind in ("webhook", "client")


def _tool_type(tool: Tool) -> str:
    """The type a tool's config gives, such as `"mcp"`."""
    if tool.kind != "other":
        return tool.kind
    try:
        return str(tool.to_json().get("type"))
    except Exception:
        return "other"


def map_raw_workflow_tool_ids(workflow: WireDict, fn: typing.Callable[[str], str]) -> WireDict:
    """Replaces the tool ids in an API-format workflow's tool nodes and subagents, in place."""
    nodes = workflow.get("nodes")
    for node in nodes.values() if isinstance(nodes, dict) else []:
        if not isinstance(node, dict):
            continue
        if isinstance(node.get("tools"), list):
            for locator in node["tools"]:
                if isinstance(locator, dict) and isinstance(locator.get("tool_id"), str):
                    locator["tool_id"] = fn(locator["tool_id"])
        if isinstance(node.get("additional_tool_ids"), list):
            node["additional_tool_ids"] = [fn(id) if isinstance(id, str) else id for id in node["additional_tool_ids"]]
    return workflow


def raw_workflow_tool_ids(workflow: typing.Optional[typing.Mapping[str, typing.Any]]) -> typing.List[str]:
    """The tool ids an API-format workflow's nodes use."""
    nodes = workflow.get("nodes") if isinstance(workflow, typing.Mapping) else None
    ids: typing.List[str] = []
    for node in nodes.values() if isinstance(nodes, dict) else []:
        if not isinstance(node, dict):
            continue
        for locator in node.get("tools") or []:
            if isinstance(locator, dict) and isinstance(locator.get("tool_id"), str):
                ids.append(locator["tool_id"])
        ids.extend(id for id in node.get("additional_tool_ids") or [] if isinstance(id, str))
    return ids


def _raw_wire(settings: typing.Any, model: typing.Type[pydantic.BaseModel]) -> WireDict:
    """A raw `conversation_config` or `platform_settings` option in wire format. Dicts are checked against `model`."""
    if isinstance(settings, pydantic.BaseModel):
        wire = to_wire(settings)
    elif isinstance(settings, typing.Mapping):
        wire = to_wire(dict(settings))
        parse_obj_as(model, wire)
    else:
        raise TypeError(f"expected {model.__name__} or a dict, not {type(settings).__name__}")
    if not isinstance(wire, dict):
        raise TypeError(f"expected {model.__name__} or a dict")
    return wire


def _safe_json(tool: Tool) -> typing.Optional[str]:
    try:
        return tool.to_json_string()
    except Exception:
        return None


def _keep_order(ids: typing.List[str], loaded: typing.List[str]) -> typing.List[str]:
    """`ids` with the ones in `loaded` first, in that order, then the rest as they are."""

    def rank(id: str) -> int:
        return loaded.index(id) if id in loaded else len(loaded)

    return sorted(ids, key=rank)


def _invalid_config(option: str, err: BaseException) -> AgentIssue:
    return AgentIssue(code="invalid_config", severity="error", message=f"Invalid {option}: {err}", path=option)


def _conflict(option: str, path: typing.Sequence[str]) -> AgentIssue:
    dotted = ".".join(path)
    return AgentIssue(
        code="option_conflict",
        severity="error",
        message=f'"{option}" and the raw config both set {dotted}; set it in one place',
        path=dotted,
    )


def _dedupe(issues: typing.List[AgentIssue]) -> typing.List[AgentIssue]:
    seen: typing.Set[typing.Tuple[str, typing.Optional[str], str]] = set()
    unique = []
    for issue in issues:
        key = (issue.code, issue.path, issue.message)
        if key not in seen:
            seen.add(key)
            unique.append(issue)
    return unique
