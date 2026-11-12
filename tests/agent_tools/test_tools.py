import json
import typing

import httpx
import pytest

from elevenlabs import ElevenLabs
from elevenlabs.agent_tools import (
    Destination,
    Header,
    ObjectSchema,
    Schema,
    SystemTool,
    Tool,
    ToolIssue,
    ToolValidationError,
    WebhookTool,
)
from elevenlabs.core.unchecked_base_model import construct_type
from elevenlabs.types import (
    AgentConfig,
    BuiltInToolsOutput,
    ConversationalConfig,
    PromptAgentApiModelOutput,
    ToolResponseModel,
)

# Behaviour the shared fixtures (test_fixtures.py) can't cover: the Python-facing models from build(), what the
# client sends, issue paths and messages, and rules with no fixture yet. Mirrors elevenlabs-js
# tests/custom/agents/tools/tools.test.ts.


def get_order() -> WebhookTool:
    return (
        Tool.webhook("get_order", "Look up an order")
        .get("https://api.example.com/orders/{order_id}")
        .path_param("order_id", Schema.string().describe("The order number"))
    )


def issues_of(fn: typing.Callable[[], typing.Any]) -> typing.List[ToolIssue]:
    with pytest.raises(ToolValidationError) as info:
        fn()
    return info.value.issues


def codes_of(fn: typing.Callable[[], typing.Any]) -> typing.List[str]:
    return [issue.code for issue in issues_of(fn)]


def sent_body(call: typing.Callable[[ElevenLabs], typing.Any], response: typing.Dict[str, typing.Any]) -> typing.Any:
    """The JSON body the client sends for `call`, answered with `response`."""
    requests: typing.List[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=response)

    call(ElevenLabs(api_key="test", httpx_client=httpx.Client(transport=httpx.MockTransport(handler))))
    return json.loads(requests[0].content)


def tool_response(config: typing.Dict[str, typing.Any]) -> ToolResponseModel:
    """A `tools.get()` result, parsed the way the client parses one."""
    raw = {
        "id": "tool_1",
        "tool_config": config,
        "access_info": {"is_creator": True, "creator_name": "a", "creator_email": "a@example.com", "role": "admin"},
        "usage_stats": {"avg_latency_secs": 0.1},
    }
    return typing.cast(ToolResponseModel, construct_type(type_=ToolResponseModel, object_=raw))


class TestSchema:
    def test_can_be_shared_by_tools_and_editing_one_tools_copy_leaves_the_others_alone(self) -> None:
        order_id = Schema.string().describe("The order number")
        lookup = Tool.webhook("lookup", "Look up").get("https://api.example.com/{id}").path_param("id", order_id)
        cancel = (
            Tool.webhook("cancel", "Cancel")
            .post("https://api.example.com/cancel")
            .body(Schema.object().property("id", order_id))
        )

        body = typing.cast(ObjectSchema, cancel.body_schema)
        cancel.body(body.property("id", order_id.optional()))

        assert lookup.to_json()["api_schema"]["path_params_schema"] == {
            "id": {"description": "The order number", "type": "string"}
        }
        assert cancel.to_json()["api_schema"]["request_body_schema"] == {
            "properties": {"id": {"description": "The order number", "type": "string"}},
            "type": "object",
        }

    def test_loads_properties_not_in_required_as_optional(self) -> None:
        schema = Schema.from_json(
            {"properties": {"a": {"type": "string"}, "b": {"type": "string"}}, "required": ["a"], "type": "object"}
        )
        assert isinstance(schema, ObjectSchema)
        a, b = schema.property_schema("a"), schema.property_schema("b")
        assert a is not None and not a.is_optional
        assert b is not None and b.is_optional

    def test_whole_number_floats_are_integer_constants_but_booleans_are_not(self) -> None:
        def params(constant: typing.Any) -> typing.Callable[[], typing.Any]:
            return lambda: Tool.client("t", "T").param("n", Schema.integer().constant(constant)).build()

        params(3.0)()
        assert codes_of(params(True)) == ["constant_type_mismatch"]
        assert codes_of(params(2.5)) == ["constant_type_mismatch"]


class TestWebhookTool:
    def test_builds_the_request_model_tools_create_sends_exactly_as_to_json_writes_it(self) -> None:
        tool = get_order().header("Authorization", Header.secret("sec_1")).options(response_timeout_secs=10)
        request = tool.build()

        assert request.tool_config.type == "webhook"
        body = sent_body(
            lambda client: client.conversational_ai.tools.create(request=request),
            {"id": "tool_1", "tool_config": tool.to_json()},
        )
        assert body == {"tool_config": tool.to_json()}
        assert tool.to_json() == {
            "type": "webhook",
            "name": "get_order",
            "description": "Look up an order",
            "response_timeout_secs": 10,
            "api_schema": {
                "method": "GET",
                "url": "https://api.example.com/orders/{order_id}",
                "path_params_schema": {"order_id": {"type": "string", "description": "The order number"}},
                "request_headers": {"Authorization": {"secret_id": "sec_1"}},
            },
        }

    def test_replaces_a_param_with_the_same_name_in_place(self) -> None:
        tool = (
            Tool.webhook("search", "Search")
            .get("https://api.example.com/search")
            .query_param("q", Schema.string().describe("Query"))
            .query_param("limit", Schema.integer().constant(10))
            .query_param("q", Schema.string().describe("Search terms"))
        )
        assert tool.to_json()["api_schema"]["query_params_schema"] == {
            "properties": {
                "limit": {"constant_value": 10, "type": "integer"},
                "q": {"description": "Search terms", "type": "string"},
            },
            "required": ["q", "limit"],
        }

    def test_removes_params_headers_and_assignments(self) -> None:
        tool = (
            get_order()
            .query_param("q", Schema.string().describe("Query"))
            .header("X-A", Header.value("1"))
            .assign("a", "a")
            .assign("b", "b")
            .remove_query_param("q")
            .remove_header("X-A")
            .remove_assignment("a")
        )
        wire = tool.to_json()
        assert "query_params_schema" not in wire["api_schema"]
        assert "request_headers" not in wire["api_schema"]
        assert wire["assignments"] == [{"dynamic_variable": "b", "source": "response", "value_path": "b"}]

    def test_exposes_the_body_schema_for_editing(self) -> None:
        tool = (
            Tool.webhook("refund", "Refund")
            .post("https://api.example.com/refunds")
            .body(Schema.object().property("a", Schema.string().describe("A")))
        )
        body = typing.cast(ObjectSchema, tool.body_schema)
        tool.body(body.without("a").property("b", Schema.string().describe("B")))
        assert tool.to_json()["api_schema"]["request_body_schema"] == {
            "properties": {"b": {"description": "B", "type": "string"}},
            "required": ["b"],
            "type": "object",
        }

    def test_reports_every_problem_at_once_with_paths(self) -> None:
        issues = issues_of(
            lambda: Tool.webhook("broken", "Broken")
            .get("https://api.example.com/{a}")
            .path_param("b", Schema.string().describe("B").from_variable("b"))
            .build()
        )
        assert [(issue.code, issue.path) for issue in issues] == [
            ("missing_path_param", "path_params.a"),
            ("unknown_path_param", "path_params.b"),
            ("conflicting_value_source", "path_params.b"),
        ]

    def test_names_the_tool_and_lists_the_problems_in_the_error_message(self) -> None:
        with pytest.raises(ToolValidationError) as info:
            Tool.webhook("broken", "Broken").build()
        assert str(info.value) == (
            'Invalid tool "broken":\n  - Set the method and URL with get(), post(), put(), patch() or delete()'
        )

    def test_needs_a_value_source_on_every_literal_in_the_response_schema_and_under_any_container(self) -> None:
        issues = issues_of(
            lambda: Tool.webhook("save", "Save")
            .post("https://api.example.com/save")
            .query_param("q", Schema.string())
            .body(
                Schema.object().property(
                    "profile", Schema.object().from_variable("profile").property("name", Schema.string())
                )
            )
            .response(Schema.object().property("status", Schema.string()))
            .build()
        )
        assert [(issue.code, issue.path) for issue in issues] == [
            ("missing_value_source", "query.q"),
            ("missing_value_source", "body.profile.name"),
            ("missing_value_source", "response.status"),
        ]

    def test_requires_a_body_on_post_put_and_patch_allows_one_on_delete_and_forbids_one_on_get(self) -> None:
        body = Schema.object().property("note", Schema.string().describe("A note"))
        url = "https://api.example.com/notes"
        for method in ("post", "put", "patch"):
            assert codes_of(getattr(Tool.webhook("t", "T"), method)(url).build) == ["missing_body"]
            getattr(Tool.webhook("t", "T"), method)(url).body(body).build()
        Tool.webhook("t", "T").delete(url).build()
        Tool.webhook("t", "T").delete(url).body(body).build()
        assert codes_of(Tool.webhook("t", "T").get(url).body(body).build) == ["body_not_allowed"]
        Tool.webhook("t", "T").get(url).options(content_type="application/json").build()

    def test_needs_param_names_unique_across_path_query_and_body(self) -> None:
        issues = issues_of(
            lambda: Tool.webhook("t", "T")
            .post("https://api.example.com/orders")
            .query_param("id", Schema.string().describe("Id"))
            .body(Schema.object().property("id", Schema.string().describe("Id")))
            .build()
        )
        assert [(issue.code, issue.path) for issue in issues] == [("duplicate_param", "body.id")]

    def test_accepts_response_timeouts_from_5_to_300_seconds(self) -> None:
        def timeout(secs: int) -> typing.Callable[[], typing.Any]:
            return lambda: get_order().options(response_timeout_secs=secs).build()

        timeout(5)()
        timeout(300)()
        assert codes_of(timeout(4)) == ["invalid_option"]
        assert codes_of(timeout(301)) == ["invalid_option"]

    def test_follows_redirects_only_to_an_allowed_list_of_domains(self) -> None:
        get_order().options(follow_redirects=True, follow_redirects_allowed_domains=["example.com"]).build()
        assert codes_of(get_order().options(follow_redirects=True).build) == ["invalid_option"]

    def test_rejects_an_option_for_another_kind_of_tool(self) -> None:
        issues = issues_of(get_order().options(expects_response=True).build)
        assert [(issue.code, issue.path) for issue in issues] == [("invalid_option", "expects_response")]

    def test_switches_a_loaded_params_value_source_by_replacing_the_property_in_place(self) -> None:
        loaded = Tool.from_json(
            Tool.webhook("refund", "Refund")
            .post("https://api.example.com/refunds")
            .body(
                Schema.object()
                .property("order_id", Schema.string().describe("The order number"))
                .property("reason", Schema.string().describe("Why"))
            )
            .to_json()
        ).as_webhook()
        assert loaded is not None
        body = typing.cast(ObjectSchema, loaded.body_schema)
        loaded.body(body.property("order_id", Schema.string().from_variable("order_id")))
        assert loaded.to_json()["api_schema"]["request_body_schema"] == {
            "properties": {
                "order_id": {"dynamic_variable": "order_id", "type": "string"},
                "reason": {"description": "Why", "type": "string"},
            },
            "required": ["order_id", "reason"],
            "type": "object",
        }


class TestValueSources:
    def test_treats_an_empty_description_or_variable_name_as_no_source_as_the_api_does(self) -> None:
        def build(schema: Schema) -> typing.Callable[[], typing.Any]:
            return Tool.client("t", "T").param("x", schema).build

        assert codes_of(build(Schema.string().describe(""))) == ["missing_value_source"]
        assert codes_of(build(Schema.string().from_variable(""))) == ["missing_value_source"]
        assert codes_of(build(Schema.string().describe("").allowed_from("fares"))) == [
            "allowed_values_needs_description",
            "missing_value_source",
        ]

    @pytest.mark.parametrize(
        "type_, value", [(["integer", "null"], 42), (["number", "null"], 1.5), (["boolean", "null"], True)]
    )
    def test_accepts_a_constant_of_a_nullable_literal_type_and_writes_the_type_back(
        self, type_: typing.List[str], value: typing.Any
    ) -> None:
        raw = {
            "name": "t",
            "description": "T",
            "type": "client",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": type_, "constant_value": value}},
                "required": ["x"],
            },
        }
        tool = Tool.from_json(raw)
        tool.build()
        assert tool.to_json() == raw

    def test_keeps_a_null_constant_on_a_nullable_literal_through_a_reload_and_sends_it(self) -> None:
        raw = {
            "name": "t",
            "description": "T",
            "type": "client",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": ["integer", "null"], "constant_value": None}},
                "required": ["x"],
            },
        }
        tool = Tool.from_json(json.dumps(raw))
        assert tool.to_json() == raw
        request = tool.build()
        body = sent_body(lambda client: client.conversational_ai.tools.create(request=request), {"id": "tool_1"})
        assert body["tool_config"]["parameters"]["properties"]["x"] == {
            "type": ["integer", "null"],
            "constant_value": None,
        }

    def test_reads_a_null_constant_on_an_object_as_unset(self) -> None:
        schema = Schema.from_json(
            {"type": "object", "constant_value": None, "properties": {"a": {"type": "string", "description": "A"}}}
        )
        assert schema.to_json() == {"type": "object", "properties": {"a": {"type": "string", "description": "A"}}}

    def test_still_rejects_a_constant_of_the_wrong_type_for_a_nullable_literal(self) -> None:
        raw = {
            "name": "t",
            "description": "T",
            "type": "client",
            "parameters": {"type": "object", "properties": {"x": {"type": ["integer", "null"], "constant_value": "a"}}},
        }
        assert codes_of(Tool.from_json(raw).build) == ["constant_type_mismatch"]


class TestClientTool:
    def test_loads_empty_params_with_no_type_as_an_object_and_can_add_to_them(self) -> None:
        tool = Tool.from_json({"name": "t", "description": "T", "type": "client", "parameters": {}}).as_client()
        assert tool is not None and tool.parameters_schema is not None
        assert tool.parameters_schema.kind == "object"
        tool.param("x", Schema.string().describe("X")).build()

    def test_checks_require_any_of_on_the_params_object_against_the_params_it_still_has(self) -> None:
        tool = Tool.from_json(
            {
                "name": "t",
                "description": "T",
                "type": "client",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "string", "description": "A"},
                        "b": {"type": "string", "description": "B"},
                    },
                    "required_constraints": {"any_of": [{"required": ["a", "b"]}]},
                },
            }
        ).as_client()
        assert tool is not None
        tool.build()
        tool.remove_param("b")
        assert [(issue.code, issue.path) for issue in issues_of(tool.build)] == [
            ("unknown_required_property", "params")
        ]

    def test_removes_params(self) -> None:
        tool = (
            Tool.client("show", "Show something")
            .param("a", Schema.string().describe("A"))
            .param("b", Schema.string().describe("B"))
            .remove_param("a")
        )
        assert tool.parameters_schema is not None
        assert tool.parameters_schema.property_names == ["b"]

    def test_leaves_parameters_out_when_there_are_none(self) -> None:
        assert Tool.client("ping", "Ping the client").to_json() == {
            "description": "Ping the client",
            "name": "ping",
            "type": "client",
        }

    def test_accepts_response_timeouts_from_1_to_120_seconds_or_minus_1_with_expects_response(self) -> None:
        def build(**options: typing.Any) -> typing.Callable[[], typing.Any]:
            return lambda: Tool.client("wait", "Wait").options(**options).build()

        build(response_timeout_secs=1)()
        build(response_timeout_secs=120)()
        build(response_timeout_secs=-1, expects_response=True)()
        for secs in (0, 121, -1):
            assert codes_of(build(response_timeout_secs=secs)) == ["invalid_option"]

    def test_takes_client_options(self) -> None:
        tool = Tool.client("show", "Show").options(
            expects_response=True, execution_mode="async", dynamic_variable_placeholders={"user": "{}"}
        )
        config = tool.build_config()
        assert config.expects_response is True
        assert tool.to_json()["dynamic_variables"] == {"dynamic_variable_placeholders": {"user": "{}"}}


class TestSystemTool:
    def test_builds_an_entry_for_prompt_built_in_tools_that_agents_create_sends(self) -> None:
        end_call = SystemTool.end_call()
        transfer = SystemTool.transfer_to_number().transfer(
            "Caller asks for billing", Destination.phone("+15551234567")
        )
        config = ConversationalConfig(
            agent=AgentConfig(
                prompt=PromptAgentApiModelOutput(
                    built_in_tools=BuiltInToolsOutput(
                        end_call=end_call.build_config(), transfer_to_number=transfer.build_config()
                    )
                )
            )
        )
        body = sent_body(
            lambda client: client.conversational_ai.agents.create(conversation_config=config),
            {"agent_id": "agent_1"},
        )
        built_in = body["conversation_config"]["agent"]["prompt"]["built_in_tools"]
        assert built_in == {"end_call": end_call.to_json(), "transfer_to_number": transfer.to_json()}
        assert built_in["end_call"] == {
            "type": "system",
            "name": "end_call",
            "params": {"system_tool_type": "end_call"},
        }

    def test_rejects_transfer_on_a_tool_that_doesnt_transfer(self) -> None:
        tool = SystemTool.end_call().transfer("Caller asks", Destination.phone("+15551234567"))
        assert codes_of(tool.build) == ["invalid_option"]

    def test_transfers_to_a_sip_uri_only_with_a_sip_refer(self) -> None:
        sip = Destination.sip("sip:sales@pbx.example.com")
        SystemTool.transfer_to_number().transfer("Caller wants sales", sip, transfer_type="sip_refer").build()
        tool = SystemTool.transfer_to_number().transfer("Caller wants sales", sip)
        assert codes_of(tool.build) == ["invalid_destination", "no_transfers"]

    def test_transfers_to_a_sip_uri_held_in_a_dynamic_variable_only_with_a_sip_refer(self) -> None:
        sip = Destination.sip_variable("partner_sip")
        SystemTool.transfer_to_number().transfer("Caller is a partner", sip, transfer_type="sip_refer").build()
        tool = SystemTool.transfer_to_number().transfer("Caller is a partner", sip)
        assert codes_of(tool.build) == ["invalid_destination", "no_transfers"]

    def test_rejects_options_of_the_other_transfer_kind(self) -> None:
        tool = SystemTool.transfer_to_agent().transfer(
            "Caller wants sales", Destination.agent("agent_sales"), transfer_type="conference"
        )
        assert [(issue.code, issue.path) for issue in issues_of(tool.build)] == [("invalid_option", "transfer_type")]


class TestLoading:
    def test_writes_back_query_schema_fields_the_builder_doesnt_model(self) -> None:
        raw = {
            "name": "t",
            "description": "T",
            "type": "webhook",
            "api_schema": {
                "url": "https://api.example.com/t",
                "method": "GET",
                "query_params_schema": {
                    "properties": {"q": {"type": "string", "description": "Search terms"}},
                    "required": ["q"],
                    "x-metadata": {"owner": "search"},
                },
            },
        }
        tool = Tool.from_json(raw)
        assert tool.to_json() == raw
        webhook = tool.as_webhook()
        assert webhook is not None
        webhook.query_param("page", Schema.integer().describe("Page").optional())
        assert webhook.to_json()["api_schema"]["query_params_schema"]["x-metadata"] == {"owner": "search"}

    def test_loads_empty_webhook_body_and_response_schemas_with_no_type_as_objects(self) -> None:
        tool = Tool.from_json(
            {
                "name": "t",
                "description": "T",
                "type": "webhook",
                "api_schema": {
                    "url": "https://api.example.com/t",
                    "method": "POST",
                    "request_body_schema": {},
                    "response_body_schema": {},
                },
            }
        ).as_webhook()
        assert tool is not None and tool.body_schema is not None and tool.response_schema is not None
        assert (tool.body_schema.kind, tool.response_schema.kind) == ("object", "object")

    def test_loads_a_request_or_a_response_wrapper_with_a_tool_config_key(self) -> None:
        config = get_order().to_json()
        assert Tool.from_json({"tool_config": config}).to_json() == config
        assert Tool.from_json(json.dumps(config)).to_json() == config

    def test_loads_the_result_of_tools_get_reading_nulls_as_absent(self) -> None:
        config = get_order().to_json()
        api_schema = {**config["api_schema"], "request_body_schema": None, "auth_connection": None}
        tool = Tool.from_response(tool_response({**config, "assignments": None, "api_schema": api_schema}))
        assert tool.kind == "webhook"
        assert tool.to_json() == config

    def test_keeps_a_tool_of_an_unknown_type_and_warns_when_its_built(self) -> None:
        raw = {"name": "search", "type": "mcp", "mcp_server_id": "mcp_1"}
        tool = Tool.from_json(raw)
        assert tool.kind == "other"
        assert tool.as_webhook() is None
        warnings: typing.List[ToolIssue] = []
        tool.build(on_warning=warnings.append)
        assert [warning.code for warning in warnings] == ["unknown_tool_type"]
        assert tool.to_json() == raw

    def test_keeps_a_loaded_system_tool_type_the_builder_has_no_constructor_for(self) -> None:
        raw = {
            "name": "start_procedure",
            "params": {"procedures": {"refund": {"procedure_id": "proc_1"}}, "system_tool_type": "start_procedure"},
            "type": "system",
        }
        tool = Tool.from_json(raw)
        system = tool.as_system()
        assert system is not None and system.system_tool_type == "start_procedure"
        assert tool.to_json() == raw
