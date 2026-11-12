from __future__ import annotations

import json
import re
import typing

from ..agent_workflows.destination import Destination
from ..core.unchecked_base_model import construct_type
from ..types.phone_number_transfer_custom_sip_headers_item import PhoneNumberTransferCustomSipHeadersItem
from ..types.phone_number_transfer_post_dial_digits import PhoneNumberTransferPostDialDigits
from ..types.pre_tool_speech_mode import PreToolSpeechMode
from ..types.response_filter import ResponseFilter
from ..types.search_strategy import SearchStrategy
from ..types.system_tool_config_output import SystemToolConfigOutput
from ..types.tool_call_sound_behavior import ToolCallSoundBehavior
from ..types.tool_call_sound_type import ToolCallSoundType
from ..types.tool_error_handling_mode import ToolErrorHandlingMode
from ..types.tool_execution_mode import ToolExecutionMode
from ..types.tool_interruption_mode import ToolInterruptionMode
from ..types.tool_request_model import ToolRequestModel
from ..types.tool_request_model_tool_config import (
    ToolRequestModelToolConfig,
    ToolRequestModelToolConfig_Client,
    ToolRequestModelToolConfig_Webhook,
)
from ..types.tool_response_model import ToolResponseModel
from ..types.transfer_type_enum import TransferTypeEnum
from ..types.uui_transfer_config import UuiTransferConfig
from ..types.webhook_tool_api_schema_config_input_content_type import WebhookToolApiSchemaConfigInputContentType
from ._wire import WireDict, canonical, deep_copy, parse, strip_nulls, to_wire
from .errors import ToolIssue, ToolValidationError, error
from .header import AuthConnection, Header
from .schema import ObjectSchema, Schema
from .validate import check_schema, is_literal

ToolKind = typing.Literal["webhook", "client", "system", "other"]

T = typing.TypeVar("T", bound="Tool")

_COMMON_OPTIONS = (
    "name",
    "description",
    "response_timeout_secs",
    "interruption_mode",
    "pre_tool_speech",
    "tool_call_sound",
    "tool_call_sound_behavior",
    "tool_error_handling_mode",
)
_WEBHOOK_OPTIONS = (
    *_COMMON_OPTIONS,
    "dynamic_variable_placeholders",
    "execution_mode",
    "content_type",
    "response_filter",
    "follow_redirects",
    "follow_redirects_allowed_domains",
)
_CLIENT_OPTIONS = (*_COMMON_OPTIONS, "dynamic_variable_placeholders", "execution_mode", "expects_response")
_PHONE_TRANSFER_OPTIONS = ("transfer_type", "custom_sip_headers", "sip_refer_play_dialtone", "uui", "post_dial_digits")
_AGENT_TRANSFER_OPTIONS = (
    "delay_ms",
    "transfer_message",
    "enable_transferred_agent_first_message",
    "preserve_client_tts_overrides",
    "preserve_voice_settings",
)
_ENV_VAR_TEMPLATE = re.compile(r"\{\{system__env_[a-z][a-z0-9_]*\}\}")
_PLACEHOLDER = re.compile(r"\{([^{}]+)\}")

OnWarning = typing.Callable[[ToolIssue], typing.Any]


class Tool:
    """
    An agent tool, written as code. Create one with `Tool.webhook()`, `Tool.client()` or a `SystemTool`
    constructor, or load one with `Tool.from_json()` / `Tool.from_response()`.

    Examples
    --------
    from elevenlabs.agent_tools import Header, Schema, Tool

    get_order = (
        Tool.webhook("get_order", "Look up an order by the number the caller gives")
        .get("https://api.example.com/orders/{order_id}")
        .path_param("order_id", Schema.string().describe("The order number, e.g. A-1042"))
        .header("Authorization", Header.secret("sec_orders_api"))
        .options(response_timeout_secs=10)
    )
    client.conversational_ai.tools.create(request=get_order.build())
    """

    kind: ToolKind
    """`"webhook"`, `"client"`, `"system"`, or `"other"` for a loaded tool of a type this SDK can't edit."""

    def __init__(self, config: WireDict) -> None:
        # Use the static constructors. `config` is the tool config in wire format, except the parts subclasses
        # keep in their own fields.
        self._config = config
        # Problems found while chaining, reported by `build()`.
        self._issues: typing.List[ToolIssue] = []

    @staticmethod
    def webhook(name: str, description: str) -> WebhookTool:
        """A tool the server runs by calling an HTTP endpoint. Set the method and URL with `get()`, `post()`..."""
        return WebhookTool({"name": name, "description": description}, {})

    @staticmethod
    def client(name: str, description: str) -> ClientTool:
        """A tool that sends an event to the user's client."""
        return ClientTool({"name": name, "description": description}, None)

    @staticmethod
    def from_json(data: typing.Union[str, bytes, typing.Mapping[str, typing.Any]]) -> Tool:
        """
        Loads a tool stored in API format (snake_case), for example from `to_json_string()` or a CLI
        `tool_configs/*.json` file. Accepts a JSON string or a parsed dict: a tool config, or a request or
        response with a `tool_config` key.
        """
        parsed = parse(data)
        raw: WireDict = parsed["tool_config"] if isinstance(parsed.get("tool_config"), dict) else parsed
        tool_type = raw.get("type")
        if tool_type not in ("webhook", "client", "system"):
            return _OtherTool(raw)
        config = {key: value for key, value in raw.items() if key != "type"}
        if tool_type == "webhook":
            return WebhookTool._load(config)
        if tool_type == "client":
            parameters = config.pop("parameters", None)
            return ClientTool(
                config,
                None
                if parameters is None
                else typing.cast(ObjectSchema, Schema._from_wire(parameters, False, "object")),
            )
        params = dict(config.pop("params", None) or {})
        system_tool_type = params.pop("system_tool_type", None)
        return SystemTool(str(system_tool_type), config, params)

    @staticmethod
    def from_response(response: ToolResponseModel) -> Tool:
        """Loads the result of `tools.get()`."""
        return Tool.from_json(strip_nulls(to_wire(response.tool_config)))

    @property
    def name(self) -> str:
        """The tool's name, as the LLM sees it."""
        return str(self._config.get("name"))

    def options(
        self: T,
        *,
        name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        response_timeout_secs: typing.Optional[int] = None,
        interruption_mode: typing.Optional[ToolInterruptionMode] = None,
        pre_tool_speech: typing.Optional[PreToolSpeechMode] = None,
        tool_call_sound: typing.Optional[ToolCallSoundType] = None,
        tool_call_sound_behavior: typing.Optional[ToolCallSoundBehavior] = None,
        tool_error_handling_mode: typing.Optional[ToolErrorHandlingMode] = None,
        dynamic_variable_placeholders: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        execution_mode: typing.Optional[ToolExecutionMode] = None,
        content_type: typing.Optional[WebhookToolApiSchemaConfigInputContentType] = None,
        response_filter: typing.Optional[typing.Union[ResponseFilter, typing.Mapping[str, typing.Any]]] = None,
        follow_redirects: typing.Optional[bool] = None,
        follow_redirects_allowed_domains: typing.Optional[typing.Sequence[str]] = None,
        expects_response: typing.Optional[bool] = None,
    ) -> T:
        """
        Sets options for this kind of tool. Options left as `None` are unchanged. `build()` reports an option that
        doesn't apply.

        All tools: `name`, `description`, `response_timeout_secs`, `interruption_mode`, `pre_tool_speech`,
        `tool_call_sound`, `tool_call_sound_behavior`, `tool_error_handling_mode`. Webhook tools also take
        `dynamic_variable_placeholders`, `execution_mode`, `content_type`, `response_filter`, `follow_redirects`
        and `follow_redirects_allowed_domains`; client tools `dynamic_variable_placeholders`, `execution_mode` and
        `expects_response` (wait for the client to respond, and pass its response to the LLM).
        """
        given = {
            "name": name,
            "description": description,
            "response_timeout_secs": response_timeout_secs,
            "interruption_mode": interruption_mode,
            "pre_tool_speech": pre_tool_speech,
            "tool_call_sound": tool_call_sound,
            "tool_call_sound_behavior": tool_call_sound_behavior,
            "tool_error_handling_mode": tool_error_handling_mode,
            "dynamic_variable_placeholders": dynamic_variable_placeholders,
            "execution_mode": execution_mode,
            "content_type": content_type,
            "response_filter": response_filter,
            "follow_redirects": follow_redirects,
            "follow_redirects_allowed_domains": follow_redirects_allowed_domains,
            "expects_response": expects_response,
        }
        for key, value in given.items():
            if value is None:
                continue
            if key not in self._allowed_options():
                self._issues.append(error("invalid_option", key, f'Option "{key}" doesn\'t apply to {self.kind} tools'))
            else:
                self._set_option(key, to_wire(value))
        return self

    def as_webhook(self) -> typing.Optional[WebhookTool]:
        """This tool as a `WebhookTool`, or `None` if it's another kind."""
        return self if isinstance(self, WebhookTool) else None

    def as_client(self) -> typing.Optional[ClientTool]:
        """This tool as a `ClientTool`, or `None` if it's another kind."""
        return self if isinstance(self, ClientTool) else None

    def as_system(self) -> typing.Optional[SystemTool]:
        """This tool as a `SystemTool`, or `None` if it's another kind."""
        return self if isinstance(self, SystemTool) else None

    def build(self, *, on_warning: typing.Optional[OnWarning] = None) -> ToolRequestModel:
        """
        Validates the tool and returns it as the request `tools.create()` and `tools.update()` accept.
        `on_warning` is called for each non-fatal problem.

        Raises
        ------
        ToolValidationError
            Listing every problem, if the tool is invalid.
        """
        return typing.cast(
            ToolRequestModel,
            construct_type(type_=ToolRequestModel, object_={"tool_config": self._checked_wire(on_warning)}),
        )

    def build_config(
        self, *, on_warning: typing.Optional[OnWarning] = None
    ) -> typing.Union[ToolRequestModelToolConfig, SystemToolConfigOutput]:
        """
        Validates the tool and returns only its config. For a system tool that's a `SystemToolConfigOutput`, its
        entry in `prompt.built_in_tools`, for example
        `BuiltInToolsOutput(end_call=SystemTool.end_call().build_config())`. Create webhook and client tools with
        `tools.create(request=tool.build())` and attach them by id in `prompt.tool_ids`; the inline `prompt.tools`
        field is deprecated, and replaces `built_in_tools` with the system tools it contains.

        Raises
        ------
        ToolValidationError
            Listing every problem, if the tool is invalid.
        """
        return self._construct(ToolRequestModelToolConfig, on_warning)

    def _construct(self, type_: typing.Any, on_warning: typing.Optional[OnWarning]) -> typing.Any:
        return construct_type(type_=type_, object_=self._checked_wire(on_warning))

    def to_json(self) -> WireDict:
        """
        The tool config in API format (snake_case keys, sorted at every level), the shape of a CLI
        `tool_configs/*.json` file. Validates like `build()`.
        """
        return typing.cast(WireDict, canonical(self._checked_wire(None)))

    def to_json_string(self) -> str:
        """`to_json()` as a string with 2-space indentation and a trailing newline: the canonical file format."""
        return json.dumps(self.to_json(), indent=2, ensure_ascii=False) + "\n"

    def _checked_wire(self, on_warning: typing.Optional[OnWarning]) -> WireDict:
        issues = [*self._issues, *self._validate()]
        errors = [issue for issue in issues if issue.severity == "error"]
        if errors:
            raise ToolValidationError(self.name, errors)
        if on_warning is not None:
            for warning in issues:
                if warning.severity == "warning":
                    on_warning(warning)
        return typing.cast(WireDict, deep_copy(self._to_wire()))

    def _allowed_options(self) -> typing.Tuple[str, ...]:
        raise NotImplementedError

    def _set_option(self, key: str, value: typing.Any) -> None:
        if key == "dynamic_variable_placeholders":
            self._config["dynamic_variables"] = {
                **(self._config.get("dynamic_variables") or {}),
                "dynamic_variable_placeholders": value,
            }
        else:
            self._config[key] = value

    def _validate(self) -> typing.List[ToolIssue]:
        """Problems that need the finished tool."""
        raise NotImplementedError

    def _to_wire(self) -> WireDict:
        raise NotImplementedError


class WebhookTool(Tool):
    """A tool the server runs by calling an HTTP endpoint."""

    kind: ToolKind = "webhook"

    def __init__(self, config: WireDict, api: WireDict) -> None:
        super().__init__(config)
        # The `api_schema` fields not kept below: url, method, auth, content type and so on.
        self._api = api
        self._path_params: typing.Dict[str, Schema] = {}
        self._query: typing.Optional[ObjectSchema] = None
        self._body: typing.Optional[Schema] = None
        self._response: typing.Optional[Schema] = None
        self._headers: typing.Dict[str, typing.Any] = {}

    @staticmethod
    def _load(config: WireDict) -> WebhookTool:
        api = dict(config.pop("api_schema", None) or {})
        path_params = api.pop("path_params_schema", None) or {}
        query = api.pop("query_params_schema", None)
        body = api.pop("request_body_schema", None)
        response = api.pop("response_body_schema", None)
        headers = api.pop("request_headers", None) or {}
        tool = WebhookTool(config, api)
        for name, model in path_params.items():
            tool._path_params[name] = Schema._from_wire(model)
        if query is not None:
            tool._query = typing.cast(ObjectSchema, Schema._from_wire({"type": "object", **query}))
        if body is not None:
            tool._body = Schema._from_wire(body, False, "object")
        if response is not None:
            tool._response = Schema._from_wire(response, False, "object")
        tool._headers = dict(headers)
        return tool

    def get(self, url: str) -> WebhookTool:
        """Sends a `GET` to `url`. `{name}` placeholders in the URL are filled from path params."""
        return self._request("GET", url)

    def post(self, url: str) -> WebhookTool:
        """Sends a `POST` to `url`."""
        return self._request("POST", url)

    def put(self, url: str) -> WebhookTool:
        """Sends a `PUT` to `url`."""
        return self._request("PUT", url)

    def patch(self, url: str) -> WebhookTool:
        """Sends a `PATCH` to `url`."""
        return self._request("PATCH", url)

    def delete(self, url: str) -> WebhookTool:
        """Sends a `DELETE` to `url`."""
        return self._request("DELETE", url)

    def path_param(self, name: str, schema: Schema) -> WebhookTool:
        """Sets the path param `name`, filling the `{name}` placeholder in the URL. Literal schemas only."""
        self._path_params[name] = schema
        return self

    def query_param(self, name: str, schema: Schema) -> WebhookTool:
        """Sets the query param `name`. Required unless the schema is `optional()`. Literal schemas only."""
        self._query = (self._query or Schema.object()).property(name, schema)
        return self

    def body(self, schema: Schema) -> WebhookTool:
        """Sets the request body schema. Must be an object."""
        self._body = schema
        return self

    def response(self, schema: Schema) -> WebhookTool:
        """Sets the response body schema. Must be an object."""
        self._response = schema
        return self

    def header(self, name: str, value: Header) -> WebhookTool:
        """Sets the request header `name`."""
        self._headers[name] = value.to_wire()
        return self

    def auth(self, connection: AuthConnection) -> WebhookTool:
        """Authenticates requests with an auth connection."""
        self._api["auth_connection"] = connection.to_wire()
        return self

    def assign(
        self,
        variable: str,
        value_path: str,
        *,
        sanitize: typing.Optional[bool] = None,
        preserve_native_type: typing.Optional[bool] = None,
    ) -> WebhookTool:
        """
        Stores the value at `value_path` in the response (dot notation, e.g. `"order.status"`) in `variable`.
        `sanitize` removes the value from the response before the LLM and the transcript see it;
        `preserve_native_type` stores lists and objects as they are instead of as JSON strings.
        """
        assignment: WireDict = {"source": "response", "dynamic_variable": variable, "value_path": value_path}
        if sanitize is not None:
            assignment["sanitize"] = sanitize
        if preserve_native_type is not None:
            assignment["preserve_native_type"] = preserve_native_type
        self._config["assignments"] = [*(self._config.get("assignments") or []), assignment]
        return self

    def remove_path_param(self, name: str) -> WebhookTool:
        """Removes the path param `name`."""
        self._path_params.pop(name, None)
        return self

    def remove_query_param(self, name: str) -> WebhookTool:
        """Removes the query param `name`."""
        if self._query is not None:
            self._query = self._query.without(name)
        return self

    def remove_header(self, name: str) -> WebhookTool:
        """Removes the request header `name`."""
        self._headers.pop(name, None)
        return self

    def remove_assignment(self, variable: str) -> WebhookTool:
        """Removes every assignment to `variable`."""
        assignments = self._config.get("assignments") or []
        self._config["assignments"] = [a for a in assignments if a.get("dynamic_variable") != variable]
        return self

    @property
    def body_schema(self) -> typing.Optional[Schema]:
        """The request body schema, for editing and setting again with `body()`."""
        return self._body

    @property
    def response_schema(self) -> typing.Optional[Schema]:
        """The response body schema, for editing and setting again with `response()`."""
        return self._response

    def build_config(self, *, on_warning: typing.Optional[OnWarning] = None) -> ToolRequestModelToolConfig_Webhook:
        """Validates the tool and returns only its config. See `Tool.build_config()`."""
        return typing.cast(
            ToolRequestModelToolConfig_Webhook, self._construct(ToolRequestModelToolConfig_Webhook, on_warning)
        )

    def _allowed_options(self) -> typing.Tuple[str, ...]:
        return _WEBHOOK_OPTIONS

    def _set_option(self, key: str, value: typing.Any) -> None:
        if key in ("content_type", "response_filter"):
            self._api[key] = value
        else:
            super()._set_option(key, value)

    def _validate(self) -> typing.List[ToolIssue]:
        issues: typing.List[ToolIssue] = []
        url: typing.Optional[str] = self._api.get("url")
        if url is None:
            issues.append(
                error("missing_url", None, "Set the method and URL with get(), post(), put(), patch() or delete()")
            )
        # As the API does: env var templates aren't placeholders, and the auth connection fills
        # `auth_resolved_params`.
        placeholders = _PLACEHOLDER.findall(_ENV_VAR_TEMPLATE.sub("env", url or ""))
        auth_resolved: typing.List[str] = self._api.get("auth_resolved_params") or []
        for name in placeholders:
            if name not in self._path_params and name not in auth_resolved:
                issues.append(
                    error(
                        "missing_path_param",
                        f"path_params.{name}",
                        f'The URL has {{{name}}} but no path_param("{name}")',
                    )
                )
        for name, schema in self._path_params.items():
            path = f"path_params.{name}"
            if url is not None and name not in placeholders:
                issues.append(error("unknown_path_param", path, f'path_param("{name}") has no {{{name}}} in the URL'))
            elif name in auth_resolved:
                issues.append(
                    error("unknown_path_param", path, f"{{{name}}} is filled by the auth connection, not a path_param")
                )
            if not is_literal(schema.kind):
                issues.append(
                    error("param_not_literal", path, f'Path param "{name}" must be a string, integer, number or bool')
                )
            check_schema(schema, path, True, issues)
        if self._query is not None:
            for name in self._query.property_names:
                schema = typing.cast(Schema, self._query.property_schema(name))
                path = f"query.{name}"
                if not is_literal(schema.kind):
                    issues.append(
                        error(
                            "param_not_literal", path, f'Query param "{name}" must be a string, integer, number or bool'
                        )
                    )
                check_schema(schema, path, True, issues)
        for label, part in (("body", self._body), ("response", self._response)):
            if part is None:
                continue
            if part.kind != "object":
                issues.append(error("body_not_object", label, f"The {label} schema must be an object"))
            check_schema(part, label, False, issues)
        method = self._api.get("method")
        if method == "GET" and self._body is not None:
            issues.append(error("body_not_allowed", "body", "A GET request can't have a body"))
        if method in ("POST", "PUT", "PATCH") and self._body is None:
            issues.append(error("missing_body", "body", f"A {method} request needs a body"))
        where: typing.Dict[str, str] = {}
        body_names = self._body.property_names if isinstance(self._body, ObjectSchema) else []
        for location, names in (
            ("path_params", list(self._path_params)),
            ("query", self._query.property_names if self._query is not None else []),
            ("body", body_names),
        ):
            for name in names:
                first = where.get(name)
                if first is not None:
                    issues.append(
                        error(
                            "duplicate_param",
                            f"{location}.{name}",
                            f'"{name}" is in both {first} and {location}; param names must be unique across path, '
                            "query and body",
                        )
                    )
                else:
                    where[name] = location
        seen: typing.Dict[str, str] = {}
        for name in self._headers:
            other = seen.get(name.lower())
            if other is not None:
                issues.append(
                    error("duplicate_header", f"headers.{name}", f'Headers "{other}" and "{name}" differ only in case')
                )
            seen[name.lower()] = name
        timeout = self._config.get("response_timeout_secs")
        if timeout is not None and (timeout < 5 or timeout > 300):
            issues.append(
                error("invalid_option", "response_timeout_secs", "A webhook tool's response_timeout_secs must be 5-300")
            )
        domains = self._config.get("follow_redirects_allowed_domains")
        if self._config.get("follow_redirects") is True and not domains:
            issues.append(
                error("invalid_option", "follow_redirects", "follow_redirects needs follow_redirects_allowed_domains")
            )
        return issues

    def _to_wire(self) -> WireDict:
        api: WireDict = dict(self._api)
        if self._path_params:
            api["path_params_schema"] = {name: schema._to_wire() for name, schema in self._path_params.items()}
        if self._query is not None:
            query = self._query._to_wire()
            if "properties" in query:
                api["query_params_schema"] = {key: query[key] for key in ("properties", "required") if key in query}
        if self._body is not None:
            api["request_body_schema"] = self._body._to_wire()
        if self._response is not None:
            api["response_body_schema"] = self._response._to_wire()
        if self._headers:
            api["request_headers"] = dict(self._headers)
        return {**self._config, "type": "webhook", "api_schema": api}

    def _request(self, method: str, url: str) -> WebhookTool:
        self._api["method"] = method
        self._api["url"] = url
        return self


class ClientTool(Tool):
    """A tool that sends an event to the user's client."""

    kind: ToolKind = "client"

    def __init__(self, config: WireDict, parameters: typing.Optional[ObjectSchema]) -> None:
        super().__init__(config)
        self._parameters = parameters

    def param(self, name: str, schema: Schema) -> ClientTool:
        """Sets the param `name`. Required unless the schema is `optional()`. Any kind of schema."""
        self._parameters = (self._parameters or Schema.object()).property(name, schema)
        return self

    def remove_param(self, name: str) -> ClientTool:
        """Removes the param `name`."""
        if self._parameters is not None:
            self._parameters = self._parameters.without(name)
        return self

    @property
    def parameters_schema(self) -> typing.Optional[ObjectSchema]:
        """The params, as an object schema."""
        return self._parameters

    def build_config(self, *, on_warning: typing.Optional[OnWarning] = None) -> ToolRequestModelToolConfig_Client:
        """Validates the tool and returns only its config. See `Tool.build_config()`."""
        return typing.cast(
            ToolRequestModelToolConfig_Client, self._construct(ToolRequestModelToolConfig_Client, on_warning)
        )

    def _allowed_options(self) -> typing.Tuple[str, ...]:
        return _CLIENT_OPTIONS

    def _validate(self) -> typing.List[ToolIssue]:
        issues: typing.List[ToolIssue] = []
        if self._parameters is not None:
            # Checks the params object's own require_any_of()/require_all_of() and every param under it.
            check_schema(self._parameters, "params", False, issues)
        timeout = self._config.get("response_timeout_secs")
        if timeout is not None and timeout != -1 and (timeout < 1 or timeout > 120):
            issues.append(
                error(
                    "invalid_option",
                    "response_timeout_secs",
                    "A client tool's response_timeout_secs must be 1-120, or -1",
                )
            )
        if timeout == -1 and self._config.get("expects_response") is not True:
            issues.append(
                error("invalid_option", "response_timeout_secs", "response_timeout_secs=-1 needs expects_response=True")
            )
        return issues

    def _to_wire(self) -> WireDict:
        wire: WireDict = {**self._config, "type": "client"}
        if self._parameters is not None:
            wire["parameters"] = self._parameters._to_wire()
        return wire


class SystemTool(Tool):
    """A built-in tool the agent runs itself, such as ending the call or transferring it."""

    kind: ToolKind = "system"

    def __init__(self, system_tool_type: str, config: WireDict, params: WireDict) -> None:
        super().__init__(config)
        self.system_tool_type = system_tool_type
        """The API's `system_tool_type`, for example `"end_call"`."""
        self._params = params

    @staticmethod
    def end_call() -> SystemTool:
        """Lets the agent end the call."""
        return SystemTool._create("end_call", {})

    @staticmethod
    def skip_turn(*, wait_timeout_secs: typing.Optional[int] = None) -> SystemTool:
        """
        Lets the agent stay quiet when the user asks for a moment. `wait_timeout_secs` is how long to wait before
        the agent checks in; -1 waits for the user.
        """
        return SystemTool._create("skip_turn", {"wait_timeout_secs": wait_timeout_secs})

    @staticmethod
    def language_detection(*, only_at_conversation_start: typing.Optional[bool] = None) -> SystemTool:
        """Lets the agent switch language. `only_at_conversation_start` limits it to the first two user turns."""
        return SystemTool._create("language_detection", {"only_at_conversation_start": only_at_conversation_start})

    @staticmethod
    def play_keypad_touch_tone(
        *,
        use_out_of_band_dtmf: typing.Optional[bool] = None,
        suppress_turn_after_dtmf: typing.Optional[bool] = None,
    ) -> SystemTool:
        """
        Lets the agent play keypad tones, for phone menus. `use_out_of_band_dtmf` sends them as RTP events instead
        of in-band audio (SIP trunk numbers only); `suppress_turn_after_dtmf` keeps the agent quiet afterwards, so
        speech doesn't confuse an IVR.
        """
        return SystemTool._create(
            "play_keypad_touch_tone",
            {"use_out_of_band_dtmf": use_out_of_band_dtmf, "suppress_turn_after_dtmf": suppress_turn_after_dtmf},
        )

    @staticmethod
    def voicemail_detection(*, voicemail_message: typing.Optional[str] = None) -> SystemTool:
        """Lets the agent detect voicemail and leave `voicemail_message`, or hang up if there is none."""
        return SystemTool._create("voicemail_detection", {"voicemail_message": voicemail_message})

    @staticmethod
    def knowledge_base(*, enabled_strategies: typing.Optional[typing.Sequence[SearchStrategy]] = None) -> SystemTool:
        """Lets the agent search its knowledge base."""
        return SystemTool._create(
            "knowledge_base", {"enabled_strategies": None if enabled_strategies is None else list(enabled_strategies)}
        )

    @staticmethod
    def transfer_to_number(*, enable_client_message: typing.Optional[bool] = None) -> SystemTool:
        """
        Lets the agent transfer the call to a phone number or SIP URI. Add destinations with `transfer()`.
        `enable_client_message` plays a message to the caller while they wait.
        """
        return SystemTool._create(
            "transfer_to_number", {"enable_client_message": enable_client_message, "transfers": []}
        )

    @staticmethod
    def transfer_to_agent() -> SystemTool:
        """Lets the agent hand the conversation to another agent. Add destinations with `transfer()`."""
        return SystemTool._create("transfer_to_agent", {"transfers": []})

    @staticmethod
    def _create(system_tool_type: str, params: WireDict) -> SystemTool:
        return SystemTool(
            system_tool_type,
            {"name": system_tool_type},
            {key: value for key, value in params.items() if value is not None},
        )

    def transfer(
        self,
        condition: str,
        destination: Destination,
        *,
        transfer_type: typing.Optional[TransferTypeEnum] = None,
        custom_sip_headers: typing.Optional[typing.Sequence[PhoneNumberTransferCustomSipHeadersItem]] = None,
        sip_refer_play_dialtone: typing.Optional[bool] = None,
        uui: typing.Optional[UuiTransferConfig] = None,
        post_dial_digits: typing.Optional[PhoneNumberTransferPostDialDigits] = None,
        delay_ms: typing.Optional[int] = None,
        transfer_message: typing.Optional[str] = None,
        enable_transferred_agent_first_message: typing.Optional[bool] = None,
        preserve_client_tts_overrides: typing.Optional[bool] = None,
        preserve_voice_settings: typing.Optional[bool] = None,
    ) -> SystemTool:
        """
        Adds a destination to a transfer tool. `condition` is plain text telling the LLM when to transfer there.
        `transfer_to_number` takes phone and SIP destinations, with `transfer_type`, `custom_sip_headers`,
        `sip_refer_play_dialtone`, `uui` and `post_dial_digits`; a SIP URI needs `transfer_type="sip_refer"`.
        `transfer_to_agent` takes agent destinations, with the other options.
        """
        given = {
            "transfer_type": transfer_type,
            "custom_sip_headers": custom_sip_headers,
            "sip_refer_play_dialtone": sip_refer_play_dialtone,
            "uui": uui,
            "post_dial_digits": post_dial_digits,
            "delay_ms": delay_ms,
            "transfer_message": transfer_message,
            "enable_transferred_agent_first_message": enable_transferred_agent_first_message,
            "preserve_client_tts_overrides": preserve_client_tts_overrides,
            "preserve_voice_settings": preserve_voice_settings,
        }
        options = {key: to_wire(value) for key, value in given.items() if value is not None}
        model = destination.to_wire()
        to_number = self.system_tool_type == "transfer_to_number"
        if not to_number and self.system_tool_type != "transfer_to_agent":
            self._issues.append(
                error(
                    "invalid_option",
                    "transfer",
                    f"transfer() only applies to transfer tools, not {self.system_tool_type}",
                )
            )
            return self
        if (model.get("type") == "phone_number") != to_number:
            self._issues.append(
                error(
                    "invalid_destination",
                    "transfer",
                    f'transfer_to_number() needs a phone or SIP destination, not an agent ("{condition}")'
                    if to_number
                    else f'transfer_to_agent() needs an agent destination ("{condition}")',
                )
            )
            return self
        allowed = _PHONE_TRANSFER_OPTIONS if to_number else _AGENT_TRANSFER_OPTIONS
        for key in options:
            if key not in allowed:
                self._issues.append(
                    error("invalid_option", key, f'Option "{key}" doesn\'t apply to {self.system_tool_type}')
                )
        settings = {key: value for key, value in options.items() if key in allowed}
        target = {key: value for key, value in model.items() if key != "type"}
        # A SIP URI held in a dynamic variable resolves to a SIP URI too, so it also needs SIP REFER.
        destination_type = (target.get("transfer_destination") or {}).get("type")
        if destination_type in ("sip_uri", "sip_uri_dynamic_variable") and settings.get("transfer_type") != "sip_refer":
            self._issues.append(
                error(
                    "invalid_destination",
                    "transfer",
                    f'A SIP URI destination needs transfer_type="sip_refer" ("{condition}")',
                )
            )
            return self
        entry = {**target, **settings, "condition": condition}
        self._params["transfers"] = [*(self._params.get("transfers") or []), entry]
        return self

    def build_config(self, *, on_warning: typing.Optional[OnWarning] = None) -> SystemToolConfigOutput:
        """
        Validates the tool and returns its entry for `prompt.built_in_tools`, for example
        `BuiltInToolsOutput(end_call=SystemTool.end_call().build_config())`. (The `ConversationalConfig` that
        `agents.create()` and `agents.update()` take is built from the generated `...Output` models.)

        Raises
        ------
        ToolValidationError
            Listing every problem, if the tool is invalid.
        """
        return typing.cast(SystemToolConfigOutput, self._construct(SystemToolConfigOutput, on_warning))

    def _allowed_options(self) -> typing.Tuple[str, ...]:
        return _COMMON_OPTIONS

    def _validate(self) -> typing.List[ToolIssue]:
        transfers = self._params.get("transfers")
        if self.system_tool_type in ("transfer_to_number", "transfer_to_agent") and not transfers:
            return [error("no_transfers", "transfer", f"{self.system_tool_type} needs at least one transfer()")]
        return []

    def _to_wire(self) -> WireDict:
        return {
            **self._config,
            "type": "system",
            "params": {"system_tool_type": self.system_tool_type, **self._params},
        }


class _OtherTool(Tool):
    """A loaded tool of a type the builder has no constructor for, such as `mcp`. Kept exactly as loaded."""

    kind: ToolKind = "other"

    def _allowed_options(self) -> typing.Tuple[str, ...]:
        return ()

    def _validate(self) -> typing.List[ToolIssue]:
        return [
            ToolIssue(
                code="unknown_tool_type",
                severity="warning",
                message=(
                    f'Tool "{self.name}" has type "{self._config.get("type")}", which this SDK can\'t edit. It '
                    "round-trips through to_json(), but build()'s output may be rejected by tools.create() and "
                    "tools.update()"
                ),
            )
        ]

    def _to_wire(self) -> WireDict:
        return self._config
