import json
import pathlib
import typing

import pytest

from elevenlabs.agent_builder import Agent, AgentValidationError
from elevenlabs.agent_builder._wire import canonical, deep_merge
from elevenlabs.agent_builder.agent import _typed_option
from elevenlabs.agent_tools import Schema, SystemTool, Tool, WebhookTool
from elevenlabs.agent_workflows import Workflow
from elevenlabs.types import ConversationalConfig, TurnConfig

CLI_PROJECT = pathlib.Path(__file__).parent / "fixtures" / "project" / "cli-graph"


def read_json(path: str) -> typing.Dict[str, typing.Any]:
    return json.loads((CLI_PROJECT / path).read_text(encoding="utf-8"))


def get_order() -> WebhookTool:
    return (
        Tool.webhook("get_order", "Look up an order by its number")
        .get("https://api.example.com/orders/{order_id}")
        .path_param("order_id", Schema.string().describe("The order number"))
    )


def show_order() -> Tool:
    return Tool.client("show_order", "Show the order card").param("order_id", Schema.string().from_variable("order_id"))


def issues_of(fn: typing.Callable[[], typing.Any]) -> typing.List[typing.Tuple[str, typing.Optional[str]]]:
    with pytest.raises(AgentValidationError) as info:
        fn()
    return [(issue.code, issue.path) for issue in info.value.issues]


class TestToJsonAndBuild:
    def test_maps_typed_options_tools_and_system_tools_into_the_api_config(self) -> None:
        agent = Agent(
            "Support line",
            prompt="You are a support agent.",
            first_message="Hi!",
            language="en",
            llm="gemini-2.0-flash",
            temperature=0.5,
            voice_id="voice_1",
            tts_model="eleven_flash_v2_5",
            tags=["support"],
            tools=[SystemTool.end_call(), get_order()],
            tool_ids=["tool_existing"],
        )
        config = agent.to_json(tool_ids={"get_order": "tool_1"})
        assert config == {
            "conversation_config": {
                "agent": {
                    "first_message": "Hi!",
                    "language": "en",
                    "prompt": {
                        "built_in_tools": {
                            "end_call": {
                                "name": "end_call",
                                "params": {"system_tool_type": "end_call"},
                                "type": "system",
                            }
                        },
                        "llm": "gemini-2.0-flash",
                        "prompt": "You are a support agent.",
                        "temperature": 0.5,
                        "tool_ids": ["tool_existing", "tool_1"],
                    },
                },
                "tts": {"model_id": "eleven_flash_v2_5", "voice_id": "voice_1"},
            },
            "name": "Support line",
            "platform_settings": {},
            "tags": ["support"],
        }
        assert json.dumps(config) == json.dumps(canonical(config))

        body = agent.build(tool_ids={"get_order": "tool_1"})
        assert body["name"] == "Support line"
        prompt = body["conversation_config"].agent.prompt  # type: ignore[union-attr]
        assert prompt.tool_ids == ["tool_existing", "tool_1"]  # type: ignore[union-attr]
        assert prompt.built_in_tools.end_call.name == "end_call"  # type: ignore[union-attr]
        assert "workflow" not in body

    def test_typed_options_take_their_paths_from_the_generated_models(self) -> None:
        paths = {
            key: ".".join(_typed_option(key, value)[0])
            for key, value in {
                "prompt": "p",
                "first_message": "Hi",
                "language": "en",
                "llm": "gpt-4o",
                "temperature": 0.5,
                "voice_id": "v",
                "tts_model": "eleven_flash_v2_5",
            }.items()
        }
        assert paths == {
            "prompt": "conversation_config.agent.prompt.prompt",
            "first_message": "conversation_config.agent.first_message",
            "language": "conversation_config.agent.language",
            "llm": "conversation_config.agent.prompt.llm",
            "temperature": "conversation_config.agent.prompt.temperature",
            "voice_id": "conversation_config.tts.voice_id",
            "tts_model": "conversation_config.tts.model_id",
        }

    def test_merges_the_raw_config_under_the_typed_options(self) -> None:
        agent = Agent(
            "A",
            prompt="p",
            conversation_config={"turn": {"turn_timeout": 7}, "agent": {"disable_first_message_interruptions": True}},
            platform_settings={"privacy": {"record_voice": False}},
        )
        agent.update(conversation_config=ConversationalConfig(turn=TurnConfig(silence_end_call_timeout=20)))
        config = agent.to_json()
        assert config["conversation_config"] == {
            "agent": {"disable_first_message_interruptions": True, "prompt": {"prompt": "p"}},
            "turn": {"silence_end_call_timeout": 20, "turn_timeout": 7},
        }
        assert config["platform_settings"] == {"privacy": {"record_voice": False}}

    def test_reports_a_raw_config_the_generated_model_rejects(self) -> None:
        agent = Agent("A", prompt="p", conversation_config={"turn": {"turn_timeout": "soon"}})
        assert issues_of(agent.validate) == [("invalid_config", "conversation_config")]

    def test_fills_in_the_ids_of_tool_objects_used_by_workflow_nodes(self) -> None:
        lookup = get_order()
        show = show_order()
        wf = Workflow()
        triage = wf.converse("triage", "Find out what the caller needs")
        (
            triage.when("Caller gave an order number")
            .tool(
                "lookup",
                [lookup],
                schema_overrides={"get_order": {"path_params.order_id": {"source": "constant", "constant_value": "1"}}},
            )
            .on_success()
            .converse("resolve", "Explain the order", tool_ids=[show, "tool_raw"])
        )
        agent = Agent("A", prompt="p", workflow=wf)

        assert agent.tools() == [lookup, show]
        nodes = agent.to_json(tool_ids={"get_order": "tool_g", "show_order": "tool_s"})["workflow"]["nodes"]
        assert nodes["lookup"]["tools"] == [
            {
                "schema_overrides": {"path_params.order_id": {"constant_value": "1", "source": "constant"}},
                "tool_id": "tool_g",
            }
        ]
        assert nodes["resolve"]["additional_tool_ids"] == ["tool_s", "tool_raw"]
        assert issues_of(lambda: agent.to_json(tool_ids={"get_order": "tool_g"})) == [
            ("unresolved_tool", "tools.show_order")
        ]

    def test_validates_without_ids_so_ci_needs_no_api_key(self) -> None:
        Agent("A", prompt="p", tools=[get_order()]).validate()

    def test_reports_every_problem_at_once(self) -> None:
        wf = Workflow()
        wf.tool("hang_up", [SystemTool.end_call()])
        agent = Agent(
            "",
            prompt="p",
            tools=[get_order(), get_order(), Tool.webhook("broken", "No URL")],
            workflow=wf,
            conversation_config={"agent": {"prompt": {"prompt": "raw prompt"}}},
        )
        assert issues_of(agent.validate) == [
            ("missing_name", None),
            ("option_conflict", "conversation_config.agent.prompt.prompt"),
            ("duplicate_tool_name", "tools.get_order"),
            ("invalid_tool", "tools.broken"),
            ("system_tool_in_workflow", "workflow.tools.end_call"),
        ]

    def test_warns_without_failing_when_there_is_no_prompt(self) -> None:
        warnings: typing.List[str] = []
        Agent("A").validate(on_warning=lambda issue: warnings.append(issue.code))
        assert warnings == ["missing_prompt"]


class TestFromJson:
    def test_round_trips_a_cli_agent_config_keeping_unmodeled_fields_and_tool_order(self) -> None:
        raw = read_json("agent_configs/support.json")
        lookup = Tool.from_json(read_json("tool_configs/lookup_order.json"))
        agent = Agent.from_json(raw, tools_by_id={"tool_lookup": lookup})

        assert agent.name == "Support"
        assert agent.tools() == [lookup]
        assert agent.tool_ids == ["tool_from_dashboard"]
        assert agent.to_json(tool_ids={"lookup_order": "tool_lookup"}) == canonical(raw)
        assert json.dumps(agent.to_json(tool_ids={"lookup_order": "tool_lookup"})) == json.dumps(canonical(raw))

    def test_turns_a_loaded_workflow_into_a_workflow_on_first_use_with_tool_objects(self) -> None:
        raw = read_json("agent_configs/support.beta.json")
        refund = Tool.from_json(read_json("tool_configs/issue_refund.json"))
        agent = Agent.from_json(raw, tools_by_id={"tool_refund": refund})

        assert agent.tools() == [refund]  # read from the raw workflow, before it's materialized
        unedited = agent.to_json(tool_ids={"issue_refund": "tool_refund"})
        assert unedited["workflow"] == canonical(raw["workflow"])

        workflow = agent.workflow
        assert workflow is not None
        workflow.node("refunds").update(prompt="Handle refunds")
        nodes = agent.to_json(tool_ids={"issue_refund": "tool_new"})["workflow"]["nodes"]
        assert nodes["refunds"]["additional_tool_ids"] == ["tool_new"]
        assert nodes["refunds"]["additional_prompt"] == "Handle refunds"

    def test_accepts_a_json_string(self) -> None:
        text = (CLI_PROJECT / "agent_configs" / "billing.json").read_text(encoding="utf-8")
        config = Agent.from_json(text).to_json()
        # Fields the file leaves out get their defaults, like `platform_settings: {}`.
        assert config == {"platform_settings": {}, **canonical(json.loads(text))}


class TestReviewFixes:
    def test_deep_merge_copies_what_it_merges(self) -> None:
        source: typing.Dict[str, typing.Any] = {"turn": {"turn_timeout": 7}, "tags": ["a"]}
        target: typing.Dict[str, typing.Any] = {"turn": {}}
        deep_merge(target, source)
        source["turn"]["turn_timeout"] = 8
        source["tags"].append("b")
        assert target == {"turn": {"turn_timeout": 7}, "tags": ["a"]}

    def test_replaces_a_loaded_agents_system_tools_along_with_its_other_tools(self) -> None:
        agent = Agent.from_json(read_json("agent_configs/support.json"))
        assert agent.tools() == []  # system tools aren't managed by push
        agent.update(tools=[])
        prompt = agent.to_json()["conversation_config"]["agent"]["prompt"]
        assert "built_in_tools" not in prompt
        assert prompt["tool_ids"] == ["tool_lookup", "tool_from_dashboard"]  # ids it doesn't manage stay

    def test_treats_an_explicitly_empty_tool_list_as_set(self) -> None:
        agent = Agent(
            "A",
            prompt="p",
            tool_ids=[],
            conversation_config={"agent": {"prompt": {"tool_ids": ["tool_existing"]}}},
        )
        assert issues_of(agent.validate) == [("option_conflict", "conversation_config.agent.prompt.tool_ids")]

    def test_validates_a_loaded_workflow_without_materializing_it(self) -> None:
        raw = read_json("agent_configs/support.beta.json")
        raw["workflow"]["edges"]["broken"] = {"source": "start_node", "target": "nowhere"}
        agent = Agent.from_json(raw)
        assert issues_of(agent.validate) == [("invalid_workflow", "workflow")]

    def test_writes_new_tool_ids_into_a_loaded_workflow_it_has_not_materialized(self) -> None:
        refund = Tool.from_json(read_json("tool_configs/issue_refund.json"))
        agent = Agent.from_json(read_json("agent_configs/support.beta.json"), tools_by_id={"tool_refund": refund})
        nodes = agent.to_json(tool_ids={"issue_refund": "tool_clone"})["workflow"]["nodes"]
        assert nodes["refunds"]["additional_tool_ids"] == ["tool_clone"]

    def test_attaches_a_tool_added_with_add_tool(self) -> None:
        agent = Agent("A", prompt="p").add_tool(get_order())
        prompt = agent.to_json(tool_ids={"get_order": "tool_1"})["conversation_config"]["agent"]["prompt"]
        assert prompt["tool_ids"] == ["tool_1"]


class TestWorkflowToolRefs:
    def test_lets_a_removed_nodes_tool_name_be_reused_by_a_new_tool_object(self) -> None:
        wf = Workflow()
        wf.tool("a", [get_order()])
        wf.remove("a")
        wf.tool("b", [get_order()])
        wf.build(tool_ids={"get_order": "tool_1"})

    def test_reports_two_different_tools_with_one_name(self) -> None:
        wf = Workflow()
        wf.tool("a", [get_order()])
        wf.tool("b", [get_order()])
        with pytest.raises(Exception) as info:
            wf.build(tool_ids={"get_order": "tool_1"})
        assert [issue.code for issue in info.value.issues] == ["duplicate_tool_name"]  # type: ignore[attr-defined]

    def test_reports_a_tool_object_without_an_id(self) -> None:
        wf = Workflow()
        wf.tool("a", [get_order()])
        with pytest.raises(Exception) as info:
            wf.build()
        assert [issue.code for issue in info.value.issues] == ["unresolved_tool"]  # type: ignore[attr-defined]
