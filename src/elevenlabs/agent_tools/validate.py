import typing

from .errors import ToolIssue, error
from .schema import Schema, SchemaKind


def check_schema(schema: Schema, path: str, is_property: bool, issues: typing.List[ToolIssue]) -> None:
    """
    Checks a schema and everything under it. `path` names it in messages, for example `"body.reason"`.
    `is_property` is whether it's a property or a param, so `omit()` needs it to be optional.
    """
    s = schema._state
    sources = sum(
        [
            s.description is not None,
            s.dynamic_variable is not None,
            s.has_constant,
            s.system_provided,
            s.omitted,
        ]
    )
    if sources > 1:
        issues.append(
            error(
                "conflicting_value_source",
                path,
                f'"{path}" sets more than one of describe(), from_variable(), constant(), system_provided() and omit()',
            )
        )
    if s.omitted and is_property and not s.optional:
        issues.append(error("omitted_required", path, f'"{path}" uses omit(), so it must be optional()'))
    if s.choices is not None and s.kind != "string":
        issues.append(error("invalid_choices", path, f'"{path}" uses choices(), which only applies to strings'))
    if s.allowed_from is not None and s.description is None:
        issues.append(
            error(
                "allowed_values_needs_description",
                path,
                f'"{path}" uses allowed_from(), which needs describe() so the LLM provides the value',
            )
        )
    if s.has_constant and not _matches_kind(s.kind, s.constant_value):
        issues.append(error("constant_type_mismatch", path, f'"{path}" has a constant that isn\'t a {s.kind}'))
    elif s.has_constant and s.constant_value == "":
        issues.append(
            error("constant_type_mismatch", path, f'"{path}" can\'t have "" as a constant: the API reads it as unset')
        )
    # The API rejects a literal with no value source wherever it appears, response schemas included.
    if sources == 0 and is_literal(s.kind):
        issues.append(
            error(
                "missing_value_source",
                path,
                f'"{path}" needs one of describe(), from_variable(), constant(), system_provided() or omit()',
            )
        )

    if s.kind == "object":
        names = [name for name, _ in s.properties]
        for group in (*s.any_of, *s.all_of):
            for name in group:
                if name not in names:
                    issues.append(
                        error(
                            "unknown_required_property",
                            path,
                            f'"{path}" requires "{name}" in require_any_of()/require_all_of(), but has no such property',
                        )
                    )
        for name, child in s.properties:
            check_schema(child, f"{path}.{name}", True, issues)
    if s.kind == "array":
        if s.items is None:
            issues.append(error("missing_array_items", path, f'Array "{path}" has no items schema'))
        else:
            check_schema(s.items, f"{path}[]", False, issues)


def is_literal(kind: SchemaKind) -> bool:
    return kind not in ("object", "array")


def _matches_kind(kind: SchemaKind, value: typing.Any) -> bool:
    # JSON has one number type: 3.0 is an integer, as in JavaScript. `bool` is an `int` in Python, so rule it out.
    if kind == "string":
        return isinstance(value, str)
    if kind == "integer":
        return (isinstance(value, int) and not isinstance(value, bool)) or (
            isinstance(value, float) and value.is_integer()
        )
    if kind == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "object":
        return isinstance(value, dict)
    return isinstance(value, list)
