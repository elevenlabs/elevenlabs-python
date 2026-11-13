import dataclasses
import typing

ToolIssueCode = typing.Literal[
    "missing_url",
    "missing_path_param",
    "unknown_path_param",
    "param_not_literal",
    "body_not_object",
    "body_not_allowed",
    "missing_body",
    "duplicate_param",
    "conflicting_value_source",
    "omitted_required",
    "invalid_choices",
    "allowed_values_needs_description",
    "constant_type_mismatch",
    "unknown_required_property",
    "missing_array_items",
    "duplicate_header",
    "invalid_destination",
    "no_transfers",
    "invalid_option",
    "missing_value_source",
    "unknown_tool_type",
]


@dataclasses.dataclass(frozen=True)
class ToolIssue:
    """A problem found in a tool. Errors stop `build()`; warnings are passed to its `on_warning` callback."""

    code: ToolIssueCode
    severity: typing.Literal["error", "warning"]
    message: str
    path: typing.Optional[str] = None
    """Where the problem is, for example `"body.reason"` or `"path_params.order_id"`."""


class ToolValidationError(Exception):
    """Raised by a tool's `build()` when the tool is invalid. Lists every problem found."""

    def __init__(self, name: str, issues: typing.List[ToolIssue]) -> None:
        super().__init__(f'Invalid tool "{name}":\n' + "\n".join(f"  - {issue.message}" for issue in issues))
        self.issues = issues


def error(code: ToolIssueCode, path: typing.Optional[str], message: str) -> ToolIssue:
    return ToolIssue(code=code, severity="error", message=message, path=path)
