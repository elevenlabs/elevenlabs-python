import json
import pathlib
import typing
import warnings

import httpx
import pytest

from elevenlabs import ElevenLabs
from elevenlabs.agent_workflows import (
    Condition,
    Destination,
    Expr,
    Workflow,
    WorkflowIssue,
    WorkflowValidationError,
)
from elevenlabs.types import (
    AgentWorkflowRequestModelNodesValue_StandaloneAgent,
    AgentWorkflowRequestModelNodesValue_Tool,
    GetAgentResponseModel,
    PositionInput,
    WorkflowToolLocatorSchemaOverridesValue_Constant,
    WorkflowToolLocatorSchemaOverridesValue_DynamicVariable,
)

# Behaviour the shared fixtures (test_fixtures.py) can't cover: the Python-facing model from build(), the Expr
# builder, from_agent() on SDK-shaped responses, and rules with no fixture yet.

FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> typing.Dict[str, typing.Any]:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def support_line() -> Workflow:
    wf = Workflow(prevent_subagent_loops=True)
    triage = wf.converse("triage", "Greet the caller", label="Triage")
    identify = triage.when("Caller wants to check an order").converse("identify", "Ask for the order number")
    lookup = identify.when("Caller gave an order number").tool("lookup_order", ["tool_get_order"])
    resolve = lookup.on_success().converse("resolve", "Explain the order status")
    lookup.on_failure().go_to(identify)
    triage.when(Expr.variable("tier").eq("gold")).transfer("vip", Destination.agent("agent_vip"))
    resolve.when("Caller is satisfied").end()
    return wf


def build_errors(wf: Workflow) -> typing.List[str]:
    try:
        wf.build()
    except WorkflowValidationError as err:
        return sorted(issue.code for issue in err.issues)
    return []


def collect_warnings(wf: Workflow) -> typing.List[WorkflowIssue]:
    issues: typing.List[WorkflowIssue] = []
    wf.build(on_warning=issues.append)
    return issues


def sent_workflow(workflow: typing.Any, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """The `workflow` field of the body agents.update() sends."""
    requests: typing.List[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"agent_id": "agent_1"})

    client = ElevenLabs(api_key="test", httpx_client=httpx.Client(transport=httpx.MockTransport(handler)))
    client.conversational_ai.agents.update("agent_1", workflow=workflow, **kwargs)
    return json.loads(requests[0].content)["workflow"]


class TestBuild:
    def test_returns_a_model_agents_update_sends_exactly_as_to_json_writes_it(self) -> None:
        wf = support_line()
        model = wf.build()

        assert list((model.nodes or {}).keys()) == [
            "start_node",
            "triage",
            "identify",
            "lookup_order",
            "resolve",
            "vip",
            "end",
        ]
        assert isinstance((model.nodes or {})["lookup_order"], AgentWorkflowRequestModelNodesValue_Tool)
        assert model.prevent_subagent_loops is True
        assert sent_workflow(model) == wf.to_json()

    def test_reports_every_problem_in_one_error_instead_of_failing_on_the_first(self) -> None:
        wf = Workflow()
        a = wf.converse("a", "A")
        # None of these raise: chaining only records problems, so all of them surface together.
        wf.converse("a", "duplicate id")
        a.go_to("missing")
        a.on_success().end()

        # The duplicate node also adds a second start_node → "a" edge.
        assert build_errors(wf) == ["duplicate_edge", "duplicate_node_id", "result_edge_needs_tool", "unknown_node"]
        with pytest.raises(
            WorkflowValidationError, match=r'Node id "a" is used by more than one node[\s\S]*unknown node "missing"'
        ):
            wf.build()

    def test_lets_go_to_target_a_node_that_is_only_created_later(self) -> None:
        wf = Workflow()
        wf.converse("a", "A").when("Skip ahead").go_to("b")
        wf.converse("b", "B")

        assert build_errors(wf) == []
        assert (wf.build().nodes or {})["a"].edge_order == ["a__b"]

    def test_rejects_a_second_edge_between_the_same_two_nodes(self) -> None:
        # The API allows one edge per pair of nodes, in either direction.
        twice = Workflow()
        a = twice.converse("a", "A")
        a.when("first").converse("b", "B")
        a.when("second").go_to("b")

        # This edge already has a way back, so going back along it again can't be merged into it.
        with_back = Workflow()
        with_back.converse("a", "A").when("next", back="return").converse("b", "B").when("go back").go_to("a")

        assert [build_errors(twice), build_errors(with_back)] == [["duplicate_edge"], ["duplicate_edge"]]

    def test_rejects_edges_from_a_node_to_itself_without_merging_a_second_one_into_the_first(self) -> None:
        wf = Workflow()
        a = wf.converse("a", "A")
        a.when("Ask again").go_to(a)
        a.when("Ask once more").go_to(a)

        assert build_errors(wf) == ["duplicate_edge", "self_loop", "self_loop"]

    def test_sends_go_to_back_along_an_existing_edge_as_that_edges_backward_condition(self) -> None:
        wf = Workflow()
        identify = wf.converse("identify", "Ask for the order number")
        lookup = identify.when("Gave a number").tool("lookup", ["tool_get_order"])
        lookup.on_success().converse("resolve", "Resolve")
        lookup.on_failure().go_to(identify)
        model = wf.to_json()

        assert list(wf.build().edges or {}) == ["start_node__identify", "identify__lookup", "lookup__resolve"]
        assert model["edges"]["identify__lookup"]["backward_condition"] == {"type": "result", "successful": False}
        # The API lists the edge under both nodes; the lookup node keeps its routing order.
        assert model["nodes"]["identify"]["edge_order"] == ["identify__lookup"]
        assert model["nodes"]["lookup"]["edge_order"] == ["lookup__resolve", "identify__lookup"]

    def test_lists_an_edge_with_a_backward_condition_under_both_of_its_nodes(self) -> None:
        wf = Workflow()
        wf.converse("a", "A").when("next", back="go back").converse("b", "B")
        nodes = wf.build().nodes or {}

        assert [nodes["a"].edge_order, nodes["b"].edge_order] == [["a__b"], ["a__b"]]

    def test_builds_despite_unreachable_nodes_reporting_them_as_warnings(self) -> None:
        wf = Workflow()
        wf.converse("a", "A").end()
        wf.node("a").when("never").converse("b", "B")
        wf.remove("a")
        issues: typing.List[WorkflowIssue] = []

        model = wf.build(on_warning=issues.append)

        assert [(w.code, w.node_id) for w in issues] == [("unreachable_node", "end"), ("unreachable_node", "b")]
        # Unreachable nodes share the column after the deepest reachable one, in insertion order.
        nodes = model.nodes or {}
        assert nodes["end"].position == PositionInput(x=300, y=0)
        assert nodes["b"].position == PositionInput(x=300, y=200)

    def test_counts_a_node_reached_only_through_a_backward_condition_as_reachable(self) -> None:
        always = {"type": "unconditional"}
        wf = Workflow.from_json(
            {
                "nodes": {
                    "start": {"type": "start", "edge_order": ["start__a"], "position": {"x": 0, "y": 0}},
                    "a": {
                        "type": "override_agent",
                        "label": "a",
                        "additional_prompt": "A",
                        "edge_order": [],
                        "position": {"x": 300, "y": 0},
                    },
                    "b": {
                        "type": "override_agent",
                        "label": "b",
                        "additional_prompt": "B",
                        "edge_order": ["b__a"],
                        "position": {"x": 600, "y": 0},
                    },
                },
                "edges": {
                    "start__a": {"source": "start", "target": "a", "forward_condition": always},
                    "b__a": {"source": "b", "target": "a", "forward_condition": always, "backward_condition": always},
                },
            }
        )

        assert collect_warnings(wf) == []

    def test_lays_out_a_node_by_its_forward_path_not_by_a_back_edge_to_an_ancestor(self) -> None:
        wf = Workflow()
        a = wf.converse("a", "A")
        a.when("next").converse("b", "B").when("next").converse("c", "C").go_to(a, back="Back to C")

        assert (wf.build().nodes or {})["c"].position == PositionInput(x=900, y=0)

    def test_places_a_node_reached_only_through_a_backward_condition_after_its_target(self) -> None:
        always = {"type": "unconditional"}
        wf = Workflow.from_json(
            {
                "nodes": {
                    "start": {"type": "start", "edge_order": ["start__a"], "position": {"x": 0, "y": 0}},
                    "a": {"type": "override_agent", "label": "a", "additional_prompt": "A", "edge_order": []},
                    "b": {"type": "override_agent", "label": "b", "additional_prompt": "B", "edge_order": ["b__a"]},
                },
                "edges": {
                    "start__a": {"source": "start", "target": "a", "forward_condition": always},
                    "b__a": {"source": "b", "target": "a", "forward_condition": always, "backward_condition": always},
                },
            }
        )

        nodes = wf.build().nodes or {}

        assert [nodes["a"].position, nodes["b"].position] == [PositionInput(x=300, y=0), PositionInput(x=600, y=0)]

    def test_places_a_new_node_on_a_free_row_instead_of_on_top_of_a_loaded_node(self) -> None:
        def at(x: int, y: int) -> typing.Dict[str, typing.Any]:
            return {"position": {"x": x, "y": y}}

        def edge(source: str, target: str) -> typing.Dict[str, typing.Any]:
            return {"source": source, "target": target, "forward_condition": {"type": "llm", "condition": target}}

        wf = Workflow.from_json(
            {
                "nodes": {
                    "start": {"type": "start", **at(0, 0), "edge_order": ["start__a"]},
                    "a": {"type": "override_agent", "label": "a", **at(300, 0), "edge_order": ["a__b", "a__c"]},
                    "b": {"type": "override_agent", "label": "b", **at(600, 0)},
                    "c": {"type": "override_agent", "label": "c", **at(600, 200)},
                },
                "edges": {"start__a": edge("start", "a"), "a__b": edge("a", "b"), "a__c": edge("a", "c")},
            }
        )

        wf.node("a").when("d").converse("d", "D")

        assert (wf.build().nodes or {})["d"].position == PositionInput(x=600, y=400)

    def test_warns_about_a_node_type_this_sdk_version_doesnt_model_and_still_sends_it(self) -> None:
        fixture = load_fixture("06-round-trip.json")
        wf = Workflow.from_json(fixture["from"])

        # "say" is in the generated types, so only the made-up type is flagged.
        assert [(w.code, w.node_id) for w in collect_warnings(wf)] == [("unknown_node_type", "survey")]
        with warnings.catch_warnings():
            # Pydantic warns that the untyped node doesn't match any member of the node union.
            warnings.simplefilter("ignore")
            assert sent_workflow(wf.build()) == fixture["expected"]

    def test_to_json_can_be_sent_as_is_for_node_types_this_sdk_version_doesnt_model(self) -> None:
        wf = Workflow.from_json(load_fixture("06-round-trip.json")["from"])

        body = sent_workflow(None, request_options={"additional_body_parameters": {"workflow": wf.to_json()}})

        assert body == wf.to_json()

    def test_writes_whole_float_positions_as_integers_like_every_other_sdk(self) -> None:
        wf = Workflow()
        wf.converse("a", "A", position=PositionInput(x=300, y=0))

        assert '"x": 300,' in wf.to_json_string()


class TestExpr:
    # The fixtures load these ASTs as data, so this is the only check that the Expr builder produces them.
    fixture = load_fixture("04-expressions-and-loops.json")

    def test_builds_the_vip_rule_from_the_fixture(self) -> None:
        vip = Expr.any_of(
            Expr.variable("tier").eq("gold"),
            Expr.all_of(Expr.variable("orders").gte(10), Expr.variable("churn_risk").neq(False)),
        )

        assert Condition.expr(vip).to_wire() == self.fixture["expected"]["edges"]["triage__vip"]["forward_condition"]

    def test_builds_the_refund_rule_from_the_fixture(self) -> None:
        threshold = Expr.if_else(
            Expr.variable("region").eq(None),
            500,
            Expr.literal(1000).sub(Expr.variable("discount").div(Expr.literal(1).add(1))),
        )
        refund = Expr.variable("unit_price").mul(Expr.variable("quantity")).gt(threshold)

        assert (
            Condition.expr(refund, label="Large refund").to_wire()
            == self.fixture["expected"]["edges"]["triage__refund"]["forward_condition"]
        )

    def test_builds_the_satisfaction_rule_from_the_fixture(self) -> None:
        satisfied = Expr.llm("How satisfied is the caller, from 1 to 10?", type="number").lt(5)

        assert Condition.expr(satisfied).to_wire() == self.fixture["expected"]["edges"]["faq__end"]["forward_condition"]

    def test_extracts_a_boolean_by_default(self) -> None:
        assert Expr.llm("Did the caller agree?").to_wire() == {
            "type": "llm",
            "value_schema": {"type": "boolean", "description": "Did the caller agree?"},
        }

    def test_lists_allowed_values(self) -> None:
        expr = Expr.llm("Which plan?", type="string", enum=["free", "pro"])

        assert expr.to_wire()["value_schema"]["enum"] == ["free", "pro"]

    def test_maps_lt_and_lte_to_distinct_operators(self) -> None:
        assert Expr.variable("x").lt(3).to_wire()["type"] == "lt_operator"
        assert Expr.variable("x").lte(3).to_wire()["type"] == "lte_operator"

    def test_turns_true_into_a_boolean_literal_not_a_number(self) -> None:
        assert Expr.literal(True).to_wire() == {"type": "boolean_literal", "value": True}

    def test_converts_to_and_from_the_generated_model(self) -> None:
        expr = Expr.if_else(Expr.variable("a"), 1, 2)

        assert Expr.from_model(expr.to_model()).to_wire() == expr.to_wire()

    def test_is_accepted_directly_by_when_as_an_expression_condition(self) -> None:
        wf = Workflow()
        wf.converse("a", "A").when(Expr.variable("n").gt(1)).end()

        assert wf.to_json()["edges"]["a__end"]["forward_condition"]["type"] == "expression"


class TestUpdate:
    def test_keeps_schema_overrides_for_tools_that_stay_when_a_tool_nodes_tools_change(self) -> None:
        override = WorkflowToolLocatorSchemaOverridesValue_DynamicVariable(dynamic_variable="order_id")
        wf = Workflow()
        wf.tool(
            "lookup",
            ["tool_order", "tool_customer"],
            schema_overrides={"tool_order": {"path_params.order_id": override}},
        )

        wf.node("lookup").update(tool_ids=["tool_order", "tool_loyalty"])

        assert wf.to_json()["nodes"]["lookup"]["tools"] == [
            {
                "schema_overrides": {
                    "path_params.order_id": {"dynamic_variable": "order_id", "source": "dynamic_variable"}
                },
                "tool_id": "tool_order",
            },
            {"tool_id": "tool_loyalty"},
        ]

    def test_keeps_explicit_nulls_in_schema_override_values(self) -> None:
        override = WorkflowToolLocatorSchemaOverridesValue_Constant(
            constant_value={"customer_id": None, "active": True}
        )
        wf = Workflow()
        wf.tool("lookup", ["tool_order"], schema_overrides={"tool_order": {"body.filter": override}})

        assert wf.to_json()["nodes"]["lookup"]["tools"][0]["schema_overrides"]["body.filter"] == {
            "constant_value": {"active": True, "customer_id": None},
            "source": "constant",
        }

    def test_rejects_schema_overrides_for_a_tool_the_node_doesnt_run(self) -> None:
        wf = Workflow()
        wf.tool("lookup", ["tool_order"], schema_overrides={"tool_typo": {}})

        assert build_errors(wf) == ["invalid_option"]

    def test_turns_a_phone_transfer_into_an_agent_transfer_dropping_phone_only_settings(self) -> None:
        wf = Workflow()
        wf.transfer("t", Destination.phone("+15551234567"), transfer_type="blind")

        wf.node("t").update(destination=Destination.agent("agent_x"), transfer_message="Hold on")

        t = (wf.build().nodes or {})["t"]
        assert isinstance(t, AgentWorkflowRequestModelNodesValue_StandaloneAgent)
        assert wf.to_json()["nodes"]["t"] == {
            "agent_id": "agent_x",
            "edge_order": [],
            "position": {"x": 300, "y": 0},
            "transfer_message": "Hold on",
            "type": "standalone_agent",
        }

    def test_points_an_agent_transfer_at_the_new_agents_default_entry(self) -> None:
        wf = Workflow.from_json(
            {
                "nodes": {
                    "start": {"type": "start", "edge_order": ["start__t"]},
                    "t": {
                        "type": "standalone_agent",
                        "agent_id": "agent_a",
                        "node_id": "qualify",
                        "branch_id": "branch_beta",
                        "transfer_message": "One moment",
                    },
                },
                "edges": {
                    "start__t": {"source": "start", "target": "t", "forward_condition": {"type": "unconditional"}}
                },
            }
        )

        wf.node("t").update(destination=Destination.agent("agent_b"))

        t = wf.to_json()["nodes"]["t"]
        del t["position"], t["edge_order"]
        assert t == {"type": "standalone_agent", "agent_id": "agent_b", "transfer_message": "One moment"}

    def test_rejects_options_that_belong_to_another_node_kind(self) -> None:
        wf = Workflow()
        wf.converse("a", "A")
        wf.node("a").update(transfer_message="agent transfers only", destination=Destination.phone("+1"))

        assert build_errors(wf) == ["invalid_option", "invalid_option"]

    def test_reports_updates_to_a_node_that_doesnt_exist(self) -> None:
        wf = Workflow()
        wf.node("missing").update(label="x")

        assert build_errors(wf) == ["unknown_node", "unknown_node"]


class TestOnResult:
    def test_routes_only_the_outcomes_it_is_given(self) -> None:
        wf = Workflow()
        triage = wf.converse("triage", "Triage")
        triage.when("Has an order").tool("lookup", ["tool_get_order"]).on_result(
            failure=lambda failed: failed.go_to(triage)
        )

        # The failure route goes back along the triage → lookup edge.
        assert (wf.build().nodes or {})["lookup"].edge_order == ["triage__lookup"]

    def test_puts_the_success_edge_first_even_when_failure_is_given_first(self) -> None:
        wf = Workflow()
        wf.tool("lookup", ["tool_get_order"]).on_result(
            failure=lambda failed: failed.end(id="failed"),
            success=lambda ok: ok.end(),
        )

        assert (wf.build().nodes or {})["lookup"].edge_order == ["lookup__end", "lookup__failed"]

    def test_fails_the_build_when_used_on_a_node_that_isnt_a_tool(self) -> None:
        wf = Workflow()
        wf.converse("a", "A").on_result(success=lambda ok: ok.end())

        assert build_errors(wf) == ["result_edge_needs_tool"]


class TestInsertBetween:
    def test_fails_the_build_when_the_callback_doesnt_return_the_last_inserted_node(self) -> None:
        wf = Workflow()
        wf.converse("a", "A").when("next").converse("b", "B")

        assert wf.insert_between("a", "b", lambda start: None) is None
        with pytest.raises(WorkflowValidationError, match="must return the last inserted node"):
            wf.build()

    def test_keeps_the_replaced_edges_condition_and_slot_and_returns_the_inserted_node(self) -> None:
        wf = Workflow()
        a = wf.converse("a", "A")
        a.when("first").converse("b", "B")
        a.when("second").end()

        verify = wf.insert_between("a", "b", lambda start: start.converse("verify", "Verify"))
        assert verify is not None
        verify.when("Can't verify").end(id="unverified")
        model = wf.to_json()

        assert model["nodes"]["a"]["edge_order"] == ["a__verify", "a__end"]
        assert model["edges"]["a__verify"]["forward_condition"] == {"type": "llm", "condition": "first"}
        assert model["edges"]["verify__b"]["forward_condition"] == {"type": "unconditional"}
        # The returned node is the inserted one, so branches added to it leave "verify".
        assert model["nodes"]["verify"]["edge_order"] == ["verify__b", "verify__unverified"]


class TestLoading:
    agent = GetAgentResponseModel.construct(
        agent_id="agent_1",
        workflow={
            "prevent_subagent_loops": False,
            "nodes": {
                "s": {"type": "start", "position": {"x": 5, "y": 5}, "edge_order": ["n__end"]},
                "n": {
                    "type": "override_agent",
                    "label": "N",
                    "additional_prompt": "Hi",
                    "position": {"x": 5, "y": 205},
                    "edge_order": [],
                },
            },
            # An editor-assigned id that happens to match the builder's naming scheme for a different edge.
            "edges": {"n__end": {"source": "s", "target": "n", "forward_condition": {"type": "unconditional"}}},
        },
    )

    def test_from_agent_keeps_ids_and_positions_and_never_reuses_a_loaded_edge_id(self) -> None:
        wf = Workflow.from_agent(self.agent)
        wf.node("n").when("Done").end()
        model = wf.to_json()

        assert wf.start_id == "s"
        assert model["nodes"]["s"] == {"edge_order": ["n__end"], "position": {"x": 5, "y": 5}, "type": "start"}
        assert model["edges"]["n__end"]["target"] == "n"
        assert model["nodes"]["n"]["edge_order"] == ["n__end__2"]
        assert model["edges"]["n__end__2"]["target"] == "end"

    def test_from_agent_accepts_the_workflow_field(self) -> None:
        workflow = self.agent.workflow
        assert workflow is not None

        assert Workflow.from_agent(workflow).to_json() == Workflow.from_agent(self.agent).to_json()

    def test_from_agent_gives_an_empty_workflow_for_an_agent_that_has_none(self) -> None:
        wf = Workflow.from_agent(GetAgentResponseModel.construct(agent_id="a"))

        assert wf.node_ids == ["start_node"]
        assert build_errors(wf) == []

    def test_to_json_string_writes_snake_case_json_that_from_json_reads_back_unchanged(self) -> None:
        json_string = support_line().to_json_string()

        assert '"additional_prompt": "Greet the caller"' in json_string
        assert Workflow.from_json(json_string).to_json_string() == json_string

    def test_from_json_reads_the_workflow_out_of_a_cli_agent_config_file(self) -> None:
        workflow = support_line().to_json()
        cli_config = {
            "name": "Support",
            "conversation_config": {"agent": {"prompt": {"prompt": "You are a support agent."}}},
            "platform_settings": {},
            "tags": ["support"],
            "workflow": workflow,
        }

        assert Workflow.from_json(json.dumps(cli_config)).to_json() == workflow

    def test_from_json_doesnt_share_state_with_its_input(self) -> None:
        data = support_line().to_json()
        wf = Workflow.from_json(data)
        wf.node("triage").update(prompt="Changed")

        assert data["nodes"]["triage"]["additional_prompt"] == "Greet the caller"
