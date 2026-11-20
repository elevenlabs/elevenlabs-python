import json
import os
import pathlib
import stat
import typing

import pytest
from .fake_server import FakeServer

from elevenlabs.agent_builder import Agent, AgentProject, AgentProjectError
from elevenlabs.agent_builder._format import format_config, format_index, sanitize_filename, unique_path
from elevenlabs.agent_tools import Tool

# A project in the CLI's layout, shared by every SDK and copied from the reference SDK (elevenlabs-js,
# docs/agents-as-code/fixtures); see agent-spec.md there, "Fixtures".
CLI_PROJECT = pathlib.Path(__file__).parent / "fixtures" / "project" / "cli-graph"


def read_json(path: str) -> typing.Dict[str, typing.Any]:
    return json.loads((CLI_PROJECT / path).read_text(encoding="utf-8"))


def read_tree(dir: pathlib.Path) -> typing.Dict[str, str]:
    return {
        path.relative_to(dir).as_posix(): path.read_bytes().decode("utf-8")
        for path in sorted(dir.rglob("*"))
        if path.is_file()
    }


class TestAgentProject:
    def test_loads_a_cli_project_tools_by_id_agents_with_tool_objects_unknown_ids_kept(self) -> None:
        project = AgentProject.from_files(read_tree(CLI_PROJECT))
        assert [agent.name for agent in project.agents()] == ["Support", "Billing"]
        assert [tool.name for tool in project.tools()] == ["lookup_order", "issue_refund"]

        support = project.agent("Support")
        assert [tool.name for tool in support.tools()] == ["lookup_order"]
        assert support.tool_ids == ["tool_from_dashboard"]
        assert project.agent_id(support) == "agent_support"
        assert project.tool_id(support.tools()[0]) == "tool_lookup"

    def test_gives_back_every_file_unchanged_when_nothing_was_pushed_branch_configs_included(self) -> None:
        files = read_tree(CLI_PROJECT)
        assert AgentProject.from_files(files).to_files() == files

    def test_round_trips_the_cli_agent_config_to_its_sorted_form(self) -> None:
        project = AgentProject.from_files(read_tree(CLI_PROJECT))
        support = project.agent("Support")
        config = support.to_json(tool_ids={"lookup_order": "tool_lookup"})
        assert format_config(config) == format_config(read_json("agent_configs/support.json"))

    def test_reports_missing_malformed_and_not_yet_supported_files_clearly(self) -> None:
        def index(config: str) -> str:
            return json.dumps({"agents": [{"config": config}]})

        with pytest.raises(AgentProjectError, match="only JSON config files are supported yet"):
            AgentProject.from_files({"agents.json": index("agent_configs/a.yaml")})
        with pytest.raises(AgentProjectError, match="points at agent_configs/a.json, which doesn't exist"):
            AgentProject.from_files({"agents.json": index("agent_configs/a.json")})
        with pytest.raises(AgentProjectError):
            AgentProject.from_files({"agents.json": "{"})
        with pytest.raises(AgentProjectError, match='No agent named "Nope"'):
            AgentProject.from_files({}).agent("Nope")

    def test_names_new_files_like_the_cli(self) -> None:
        assert sanitize_filename("  Support line / EU ") == "Support-line-EU"
        assert sanitize_filename(".hidden") == "_hidden"
        assert sanitize_filename("...") == "unnamed"
        assert sanitize_filename("a" * 120) == "a" * 100
        assert unique_path("agent_configs", "A", {"agent_configs/A.json", "agent_configs/A-1.json"}) == (
            "agent_configs/A-2.json"
        )

    def test_save_needs_a_directory(self) -> None:
        with pytest.raises(AgentProjectError, match="to_files"):
            AgentProject.from_files({}).save()


class TestAgentProjectOnDisk:
    def test_opens_an_empty_directory_and_push_writes_the_cli_layout_owner_only(self, tmp_path: pathlib.Path) -> None:
        (tmp_path / "agent_configs").mkdir()
        (tmp_path / "agent_configs" / "A.json").write_text("not ours")  # a file the project doesn't list
        project = AgentProject.open(tmp_path)
        server = FakeServer()
        agent = Agent("A", prompt="p", tools=[Tool.client("ping", "Ping the app")])

        server.client().conversational_ai.agents.push(agent, project=project)

        files = read_tree(tmp_path)
        assert sorted(files) == [
            "agent_configs/A-1.json",
            "agent_configs/A.json",
            "agents.json",
            "tool_configs/ping.json",
            "tools.json",
        ]
        assert files["agent_configs/A.json"] == "not ours"
        assert files["tool_configs/ping.json"] == (
            '{\n    "description": "Ping the app",\n    "name": "ping",\n    "type": "client"\n}'
        )
        if os.name == "posix":
            assert stat.S_IMODE((tmp_path / "agents.json").stat().st_mode) == 0o600
        assert project.changed_files() == []

        reopened = AgentProject.open(str(tmp_path))
        assert reopened.agent_id(reopened.agent("A")) == project.agent_id(agent)

    def test_keeps_line_endings_of_files_it_did_not_change(self, tmp_path: pathlib.Path) -> None:
        text = '{\r\n    "agents": []\r\n}'
        (tmp_path / "agents.json").write_bytes(text.encode())
        assert AgentProject.open(tmp_path).to_files()["agents.json"] == text

    def test_refuses_config_paths_outside_the_project_directly_or_through_a_symlink(
        self, tmp_path: pathlib.Path
    ) -> None:
        outside = tmp_path / "outside"
        outside.mkdir()
        (outside / "a.json").write_text("{}")

        escaping = tmp_path / "escaping"
        escaping.mkdir()
        (escaping / "agents.json").write_text(json.dumps({"agents": [{"config": "../outside/a.json"}]}))
        with pytest.raises(AgentProjectError, match="outside the project"):
            AgentProject.open(escaping)

        linked = tmp_path / "linked"
        linked.mkdir()
        (linked / "agent_configs").symlink_to(outside, target_is_directory=True)
        (linked / "agents.json").write_text(json.dumps({"agents": [{"config": "agent_configs/a.json"}]}))
        with pytest.raises(AgentProjectError, match="through a symlink"):
            AgentProject.open(linked)

    def test_never_writes_through_a_symlinked_file(self, tmp_path: pathlib.Path) -> None:
        target = tmp_path / "elsewhere.json"
        target.write_text("keep")
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        project = AgentProject.open(project_dir)
        (project_dir / "agents.json").symlink_to(target)
        project._record_agent(Agent("A", prompt="p"), "agent_1", Agent("A", prompt="p").to_json())
        with pytest.raises(AgentProjectError):
            project.save()
        assert target.read_text() == "keep"


class TestAgentProjectReviewFixes:
    def test_rejects_a_branch_the_project_has_no_file_for_before_any_request(self) -> None:
        project = AgentProject.from_files(read_tree(CLI_PROJECT))
        server = FakeServer()
        client = server.client()
        with pytest.raises(AgentProjectError, match="has no config file"):
            client.conversational_ai.agents.push(project.agent("Billing"), project=project, branch_id="agtbrch_x")
        with pytest.raises(AgentProjectError, match="has no config file"):
            client.conversational_ai.agents.pull("agent_support", project=project, branch_id="agtbrch_x")
        assert server.calls == []

    def test_keeps_the_main_agent_when_a_branch_is_recorded_and_the_tool_type_in_step(self) -> None:
        project = AgentProject.from_files(read_tree(CLI_PROJECT))
        main = project.agent("Support")
        beta = Agent.from_json(read_json("agent_configs/support.beta.json"))
        project._record_agent(beta, "agent_support", beta.to_json(), branch_id="agtbrch_beta", match_by="id")
        assert project.agent("Support") is main
        assert "agent_configs/support.beta.json" in project.changed_files()
        assert "agent_configs/support.json" not in project.changed_files()

        lookup = project.tools()[0]
        client_tool = Tool.client("lookup_order", "Now a client tool")
        lookup_id = project.tool_id(lookup)
        assert lookup_id is not None
        project._record_tool(client_tool, lookup_id, client_tool.to_json(), "id")
        assert json.loads(project.to_files()["tools.json"])["tools"][0]["type"] == "client"

    def test_drops_a_pending_write_once_a_file_is_back_to_what_was_loaded(self) -> None:
        loaded = {"name": "A", "conversation_config": {}, "platform_settings": {}, "tags": []}
        files = {
            "agents.json": format_index({"agents": [{"config": "agent_configs/a.json", "id": "agent_1"}]}),
            "agent_configs/a.json": format_config(loaded),
        }
        project = AgentProject.from_files(files)
        agent = project.agent("A")
        project._record_agent(agent, "agent_1", {**loaded, "tags": ["x"]})
        assert project.changed_files() == ["agent_configs/a.json"]
        project._record_agent(agent, "agent_1", loaded)
        assert project.changed_files() == []
        assert project.to_files() == {**files, "tools.json": '{\n    "tools": []\n}'}

    def test_matches_a_rebuilt_agent_by_name_and_rejects_ambiguous_names(self) -> None:
        project = AgentProject.from_files(read_tree(CLI_PROJECT))
        assert project.agent_id(Agent("Billing")) == "agent_billing"
        duplicate = AgentProject.from_files(
            {
                "agents.json": format_index(
                    {"agents": [{"config": "agent_configs/a.json"}, {"config": "agent_configs/b.json"}]}
                ),
                "agent_configs/a.json": json.dumps({"name": "A"}),
                "agent_configs/b.json": json.dumps({"name": "A"}),
            }
        )
        with pytest.raises(AgentProjectError, match="are named"):
            duplicate.agent_id(Agent("A"))


class TestBranchEntries:
    MAIN_CONFIG = json.dumps(
        {
            "name": "Support",
            "conversation_config": {"agent": {"prompt": {"prompt": "p"}}},
            "platform_settings": {},
            "tags": [],
        }
    )

    # A branch entry without a config path is rejected like a missing branch, before any request, so a branch never
    # writes the main branch's file.
    @pytest.mark.parametrize(
        "branch",
        [
            {"branch_id": "agtbrch_beta"},
            {"branch_id": "agtbrch_beta", "config": ""},
            {"branch_id": "agtbrch_beta", "config": 1},
        ],
        ids=["no config", "empty config", "non-string config"],
    )
    def test_rejects_a_branch_entry_without_a_config_before_anything_is_written(
        self, branch: typing.Dict[str, typing.Any]
    ) -> None:
        project = AgentProject.from_files(
            {
                "agents.json": json.dumps(
                    {
                        "agents": [
                            {
                                "config": "agent_configs/support.json",
                                "id": "agent_support",
                                "branches": {"beta": branch},
                            }
                        ]
                    }
                ),
                "agent_configs/support.json": self.MAIN_CONFIG,
            }
        )
        server = FakeServer()
        server.add_agent("agent_support", json.loads(self.MAIN_CONFIG))
        server.branches[("agent_support", "agtbrch_beta")] = json.loads(self.MAIN_CONFIG)
        support = project.agent("Support").update(prompt="changed")
        client = server.client()

        with pytest.raises(AgentProjectError, match='Branch agtbrch_beta of "Support" has no config file'):
            client.conversational_ai.agents.push(support, project=project, branch_id="agtbrch_beta")
        with pytest.raises(AgentProjectError, match='Branch agtbrch_beta of "agent_support" has no config file'):
            client.conversational_ai.agents.pull("agent_support", project=project, branch_id="agtbrch_beta")
        assert server.calls == []
        assert project.changed_files() == []

        # Recording directly never falls back to the main file either.
        with pytest.raises(AgentProjectError, match="has no config file"):
            project._record_agent(support, "agent_support", support.to_json(), branch_id="agtbrch_beta", match_by="id")
        assert project.changed_files() == []
