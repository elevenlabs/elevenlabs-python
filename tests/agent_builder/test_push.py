import json
import typing

import pytest
from .fake_server import FakeServer

from elevenlabs.agent_builder import (
    Agent,
    AgentProject,
    AgentPushError,
    AgentValidationError,
    PartialAgentPushResult,
    ToolPushResult,
)
from elevenlabs.agent_tools import Schema, SystemTool, Tool
from elevenlabs.agent_workflows import Workflow


def get_order(description: str = "Look up an order by its number") -> Tool:
    return (
        Tool.webhook("get_order", description)
        .get("https://api.example.com/orders/{order_id}")
        .path_param("order_id", Schema.string().describe("The order number"))
    )


def show_order() -> Tool:
    return Tool.client("show_order", "Show the order card").param("order_id", Schema.string().from_variable("order_id"))


def support_agent(tools: typing.Optional[typing.List[Tool]] = None) -> Agent:
    tools = tools if tools is not None else [get_order(), show_order()]
    wf = Workflow()
    (
        wf.converse("triage", "Find out what the caller needs")
        .when("Caller gave an order number")
        .tool("lookup", [tools[0]])
        .on_success()
        .converse("resolve", "Explain the order")
    )
    return Agent("Support line", prompt="You help with orders.", tools=[SystemTool.end_call(), *tools[1:]], workflow=wf)


def dumps(value: typing.Any) -> str:
    return json.dumps(value, indent=4)


class TestPush:
    def test_creates_the_tools_then_the_agent_with_their_ids(self) -> None:
        server = FakeServer()
        result = server.client().conversational_ai.agents.push(support_agent())

        assert server.writes() == [
            "POST /v1/convai/tools",
            "POST /v1/convai/tools",
            "POST /v1/convai/agents/create",
        ]
        assert result.agent_id == "agent_new_3"
        assert result.action == "created"
        assert list(result.tools.items()) == [
            ("show_order", ToolPushResult(id="tool_new_1", action="created")),
            ("get_order", ToolPushResult(id="tool_new_2", action="created")),
        ]
        sent = server.agents["agent_new_3"]
        assert sent["conversation_config"]["agent"]["prompt"]["tool_ids"] == ["tool_new_1"]
        assert sent["conversation_config"]["agent"]["prompt"]["built_in_tools"]["end_call"]["name"] == "end_call"
        assert sent["workflow"]["nodes"]["lookup"]["tools"] == [{"tool_id": "tool_new_2"}]
        assert sent["name"] == "Support line"

    def test_updates_only_what_changed_and_leaves_another_agents_same_named_tool_alone(self) -> None:
        server = FakeServer()
        client = server.client()
        agent_id = client.conversational_ai.agents.push(support_agent()).agent_id
        server.add_tool("tool_other", get_order("Someone else's").to_json(), ["agent_other"])
        server.calls.clear()

        again = client.conversational_ai.agents.push(
            support_agent([get_order("Find an order"), show_order()]), agent_id=agent_id
        )

        assert server.writes() == ["PATCH /v1/convai/tools/tool_new_2", f"PATCH /v1/convai/agents/{agent_id}"]
        assert server.calls[0].query == {"used_by_agent_id": agent_id, "page_size": "100"}
        assert again.tools == {
            "show_order": ToolPushResult(id="tool_new_1", action="unchanged"),
            "get_order": ToolPushResult(id="tool_new_2", action="updated"),
        }
        assert again.action == "updated"

    def test_reports_tools_the_agent_stopped_using_as_detached_without_deleting_them(self) -> None:
        server = FakeServer()
        client = server.client()
        agent_id = client.conversational_ai.agents.push(support_agent()).agent_id
        agent = support_agent()
        agent.update(tools=[])
        result = client.conversational_ai.agents.push(agent, agent_id=agent_id)
        assert result.tools["show_order"] == ToolPushResult(id="tool_new_1", action="detached")
        assert "tool_new_1" in server.tools

    def test_validates_before_any_api_call(self) -> None:
        server = FakeServer()
        agent = Agent("A", prompt="p", tools=[Tool.webhook("broken", "No URL")])
        with pytest.raises(AgentValidationError):
            server.client().conversational_ai.agents.push(agent)
        assert server.calls == []

    def test_reports_what_it_wrote_before_a_failure(self) -> None:
        server = FakeServer()
        server.fail_on = r"^POST /v1/convai/agents/create$"
        with pytest.raises(AgentPushError) as info:
            server.client().conversational_ai.agents.push(support_agent(), request_options={"max_retries": 0})
        assert str(info.value).startswith('Couldn\'t create agent "Support line"')
        assert info.value.step == 'Couldn\'t create agent "Support line"'
        assert info.value.__cause__ is info.value.cause
        assert info.value.result == PartialAgentPushResult(
            tools={
                "show_order": ToolPushResult(id="tool_new_1", action="created"),
                "get_order": ToolPushResult(id="tool_new_2", action="created"),
            }
        )

    def test_refuses_agent_id_together_with_a_project(self) -> None:
        server = FakeServer()
        with pytest.raises(ValueError, match="not both"):
            server.client().conversational_ai.agents.push(
                support_agent(), agent_id="agent_1", project=AgentProject.from_files({})
            )

    def test_sends_version_description_and_branch_only_when_given(self) -> None:
        server = FakeServer()
        client = server.client()
        agent_id = client.conversational_ai.agents.push(support_agent()).agent_id
        server.calls.clear()
        client.conversational_ai.agents.push(support_agent(), agent_id=agent_id)
        patch = next(call for call in server.calls if call.method == "PATCH")
        assert patch.body is not None and "version_description" not in patch.body
        assert patch.query == {}

        server.calls.clear()
        server.branches[(agent_id, "agtbrch_1")] = dict(server.agents[agent_id])
        client.conversational_ai.agents.push(
            support_agent(), agent_id=agent_id, branch_id="agtbrch_1", version_description="v2"
        )
        patch = next(call for call in server.calls if call.method == "PATCH")
        assert patch.body is not None and patch.body["version_description"] == "v2"
        assert patch.query == {"branch_id": "agtbrch_1"}

    def test_matches_a_branch_push_against_the_branch_tools_not_the_main_branch(self) -> None:
        server = FakeServer()
        client = server.client()
        agent_id = client.conversational_ai.agents.push(support_agent()).agent_id
        # The branch uses its own copy of get_order, and no show_order.
        server.add_tool("tool_branch_order", get_order("Branch lookup").to_json())
        branch = json.loads(json.dumps(server.agents[agent_id]))
        branch["workflow"]["nodes"]["lookup"]["tools"] = [{"tool_id": "tool_branch_order"}]
        branch["conversation_config"]["agent"]["prompt"]["tool_ids"] = []
        server.branches[(agent_id, "agtbrch_1")] = branch
        server.calls.clear()

        result = client.conversational_ai.agents.push(
            support_agent([get_order("Changed lookup")]), agent_id=agent_id, branch_id="agtbrch_1"
        )
        assert result.tools["get_order"].id == "tool_branch_order"
        assert result.tools["get_order"].action == "updated"
        assert "show_order" not in result.tools  # a main-branch tool the branch never used isn't "detached"
        assert server.writes() == ["PATCH /v1/convai/tools/tool_branch_order", f"PATCH /v1/convai/agents/{agent_id}"]
        assert not any(call.query.get("used_by_agent_id") for call in server.calls)


class TestPushWithAProject:
    def test_records_ids_and_writes_the_cli_layout_then_updates_by_recorded_id(self) -> None:
        server = FakeServer()
        client = server.client()
        project = AgentProject.from_files({})

        client.conversational_ai.agents.push(support_agent(), project=project)
        files = project.to_files()
        assert sorted(files) == [
            "agent_configs/Support-line.json",
            "agents.json",
            "tool_configs/get_order.json",
            "tool_configs/show_order.json",
            "tools.json",
        ]
        assert files["agents.json"] == (
            '{\n    "agents": [\n        {\n            "config": "agent_configs/Support-line.json",\n'
            '            "id": "agent_new_3"\n        }\n    ]\n}'
        )
        assert json.loads(files["tools.json"]) == {
            "tools": [
                {"type": "client", "config": "tool_configs/show_order.json", "id": "tool_new_1"},
                {"type": "webhook", "config": "tool_configs/get_order.json", "id": "tool_new_2"},
            ]
        }
        config = json.loads(files["agent_configs/Support-line.json"])
        assert config["conversation_config"]["agent"]["prompt"]["tool_ids"] == ["tool_new_1"]

        # A fresh script run: new objects, matched to the project's entries by name.
        server.calls.clear()
        reloaded = AgentProject.from_files(files)
        result = client.conversational_ai.agents.push(support_agent(), project=reloaded)
        assert server.writes() == ["PATCH /v1/convai/agents/agent_new_3"]
        assert result.tools["get_order"].action == "unchanged"
        # Only the version the update reported is new, recorded like the CLI does.
        assert reloaded.changed_files() == ["agents.json"]
        assert json.loads(reloaded.to_files()["agents.json"])["agents"][0]["version_id"] == "ver_1"

    def test_pushes_a_loaded_agents_settings_the_sdk_does_not_model(self) -> None:
        server = FakeServer()
        client = server.client()
        server.add_tool("tool_lookup", {"type": "client", "name": "lookup", "description": "old"})
        project = AgentProject.from_files(
            {
                "agents.json": json.dumps({"agents": [{"config": "agent_configs/a.json", "id": "agent_1"}]}),
                "tools.json": json.dumps(
                    {"tools": [{"type": "client", "config": "tool_configs/t.json", "id": "tool_lookup"}]}
                ),
                "agent_configs/a.json": json.dumps(
                    {
                        "name": "A",
                        "conversation_config": {
                            "agent": {"prompt": {"prompt": "p", "tool_ids": ["tool_lookup"]}},
                            "future_setting": {"on": True},
                        },
                        "platform_settings": {},
                        "tags": [],
                    }
                ),
                "tool_configs/t.json": json.dumps(
                    {"type": "client", "name": "lookup", "description": "d", "future_field": 1}
                ),
            }
        )
        server.add_agent("agent_1", {})

        agent = project.agent("A")
        agent.update(first_message="Hello")
        client.conversational_ai.agents.push(agent, project=project)

        tool_patch = next(c for c in server.calls if c.method == "PATCH" and "/tools/" in c.path)
        assert tool_patch.body is not None and tool_patch.body["tool_config"]["future_field"] == 1
        agent_patch = next(c for c in server.calls if c.method == "PATCH" and "/agents/" in c.path)
        assert agent_patch.body is not None
        assert agent_patch.body["conversation_config"]["future_setting"] == {"on": True}
        assert agent_patch.body["conversation_config"]["agent"]["first_message"] == "Hello"
        assert sorted(project.changed_files()) == [
            "agent_configs/a.json",
            "agents.json",
            "tool_configs/t.json",
            "tools.json",
        ]


class TestPull:
    def test_loads_an_agent_with_its_tools_as_tool_objects_and_writes_them_into_a_project(self) -> None:
        server = FakeServer()
        client = server.client()
        agent_id = client.conversational_ai.agents.push(support_agent()).agent_id

        project = AgentProject.from_files({})
        agent = client.conversational_ai.agents.pull(agent_id, project=project)
        assert agent.name == "Support line"
        assert [tool.name for tool in agent.tools()] == ["show_order", "get_order"]
        assert project.agent_id(agent) == agent_id

        files = project.to_files()
        assert sorted(files) == [
            "agent_configs/Support-line.json",
            "agents.json",
            "tool_configs/get_order.json",
            "tool_configs/show_order.json",
            "tools.json",
        ]
        config = json.loads(files["agent_configs/Support-line.json"])
        assert list(config) == ["conversation_config", "name", "platform_settings", "tags", "workflow"]

        # Pushing the pulled agent back changes no tools.
        server.calls.clear()
        result = client.conversational_ai.agents.push(agent, project=project)
        assert server.writes() == [f"PATCH /v1/convai/agents/{agent_id}"]
        assert [tool.action for tool in result.tools.values()] == ["unchanged", "unchanged"]


class TestPushReviewFixes:
    def test_updates_a_project_tool_whose_only_change_is_a_field_the_sdk_does_not_model(self) -> None:
        server = FakeServer()
        server.add_tool(
            "tool_1", {"type": "client", "name": "ping", "description": "d", "future_field": 1}, ["agent_1"]
        )
        server.add_agent("agent_1", {})
        project = AgentProject.from_files(
            {
                "agents.json": json.dumps({"agents": [{"config": "agent_configs/a.json", "id": "agent_1"}]}),
                "tools.json": json.dumps(
                    {"tools": [{"type": "client", "config": "tool_configs/t.json", "id": "tool_1"}]}
                ),
                "agent_configs/a.json": json.dumps(
                    {"name": "A", "conversation_config": {"agent": {"prompt": {"prompt": "p", "tool_ids": ["tool_1"]}}}}
                ),
                "tool_configs/t.json": json.dumps(
                    {"type": "client", "name": "ping", "description": "d", "future_field": 2}
                ),
            }
        )
        result = server.client().conversational_ai.agents.push(project.agent("A"), project=project)
        assert result.tools["ping"].action == "updated"
        assert server.tools["tool_1"]["config"]["future_field"] == 2

    def test_brings_the_project_up_to_date_when_the_server_already_matches_a_new_definition(self) -> None:
        server = FakeServer()
        client = server.client()
        project = AgentProject.from_files({})
        client.conversational_ai.agents.push(support_agent([get_order("v2"), show_order()]), project=project)
        stale = AgentProject.from_files(
            {**project.to_files(), "tool_configs/get_order.json": dumps(get_order("v1").to_json())}
        )
        result = client.conversational_ai.agents.push(support_agent([get_order("v2"), show_order()]), project=stale)
        assert result.tools["get_order"].action == "unchanged"
        assert json.loads(stale.to_files()["tool_configs/get_order.json"])["description"] == "v2"

    def test_does_not_report_a_tool_as_detached_while_the_workflow_still_uses_its_id(self) -> None:
        server = FakeServer()
        client = server.client()
        server.add_tool("tool_raw", show_order().to_json())
        wf = Workflow()
        wf.tool("run", ["tool_raw"])
        agent = Agent("A", prompt="p", workflow=wf)
        agent_id = client.conversational_ai.agents.push(agent).agent_id
        again = client.conversational_ai.agents.push(agent, agent_id=agent_id)
        assert again.tools == {}

    def test_keeps_a_project_tools_unmodeled_fields_when_the_same_tool_is_rebuilt_in_code(self) -> None:
        server = FakeServer()
        client = server.client()
        project = AgentProject.from_files({})
        client.conversational_ai.agents.push(support_agent(), project=project)
        files = project.to_files()
        with_extra = {**json.loads(files["tool_configs/get_order.json"]), "future_field": 1}
        files["tool_configs/get_order.json"] = dumps(with_extra)
        server.tools["tool_new_2"]["config"] = with_extra

        reloaded = AgentProject.from_files(files)
        result = client.conversational_ai.agents.push(support_agent(), project=reloaded)
        assert result.tools["get_order"].action == "unchanged"
        assert json.loads(reloaded.to_files()["tool_configs/get_order.json"])["future_field"] == 1


class TestAsync:
    async def test_push_creates_then_updates(self) -> None:
        server = FakeServer()
        client = server.async_client()
        created = await client.conversational_ai.agents.push(support_agent())
        assert created.action == "created"
        assert [tool.action for tool in created.tools.values()] == ["created", "created"]

        server.calls.clear()
        updated = await client.conversational_ai.agents.push(
            support_agent([get_order("Find an order"), show_order()]), agent_id=created.agent_id
        )
        assert server.writes() == ["PATCH /v1/convai/tools/tool_new_2", f"PATCH /v1/convai/agents/{created.agent_id}"]
        assert updated.tools["get_order"].action == "updated"

    async def test_push_reports_what_it_wrote_before_a_failure(self) -> None:
        server = FakeServer()
        server.fail_on = r"^POST /v1/convai/agents/create$"
        with pytest.raises(AgentPushError) as info:
            await server.async_client().conversational_ai.agents.push(
                support_agent(), request_options={"max_retries": 0}
            )
        assert sorted(info.value.result.tools) == ["get_order", "show_order"]

    async def test_pull_writes_the_agent_into_a_project(self) -> None:
        server = FakeServer()
        client = server.async_client()
        agent_id = (await client.conversational_ai.agents.push(support_agent())).agent_id
        project = AgentProject.from_files({})
        agent = await client.conversational_ai.agents.pull(agent_id, project=project)
        assert [tool.name for tool in agent.tools()] == ["show_order", "get_order"]
        assert project.agent_id(agent) == agent_id


MCP_CONFIG: typing.Dict[str, typing.Any] = {
    "type": "mcp",
    "name": "docs_search",
    "description": "Search the docs",
    "mcp_server_id": "mcp_1",
}
MCP_AGENT_CONFIG: typing.Dict[str, typing.Any] = {
    "name": "A",
    "conversation_config": {"agent": {"prompt": {"prompt": "p", "tool_ids": ["tool_mcp"]}}},
    "platform_settings": {},
    "tags": [],
}
MCP_MESSAGE = (
    'Tool "docs_search" has type "mcp", which push doesn\'t create or update: load it with its id or attach it with '
    "tool_ids"
)


def mcp_tool() -> Tool:
    return Tool.from_json(MCP_CONFIG)


def issues_of(agent: Agent) -> typing.List[typing.Tuple[str, typing.Optional[str], str]]:
    with pytest.raises(AgentValidationError) as raised:
        agent.validate()
    return [(issue.code, issue.path, issue.message) for issue in raised.value.issues]


def server_with_mcp() -> FakeServer:
    server = FakeServer()
    server.add_tool("tool_mcp", MCP_CONFIG, ["agent_1"])
    server.add_agent("agent_1", {})
    return server


class TestToolsPushDoesNotManage:
    # A tool push doesn't manage needs the id it was loaded with: given as a new object, it's reported before any
    # request, whether the agent or a workflow node uses it.
    def test_rejects_an_mcp_tool_without_an_id(self) -> None:
        server = FakeServer()
        agent = Agent("A", prompt="p", tools=[mcp_tool()])
        assert issues_of(agent) == [("invalid_tool", "tools.docs_search", MCP_MESSAGE)]
        with pytest.raises(AgentValidationError):
            server.client().conversational_ai.agents.push(agent)

        wf = Workflow()
        wf.converse("triage", "Find out what the caller needs").tool("search", [mcp_tool()])
        assert issues_of(Agent("A", prompt="p", workflow=wf)) == [("invalid_tool", "tools.docs_search", MCP_MESSAGE)]
        assert server.calls == []

    # Push manages webhook and client tools only: an MCP tool, like pull leaves it, stays attached by the id it was
    # loaded with and is never created or updated.
    def _check(self, server: FakeServer, agent: Agent, **options: typing.Any) -> None:
        assert agent.tools() == []
        result = server.client().conversational_ai.agents.push(agent, **options)
        assert server.writes() == ["PATCH /v1/convai/agents/agent_1"]
        assert "docs_search" not in result.tools
        assert server.agents["agent_1"]["conversation_config"]["agent"]["prompt"]["tool_ids"] == ["tool_mcp"]
        assert server.tools["tool_mcp"]["config"] == MCP_CONFIG

    def test_leaves_a_loaded_mcp_tool_attached_by_id(self) -> None:
        agent = Agent.from_json(MCP_AGENT_CONFIG, tools_by_id={"tool_mcp": mcp_tool()})
        self._check(server_with_mcp(), agent, agent_id="agent_1")

    def test_leaves_an_mcp_tool_from_tools_json_attached_by_id(self) -> None:
        project = AgentProject.from_files(
            {
                "agents.json": json.dumps({"agents": [{"config": "agent_configs/a.json", "id": "agent_1"}]}),
                "tools.json": json.dumps(
                    {"tools": [{"type": "mcp", "config": "tool_configs/docs.json", "id": "tool_mcp"}]}
                ),
                "agent_configs/a.json": json.dumps(MCP_AGENT_CONFIG),
                "tool_configs/docs.json": json.dumps(MCP_CONFIG),
            }
        )
        self._check(server_with_mcp(), project.agent("A"), project=project)

    def test_leaves_an_mcp_tool_in_a_workflow_node_attached_by_id(self) -> None:
        server = server_with_mcp()
        mcp = mcp_tool()
        agent = Agent.from_json(MCP_AGENT_CONFIG, tools_by_id={"tool_mcp": mcp})
        wf = Workflow()
        wf.converse("triage", "Find out what the caller needs").tool("search", [mcp])
        agent.update(workflow=wf)
        self._check(server, agent, agent_id="agent_1")
        assert server.agents["agent_1"]["workflow"]["nodes"]["search"]["tools"] == [{"tool_id": "tool_mcp"}]

    # A loaded MCP tool stays in tool_ids, as pull leaves it, so replacing the agent's tools keeps it attached.
    def test_keeps_a_loaded_mcp_tool_in_tool_ids(self) -> None:
        ping = Tool.from_json({"type": "client", "name": "ping", "description": "Ping the client"})
        mcp = mcp_tool()
        config = json.loads(json.dumps(MCP_AGENT_CONFIG))
        config["conversation_config"]["agent"]["prompt"]["tool_ids"] = ["tool_mcp", "tool_ping"]
        agent = Agent.from_json(config, tools_by_id={"tool_mcp": mcp, "tool_ping": ping})
        assert agent.tool_ids == ["tool_mcp"]
        assert agent.tools() == [ping]

        agent.update(tools=[get_order("Look up an order")])
        assert agent.tool_ids == ["tool_mcp"]

        def tool_ids() -> typing.Any:
            return agent.to_json(tool_ids={"get_order": "tool_order"})["conversation_config"]["agent"]["prompt"][
                "tool_ids"
            ]

        assert tool_ids() == ["tool_mcp", "tool_order"]

        # Adding the loaded MCP object back, while its id is still in tool_ids, attaches it once.
        agent.add_tool(mcp)
        assert tool_ids() == ["tool_mcp", "tool_order"]
