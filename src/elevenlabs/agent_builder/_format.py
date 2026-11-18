import json
import re
import typing

from ._wire import canonical

_UNSAFE = re.compile(r'[/\\:*?"<>|]')


def format_index(value: typing.Any) -> str:
    """The CLI's file format: 4-space indent, no trailing newline (serde_json's pretty printer)."""
    return json.dumps(value, indent=4, ensure_ascii=False)


def format_config(value: typing.Any) -> str:
    """Config files: like `format_index()`, with keys sorted at every level, as the CLI writes them."""
    return json.dumps(canonical(value), indent=4, ensure_ascii=False)


def sanitize_filename(name: str) -> str:
    """The CLI's `sanitize_filename`: a filesystem-safe file stem for an agent or tool name."""
    trimmed = name.strip()
    if trimmed == "":
        return "unnamed"
    sanitized = "".join("-" if _UNSAFE.match(c) or c.isspace() else c for c in trimmed)
    while "--" in sanitized:
        sanitized = sanitized.replace("--", "-")
    stripped = sanitized.strip(".-")
    if stripped == "":
        return "unnamed"
    result = f"_{stripped}" if trimmed.startswith(".") else stripped
    return result[:100]


def unique_path(dir: str, name: str, taken: typing.Collection[str]) -> str:
    """The CLI's `generate_unique_filename`: `<dir>/<name>.json`, then `-1`, `-2`... while the path is taken."""
    stem = sanitize_filename(name)
    candidate = f"{dir}/{stem}.json"
    n = 1
    while candidate in taken:
        candidate = f"{dir}/{stem}-{n}.json"
        n += 1
    return candidate


def normalize_path(path: str) -> str:
    """A project-relative path in one canonical spelling: forward slashes, no `./` or empty segments."""
    return "/".join(part for part in path.replace("\\", "/").split("/") if part not in ("", "."))
