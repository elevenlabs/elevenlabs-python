import errno
import json
import os
import stat
import typing
import unicodedata

from ._format import normalize_path

# File access for AgentProject.

AGENTS_FILE = "agents.json"
TOOLS_FILE = "tools.json"
AGENT_CONFIGS_DIR = "agent_configs"
TOOL_CONFIGS_DIR = "tool_configs"


class AgentProjectError(Exception):
    """Raised when a project's files can't be read: a missing or malformed file, or a format the SDK can't read yet."""


def read_project(dir: str) -> typing.Tuple[typing.Dict[str, str], typing.List[str]]:
    """
    Reads the index files and every config they list. Also returns the files already in the config directories,
    which new files mustn't overwrite.
    """
    root = os.path.realpath(dir)
    files: typing.Dict[str, str] = {}
    for index in (AGENTS_FILE, TOOLS_FILE):
        text = _read_if_exists(_resolve_in_project(root, index))
        if text is None:
            continue
        files[index] = text
        try:
            parsed = json.loads(text)
        except ValueError:
            continue  # AgentProject reports it, with the parse error.
        if not isinstance(parsed, dict):
            continue
        configs: typing.List[typing.Any] = []
        for entry in _entries(parsed, "agents"):
            configs.append(entry.get("config"))
            branches = entry.get("branches")
            if isinstance(branches, dict):
                configs.extend(
                    branch.get("config") if isinstance(branch, dict) else None for branch in branches.values()
                )
        configs.extend(entry.get("config") for entry in _entries(parsed, "tools"))
        for config in configs:
            if not isinstance(config, str):
                raise AgentProjectError(f'{index} has an entry without a "config" path')
            content = _read_if_exists(_resolve_in_project(root, config))
            if content is not None:
                files[normalize_path(config)] = content
    taken: typing.List[str] = []
    for sub in (AGENT_CONFIGS_DIR, TOOL_CONFIGS_DIR):
        try:
            names = os.listdir(os.path.join(root, sub))
        except OSError:
            continue  # No directory yet.
        taken.extend(f"{sub}/{name}" for name in names)
    return files, taken


def write_project_files(dir: str, files: typing.Sequence[typing.Tuple[str, str]]) -> None:
    """Writes each file owner-only, creating directories as needed, never through a symlink or outside the project."""
    root = os.path.realpath(dir)
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    for path, text in files:
        target = _resolve_in_project(root, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        if no_follow == 0:
            try:
                is_link = stat.S_ISLNK(os.lstat(target).st_mode)
            except FileNotFoundError:
                is_link = False
            if is_link:
                raise AgentProjectError(f"Refusing to write {path}: it's a symlink")
        try:
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | no_follow, 0o600)
        except OSError as err:
            if err.errno == errno.ELOOP:
                raise AgentProjectError(f"Refusing to write {path}: it's a symlink") from err
            raise
        try:
            try:
                os.fchmod(fd, 0o600)
            except (AttributeError, OSError):
                pass  # Not on every platform.
            data = text.encode("utf-8")
            written = 0
            while written < len(data):
                written += os.write(fd, data[written:])
        finally:
            os.close(fd)


def _resolve_in_project(root: str, path: str) -> str:
    """
    The CLI's `resolve_in_project`: the absolute path for a project-relative one, refusing anything that escapes
    the project, including through a symlinked directory.
    """
    if path.strip() == "" or any(unicodedata.category(c) == "Cc" for c in path):
        raise AgentProjectError(f"Invalid config path {json.dumps(path)}")
    candidate = os.path.normpath(os.path.join(root, path))

    def inside(p: str) -> bool:
        return p == root or p.startswith(root.rstrip(os.sep) + os.sep)

    if not inside(candidate):
        raise AgentProjectError(f"Config path {path} is outside the project")
    # With symlinks resolved, as far as the path exists, it must still be inside.
    if not inside(os.path.realpath(candidate)):
        raise AgentProjectError(f"Config path {path} leads outside the project through a symlink")
    return candidate


def _read_if_exists(path: str) -> typing.Optional[str]:
    try:
        # newline="" keeps the file's line endings, so an untouched file is given back byte for byte.
        with open(path, "r", encoding="utf-8", newline="") as file:
            return file.read()
    except FileNotFoundError:
        return None


def _entries(index: typing.Dict[str, typing.Any], key: str) -> typing.List[typing.Dict[str, typing.Any]]:
    entries = index.get(key)
    return [entry for entry in entries if isinstance(entry, dict)] if isinstance(entries, list) else []
