import dataclasses
import typing

AgentIssueCode = typing.Literal[
    "missing_name",
    "missing_prompt",
    "duplicate_tool_name",
    "invalid_tool",
    "invalid_workflow",
    "invalid_config",
    "option_conflict",
    "unresolved_tool",
    "system_tool_in_workflow",
]


@dataclasses.dataclass(frozen=True)
class AgentIssue:
    """A problem found in an agent. Errors stop `validate()` and `build()`; warnings go to their `on_warning`."""

    code: AgentIssueCode
    severity: typing.Literal["error", "warning"]
    message: str
    path: typing.Optional[str] = None
    """Where the problem is, for example `"tools.get_order"` or `"workflow"`."""


class AgentValidationError(Exception):
    """Raised by `Agent.validate()` and `Agent.build()` when the agent is invalid. Lists every problem found."""

    def __init__(self, name: str, issues: typing.List[AgentIssue]) -> None:
        super().__init__(f'Invalid agent "{name}":\n' + "\n".join(f"  - {issue.message}" for issue in issues))
        self.issues = issues


ToolPushAction = typing.Literal["created", "updated", "unchanged", "detached"]
"""What `agents.push()` did to one tool. `"detached"`: the agent used it before and no longer does; it isn't
deleted."""


@dataclasses.dataclass(frozen=True)
class ToolPushResult:
    """What `agents.push()` did to one tool."""

    id: str
    action: ToolPushAction


@dataclasses.dataclass
class AgentPushResult:
    """What `agents.push()` did."""

    agent_id: str
    action: typing.Literal["created", "updated"]
    """What happened to the agent: created, or updated in place."""
    tools: typing.Dict[str, ToolPushResult]
    """Each tool `push` touched, by name."""


@dataclasses.dataclass
class PartialAgentPushResult:
    """What `agents.push()` wrote before a request failed. `agent_id` and `action` are set once the agent is."""

    tools: typing.Dict[str, ToolPushResult] = dataclasses.field(default_factory=dict)
    agent_id: typing.Optional[str] = None
    action: typing.Optional[typing.Literal["created", "updated"]] = None


class AgentPushError(Exception):
    """
    Raised by `agents.push()` when an API call fails after it started writing. `result` lists what was written
    before the failure, so nothing created goes unreported; with a project, those ids are saved to it too. The
    failed call's exception is `cause` (and `__cause__`).
    """

    def __init__(self, step: str, result: PartialAgentPushResult, cause: BaseException) -> None:
        super().__init__(f"{step}: {cause}")
        self.step = step
        """Which step failed, for example `Couldn't create tool "get_order"`."""
        self.result = result
        self.cause = cause
