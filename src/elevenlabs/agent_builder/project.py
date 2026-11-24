from __future__ import annotations

import dataclasses
import json
import os
import re
import typing

from ..agent_tools.tool import Tool
from ._definition import tool_definition
from ._format import format_config, format_index, normalize_path, unique_path
from ._fs import (
    AGENT_CONFIGS_DIR,
    AGENTS_FILE,
    TOOL_CONFIGS_DIR,
    TOOLS_FILE,
    AgentProjectError,
    read_project,
    write_project_files,
)
from ._wire import WireDict
from .agent import Agent

__all__ = ["AGENTS_FILE", "AGENT_CONFIGS_DIR", "AgentProject", "AgentProjectError", "TOOLS_FILE", "TOOL_CONFIGS_DIR"]

_JSON_FILE = re.compile(r"\.json$", re.IGNORECASE)

# Entry fields in the order the CLI writes them. Unset fields are left out.
_AGENT_ENTRY_FIELDS = ("config", "id", "branch_id", "version_id", "branches")
_TOOL_ENTRY_FIELDS = ("type", "config", "id")


@dataclasses.dataclass(eq=False)
class _AgentSlot:
    # One entry in agents.json: `config`, `id`, `branch_id`, `version_id`, `branches`.
    entry: typing.Dict[str, typing.Any]
    agent: Agent


@dataclasses.dataclass(eq=False)
class _ToolSlot:
    # One entry in tools.json: `type`, `config`, `id`.
    entry: typing.Dict[str, typing.Any]
    tool: Tool
    # The config as loaded, in API format, sent as-is while the tool is unchanged so unmodeled fields survive.
    raw: typing.Optional[WireDict] = None
    # The tool's definition as loaded (see `tool_definition`), to tell whether it was edited since.
    baseline: typing.Optional[str] = None


class AgentProject:
    """
    An agents-as-code project in the ElevenLabs CLI's layout: `agents.json` and `tools.json` list the agents and
    tools with their ids, and each one's config sits in `agent_configs/` or `tool_configs/` in API format. A project
    made by `elevenlabs agents init` / `pull` works here, and one written here works with the CLI.

    Pass it to `agents.push(agent, project=project)` and `agents.pull(agent_id, project=project)`: the project records
    which agent and tools on the server each definition is, so pushing again updates them instead of making copies.

    Examples
    --------
    from elevenlabs.agent_builder import AgentProject

    project = AgentProject.open(".")
    agent = project.agent("Support line")
    agent.update(prompt="...")
    client.conversational_ai.agents.push(agent, project=project)
    """

    def __init__(
        self,
        files: typing.Mapping[str, str],
        dir: typing.Optional[str] = None,
        taken: typing.Iterable[str] = (),
    ) -> None:
        # Use `from_files()` or `open()`.
        self.dir = dir
        """The directory the project was opened from, if any. `save()` writes there."""
        self._files: typing.Dict[str, str] = {normalize_path(path): text for path, text in files.items()}
        self._agents: typing.List[_AgentSlot] = []
        self._tools: typing.List[_ToolSlot] = []
        # Paths written since loading, with their new contents.
        self._changed: typing.Dict[str, str] = {}
        # Paths in use on disk, so new files don't overwrite one the project doesn't list.
        self._taken: typing.Set[str] = {*self._files, *(normalize_path(path) for path in taken)}
        self._load()

    @staticmethod
    def from_files(files: typing.Mapping[str, str]) -> AgentProject:
        """
        A project from file contents, keyed by path relative to the project root. Only `agents.json`, `tools.json`
        and the config files they list are read. Missing index files mean an empty project.
        """
        return AgentProject(files)

    @staticmethod
    def open(dir: typing.Union[str, os.PathLike]) -> AgentProject:  # type: ignore[type-arg]
        """
        Reads the project in `dir`. A directory without `agents.json` and `tools.json` opens as an empty project,
        and `save()` creates them.
        """
        path = os.fspath(dir)
        files, taken = read_project(path)
        return AgentProject(files, path, taken)

    def agents(self) -> typing.List[Agent]:
        """Every agent in the project, in `agents.json` order."""
        return [slot.agent for slot in self._agents]

    def agent(self, name: str) -> Agent:
        """
        The agent named `name`. The same object every time, so edits to it are what
        `agents.push(agent, project=project)` sends.

        Raises
        ------
        AgentProjectError
            If no agent, or more than one, has that name.
        """
        matches = [slot for slot in self._agents if slot.agent.name == name]
        if len(matches) != 1:
            raise AgentProjectError(
                f'No agent named "{name}" in {AGENTS_FILE}'
                if not matches
                else f'{len(matches)} agents in {AGENTS_FILE} are named "{name}"'
            )
        return matches[0].agent

    def tools(self) -> typing.List[Tool]:
        """Every tool in `tools.json`, in order."""
        return [slot.tool for slot in self._tools]

    def agent_id(self, agent: Agent) -> typing.Optional[str]:
        """The id `agents.json` records for this agent, if it was pushed or pulled."""
        slot = self._agent_slot(agent)
        return None if slot is None else slot.entry.get("id")

    def tool_id(self, tool: Tool) -> typing.Optional[str]:
        """The id `tools.json` records for this tool, if it was pushed or pulled."""
        slot = self._tool_slot(tool)
        return None if slot is None else slot.entry.get("id")

    def to_files(self) -> typing.Dict[str, str]:
        """
        The project's files, keyed by path: the index files and every config they list, with what push and pull
        wrote since loading. Files nothing changed keep their exact text.
        """
        agents_text = _first(self._changed.get(AGENTS_FILE), self._files.get(AGENTS_FILE))
        tools_text = _first(self._changed.get(TOOLS_FILE), self._files.get(TOOLS_FILE))
        files = {
            AGENTS_FILE: self._agents_index() if agents_text is None else agents_text,
            TOOLS_FILE: self._tools_index() if tools_text is None else tools_text,
        }
        paths = [
            *(slot.entry["config"] for slot in self._agents),
            *(
                branch["config"]
                for slot in self._agents
                for branch in (slot.entry.get("branches") or {}).values()
                if isinstance(branch, dict) and isinstance(branch.get("config"), str)
            ),
            *(slot.entry["config"] for slot in self._tools),
        ]
        for path in paths:
            key = normalize_path(path)
            text = self._changed.get(key, self._files.get(key))
            if text is not None:
                files[path] = text
        return files

    def changed_files(self) -> typing.List[str]:
        """The paths push and pull changed since the project was loaded or last saved."""
        return list(self._changed)

    def save(self) -> typing.List[str]:
        """
        Writes the files push and pull changed to the project's directory, owner-only, and returns their paths.
        `agents.push()` and `agents.pull()` call this themselves for a project opened with `open()`.
        """
        if self.dir is None:
            raise AgentProjectError("This project wasn't opened from a directory; use to_files() instead")
        written = list(self._changed.items())
        if not written:
            return []
        write_project_files(self.dir, written)
        for path, text in written:
            self._files[path] = text
        self._changed.clear()
        return [path for path, _ in written]

    # Used by agents.push() and agents.pull().

    def _agent_slot(self, agent: Agent) -> typing.Optional[_AgentSlot]:
        """The entry for an agent: the one it was loaded from, else the only one with its name."""
        for slot in self._agents:
            if slot.agent is agent:
                return slot
        return _single([slot for slot in self._agents if slot.agent.name == agent.name], AGENTS_FILE, agent.name)

    def _tool_slot(self, tool: Tool) -> typing.Optional[_ToolSlot]:
        """The entry for a tool: the one it was loaded from, else the only one with its name."""
        for slot in self._tools:
            if slot.tool is tool:
                return slot
        return _single([slot for slot in self._tools if slot.tool.name == tool.name], TOOLS_FILE, tool.name)

    def _unchanged_raw(self, tool: Tool) -> typing.Optional[WireDict]:
        """
        The loaded config to send for a tool whose definition matches its project entry (the loaded object, or one
        rebuilt in code with the same name), so fields this SDK doesn't model survive.
        """
        slot = self._tool_slot(tool)
        if slot is None or slot.raw is None or slot.baseline is None:
            return None
        return slot.raw if tool_definition(tool) == slot.baseline else None

    def _record_tool(
        self,
        tool: Tool,
        id: str,
        config: WireDict,
        match_by: typing.Literal["definition", "id"] = "definition",
    ) -> None:
        """
        Records a tool's id and the config now on the server, adding an entry if it's new. Push finds the entry by
        definition; pull, by id.
        """
        slot = (
            next((s for s in self._tools if s.entry.get("id") == id), None)
            if match_by == "id"
            else self._tool_slot(tool)
        )
        if slot is None:
            path = unique_path(TOOL_CONFIGS_DIR, tool.name, self._taken)
            self._taken.add(path)
            slot = _ToolSlot(entry={"type": tool.kind, "config": path}, tool=tool)
            self._tools.append(slot)
        slot.tool = tool
        slot.entry["id"] = id
        slot.entry["type"] = tool.kind
        slot.raw = config
        slot.baseline = tool_definition(tool)
        self._write(slot.entry["config"], format_config(config))
        self._write(TOOLS_FILE, self._tools_index())

    def _record_agent(
        self,
        agent: Agent,
        id: str,
        config: WireDict,
        *,
        branch_id: typing.Optional[str] = None,
        version_id: typing.Optional[str] = None,
        match_by: typing.Literal["definition", "id"] = "definition",
    ) -> None:
        """Records an agent's id and its config, adding an entry if it's new. Push matches like `_record_tool`."""
        slot = (
            next((s for s in self._agents if s.entry.get("id") == id), None)
            if match_by == "id"
            else self._agent_slot(agent)
        )
        if slot is None:
            path = unique_path(AGENT_CONFIGS_DIR, agent.name, self._taken)
            self._taken.add(path)
            slot = _AgentSlot(entry={"config": path}, agent=agent)
            self._agents.append(slot)
        slot.entry["id"] = id
        branch = (
            None
            if branch_id is None
            else next(
                (
                    b
                    for b in (slot.entry.get("branches") or {}).values()
                    if isinstance(b, dict) and b.get("branch_id") == branch_id
                ),
                None,
            )
        )
        # A branch has its own file; the slot's agent is the main branch's, which a branch must not replace.
        if branch is None:
            slot.agent = agent
        # Like the CLI: the version the server reports, on the branch entry it belongs to.
        if version_id is not None:
            (slot.entry if branch is None else branch)["version_id"] = version_id
        path = slot.entry["config"]
        if branch is not None:
            # _check_branch made sure it has one; never fall back to the main branch's file.
            if not _has_config(branch):
                self._check_branch_of(None, agent.name, typing.cast(str, branch_id))
            path = branch["config"]
        self._write(path, format_config(config))
        self._write(AGENTS_FILE, self._agents_index())

    def _check_branch(self, agent: Agent, branch_id: typing.Optional[str]) -> None:
        """
        Rejects a branch the project has no file for, before anything is written: its settings would otherwise
        land in the main branch's file, and a later CLI push would send them to the main branch.
        """
        if branch_id is not None:
            self._check_branch_of(self._agent_slot(agent), agent.name, branch_id)

    def _check_branch_by_id(self, agent_id: str, branch_id: typing.Optional[str]) -> None:
        """`_check_branch` for `pull`, which finds the agent by id."""
        if branch_id is not None:
            slot = next((s for s in self._agents if s.entry.get("id") == agent_id), None)
            self._check_branch_of(slot, agent_id, branch_id)

    def _check_branch_of(self, slot: typing.Optional[_AgentSlot], label: str, branch_id: str) -> None:
        if slot is not None and slot.entry.get("branch_id") == branch_id:
            return
        branches = (slot.entry.get("branches") if slot is not None else None) or {}
        # The first branch entry with that id is the one recorded; it needs its own file.
        branch = next((b for b in branches.values() if isinstance(b, dict) and b.get("branch_id") == branch_id), None)
        if branch is None or not _has_config(branch):
            raise AgentProjectError(
                f'Branch {branch_id} of "{label}" has no config file in {AGENTS_FILE}. Add it under "branches" '
                "(the CLI's `agents pull --all-branches` does), or push the main branch"
            )

    def _write(self, path: str, text: str) -> None:
        key = normalize_path(path)
        if self._files.get(key) == text:
            self._changed.pop(key, None)
        else:
            self._changed[key] = text

    def _load(self) -> None:
        agents_index = self._read_index(AGENTS_FILE, "agents")
        tools_index = self._read_index(TOOLS_FILE, "tools")

        by_id: typing.Dict[str, Tool] = {}
        for entry in tools_index:
            raw = self._read_config(entry.get("config"), TOOLS_FILE)
            try:
                tool = Tool.from_json(raw)
            except Exception as err:
                raise AgentProjectError(f"{entry['config']} isn't a valid tool config: {err}") from err
            self._tools.append(_ToolSlot(entry=dict(entry), tool=tool, raw=raw, baseline=tool_definition(tool)))
            if isinstance(entry.get("id"), str):
                by_id[entry["id"]] = tool
        for entry in agents_index:
            raw = self._read_config(entry.get("config"), AGENTS_FILE)
            self._agents.append(_AgentSlot(entry=dict(entry), agent=Agent.from_json(raw, tools_by_id=by_id)))

    def _read_index(self, path: str, key: str) -> typing.List[typing.Dict[str, typing.Any]]:
        text = self._files.get(path)
        if text is None:
            return []
        try:
            parsed = json.loads(text)
        except ValueError as err:
            raise AgentProjectError(f"{path} isn't valid JSON: {err}") from err
        entries = parsed.get(key) if isinstance(parsed, dict) else None
        if entries is None:
            return []
        if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
            raise AgentProjectError(f'{path} must hold a "{key}" list of entries')
        return entries

    def _read_config(self, path: typing.Any, index: str) -> WireDict:
        if not isinstance(path, str):
            raise AgentProjectError(f'{index} has an entry without a "config" path')
        if not _JSON_FILE.search(path):
            raise AgentProjectError(
                f"{index} points at {path}: only JSON config files are supported yet (YAML and TOML aren't)"
            )
        text = self._files.get(normalize_path(path))
        if text is None:
            raise AgentProjectError(f"{index} points at {path}, which doesn't exist")
        try:
            parsed = json.loads(text)
        except ValueError as err:
            raise AgentProjectError(f"{path} isn't valid JSON: {err}") from err
        if not isinstance(parsed, dict):
            raise AgentProjectError(f"{path} must hold a JSON object")
        return parsed

    def _agents_index(self) -> str:
        return format_index({"agents": [_ordered(slot.entry, _AGENT_ENTRY_FIELDS) for slot in self._agents]})

    def _tools_index(self) -> str:
        return format_index({"tools": [_ordered(slot.entry, _TOOL_ENTRY_FIELDS) for slot in self._tools]})


_Slot = typing.TypeVar("_Slot")


def _single(matches: typing.List[_Slot], index: str, name: str) -> typing.Optional[_Slot]:
    if len(matches) > 1:
        raise AgentProjectError(f'{len(matches)} entries in {index} are named "{name}"; push the loaded one')
    return matches[0] if matches else None


def _first(*texts: typing.Optional[str]) -> typing.Optional[str]:
    return next((text for text in texts if text is not None), None)


def _ordered(entry: typing.Mapping[str, typing.Any], fields: typing.Sequence[str]) -> typing.Dict[str, typing.Any]:
    """The entry's fields the CLI writes, in its order, leaving out unset ones."""
    return {field: entry[field] for field in fields if field in entry}


def _has_config(branch: typing.Mapping[str, typing.Any]) -> bool:
    """Whether a branch entry names its own config file."""
    config = branch.get("config")
    return isinstance(config, str) and config != ""
