import asyncio
import typing
import warnings

import httpx
import pytest
from typing_extensions import Annotated, Literal

from elevenlabs import AsyncElevenLabs, ElevenLabs
from elevenlabs.agent_tools import Param, ToolSchemaDriftError, ToolSchemaDriftWarning, client_tool


@client_tool(expects_response=True)
def add_to_cart(
    sku: str,
    quantity: int = 1,
    size: typing.Optional[Literal["S", "M", "L"]] = None,
    store_id: Annotated[str, Param(from_variable="store_id")] = "",
) -> dict:
    """Add a product to the cart.

    Args:
        sku: The product SKU
        quantity: How many to add
        size: Clothing size
    """
    return {}


def _prop(type_: str, **extra: typing.Any) -> typing.Dict[str, typing.Any]:
    # The server fills unset fields with defaults; the comparison has to ignore them.
    return {"type": type_, "description": "server text", "dynamic_variable": "", "constant_value": "", **extra}


def _server_tool(name: str, properties: typing.Dict[str, typing.Any], required: typing.List[str]) -> typing.Any:
    return {
        "id": f"tool_{name}",
        "tool_config": {
            "type": "client",
            "name": name,
            "description": "d",
            "expects_response": True,
            "response_timeout_secs": 20,
            "parameters": {"type": "object", "properties": properties, "required": required, "description": ""},
        },
        "access_info": {"is_creator": True, "creator_name": "a", "creator_email": "a@example.com", "role": "admin"},
        "usage_stats": {"avg_latency_secs": 0.1},
    }


MATCHING = _server_tool(
    "add_to_cart",
    {
        "sku": _prop("string"),
        "quantity": _prop("integer"),
        "size": _prop("string", enum=["L", "M", "S"]),
        "store_id": {"type": "string", "dynamic_variable": "store_id", "description": "", "constant_value": ""},
    },
    ["sku"],
)


def _client(pages: typing.List[typing.Any], seen: typing.List[httpx.Request]) -> ElevenLabs:
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=pages[len(seen) - 1])

    return ElevenLabs(api_key="test", httpx_client=httpx.Client(transport=httpx.MockTransport(handler)))


def test_matching_tool_reports_nothing() -> None:
    seen: typing.List[httpx.Request] = []
    client = _client([{"tools": [MATCHING], "has_more": False}], seen)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert client.conversational_ai.tools.check_client_tools("agent_1", add_to_cart) == []
    assert seen[0].url.params["used_by_agent_id"] == "agent_1"


def test_reports_each_difference_and_warns() -> None:
    drifted = _server_tool(
        "add_to_cart",
        {
            "sku": _prop("integer"),
            "qty": _prop("integer"),
            "size": _prop("string", enum=["S", "M"]),
            "store_id": _prop("string"),
        },
        ["sku", "qty", "store_id"],
    )
    client = _client([{"tools": [drifted], "has_more": False}], [])
    with pytest.warns(ToolSchemaDriftWarning) as caught:
        drift = client.conversational_ai.tools.check_client_tools("agent_1", add_to_cart)

    assert {d.path: d.message for d in drift} == {
        "sku": "param 'sku' is integer on the server but string in the function",
        "quantity": "'quantity' is in the function but not on the server, so the agent never sends it: "
        "it always gets its default",
        "size": "param 'size' allows 'S', 'M' on the server but 'S', 'M', 'L' in the function",
        "store_id": "'store_id' is required on the server but optional in the function",
        "qty": "'qty' is on the server but not in the function, so the function never receives it",
    }
    assert len(caught) == len(drift)


def test_missing_tool_and_pagination() -> None:
    @client_tool
    def ping() -> str:
        """Check the client is alive."""
        return "pong"

    seen: typing.List[httpx.Request] = []
    pages = [
        {"tools": [], "has_more": True, "next_cursor": "c2"},
        {"tools": [MATCHING, _server_tool("ping", {}, [])], "has_more": False},
    ]
    client = _client(pages, seen)

    @client_tool
    def checkout() -> None:
        """Start checkout."""

    with pytest.warns(ToolSchemaDriftWarning):
        drift = client.conversational_ai.tools.check_client_tools("agent_1", add_to_cart, ping, checkout)
    assert [str(d) for d in drift] == [
        "checkout: the agent has no client tool with this name, so it never calls the function"
    ]
    assert seen[1].url.params["cursor"] == "c2"


def test_nested_objects_and_lists() -> None:
    class Address(typing.TypedDict):
        street: Annotated[str, Param("Street")]
        city: Annotated[str, Param("City")]

    @client_tool
    def ship(
        address: Annotated[Address, Param("Where to")],
        tags: Annotated[typing.List[Annotated[str, Param("A tag")]], Param("Tags")],
    ) -> None:
        """Ship it."""

    server = _server_tool(
        "ship",
        {
            "address": {
                "type": "object",
                "description": "",
                "properties": {"street": _prop("string")},
                "required": ["street"],
            },
            "tags": {"type": "array", "description": "", "items": _prop("integer")},
        },
        ["address", "tags"],
    )
    client = _client([{"tools": [server], "has_more": False}], [])
    with pytest.warns(ToolSchemaDriftWarning):
        drift = client.conversational_ai.tools.check_client_tools("agent_1", ship)
    assert [(d.path, d.message) for d in drift] == [
        (
            "address.city",
            "'address.city' is in the function but not on the server, so the agent never sends it: "
            "the call fails because it's required",
        ),
        ("tags[]", "param 'tags[]' is integer on the server but string in the function"),
    ]


def test_strict_raises() -> None:
    client = _client([{"tools": [], "has_more": False}], [])
    with pytest.raises(ToolSchemaDriftError, match="add_to_cart: the agent has no client tool"):
        client.conversational_ai.tools.check_client_tools("agent_1", add_to_cart, strict=True)


def test_async() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"tools": [MATCHING], "has_more": False})

    client = AsyncElevenLabs(api_key="test", httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    assert asyncio.run(client.conversational_ai.tools.check_client_tools("agent_1", add_to_cart)) == []
