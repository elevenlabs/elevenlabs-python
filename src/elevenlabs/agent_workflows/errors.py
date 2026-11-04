import dataclasses
import typing

WorkflowIssueCode = typing.Literal[
    "duplicate_node_id",
    "unknown_node",
    "unknown_edge",
    "invalid_option",
    "edge_into_start",
    "end_has_outgoing_edges",
    "tool_edge_needs_result",
    "result_edge_needs_tool",
    "cannot_remove_start",
    "missing_insert_result",
    "unreachable_node",
    "unknown_node_type",
]


@dataclasses.dataclass(frozen=True)
class WorkflowIssue:
    """A problem found in a workflow. Errors stop `build()`; warnings are passed to its `on_warning` callback."""

    code: WorkflowIssueCode
    severity: typing.Literal["error", "warning"]
    message: str
    node_id: typing.Optional[str] = None


class WorkflowValidationError(Exception):
    """Raised by `Workflow.build()` when the workflow is invalid. Lists every problem found."""

    def __init__(self, issues: typing.List[WorkflowIssue]) -> None:
        super().__init__("Invalid workflow:\n" + "\n".join(f"  - {issue.message}" for issue in issues))
        self.issues = issues
