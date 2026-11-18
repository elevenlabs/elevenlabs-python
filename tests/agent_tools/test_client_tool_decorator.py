import asyncio
import json
import typing

import httpx
import pytest
from typing_extensions import Annotated, Literal, NotRequired, Required, TypedDict

from elevenlabs import AsyncElevenLabs, ElevenLabs
from elevenlabs.agent_tools import ClientToolFunction, Param, Schema, Tool, ToolValidationError, client_tool
from elevenlabs.conversational_ai.conversation import ClientTools
from elevenlabs.types import ToolRequestModel


class Address(TypedDict):
    """A postal address.

    Attributes:
        street: Street and house number
        city: City
    """

    street: str
    city: str
    postcode: NotRequired[Annotated[str, Param("Postcode, if the caller knows it")]]


class Preferences(TypedDict, total=False):
    # String annotations: what `from __future__ import annotations` gives you, where __required_keys__ is wrong.
    channel: "Required[Annotated[Literal['email', 'sms'], Param('How to contact the shopper')]]"
    quiet_hours: "Annotated[bool, Param('Only contact during the day')]"


@client_tool(expects_response=True, response_timeout_secs=5)
def add_to_cart(
    sku: str,
    quantity: int = 1,
    size: typing.Optional[Literal["S", "M", "L"]] = None,
    store_id: Annotated[str, Param(from_variable="store_id")] = "",
) -> dict:
    """Add a product to the cart
    and report the new total.

    Args:
        sku: The product SKU, e.g. TSH-0042
        quantity (int): How many
            to add
        size: Clothing size
    """
    return {"sku": sku, "quantity": quantity, "size": size, "store_id": store_id}


def test_matches_the_hand_built_tool() -> None:
    by_hand = (
        Tool.client("add_to_cart", "Add a product to the cart and report the new total.")
        .param("sku", Schema.string().describe("The product SKU, e.g. TSH-0042"))
        .param("quantity", Schema.integer().describe("How many to add").optional())
        .param("size", Schema.string().choices(["S", "M", "L"]).describe("Clothing size").optional())
        .param("store_id", Schema.string().from_variable("store_id").optional())
        .options(expects_response=True, response_timeout_secs=5)
    )
    assert add_to_cart.tool.to_json_string() == by_hand.to_json_string()
    assert isinstance(add_to_cart.tool.build(), ToolRequestModel)


def test_is_still_the_function() -> None:
    assert isinstance(add_to_cart, ClientToolFunction)
    assert add_to_cart("TSH-1", quantity=2)["quantity"] == 2
    assert add_to_cart.__name__ == "add_to_cart"
    assert add_to_cart.name == "add_to_cart"
    assert "Add a product" in (add_to_cart.__doc__ or "")


def test_typed_dicts_lists_and_nesting() -> None:
    @client_tool
    def checkout(
        delivery: Literal["pickup", "home"],
        address: typing.Optional[Address] = None,
        gift_tags: typing.Optional[typing.List[Annotated[str, Param("Name on one tag")]]] = None,
        prefs: typing.Optional[Preferences] = None,
    ) -> None:
        """Start checkout.

        :param delivery: Pick up in store or deliver home
        :param address: Only for home delivery
        :param gift_tags: Names to print on gift tags
        :param prefs: Contact preferences
        """

    params = checkout.tool.to_json()["parameters"]
    assert params["required"] == ["delivery"]
    address = params["properties"]["address"]
    assert address["description"] == "Only for home delivery"
    assert address["required"] == ["street", "city"]
    assert address["properties"]["street"]["description"] == "Street and house number"
    assert params["properties"]["gift_tags"]["items"] == {"description": "Name on one tag", "type": "string"}
    prefs = params["properties"]["prefs"]
    assert prefs["required"] == ["channel"]
    assert prefs["properties"]["channel"]["enum"] == ["email", "sms"]


def test_name_description_and_constant() -> None:
    @client_tool(name="beep", description="Play a sound on the device")
    def play(
        volume: Annotated[float, Param("Volume from 0 to 1")], kind: Annotated[str, Param(constant="beep")]
    ) -> None:
        pass

    config = play.tool.to_json()
    assert (config["name"], config["description"]) == ("beep", "Play a sound on the device")
    assert config["parameters"]["properties"]["volume"] == {"description": "Volume from 0 to 1", "type": "number"}
    assert config["parameters"]["properties"]["kind"] == {"constant_value": "beep", "type": "string"}


def test_no_params() -> None:
    @client_tool
    def ping() -> str:
        """Check the client is alive."""
        return "pong"

    assert "parameters" not in ping.tool.to_json()


def test_validates_when_defined() -> None:
    with pytest.raises(ToolValidationError) as err:

        @client_tool
        def tags(names: typing.List[str]) -> None:
            """Print tags.

            Args:
                names: The names
            """

    assert [i.path for i in err.value.issues] == ["params.names[]"]


@pytest.mark.parametrize(
    "hint, message",
    [
        (dict, "unsupported type"),
        (typing.Union[int, str], r"only Optional\[T\] unions"),
        (Literal[1, 2], "Literal choices must be strings"),
        (list, "lists need an item type"),
    ],
)
def test_rejects_types_the_api_cannot_express(hint: typing.Any, message: str) -> None:
    def f(x: int) -> None:
        """Doc."""

    f.__annotations__["x"] = hint
    with pytest.raises(TypeError, match=message):
        client_tool(f)


def test_rejects_missing_hints_and_docs() -> None:
    def no_hint(x) -> None:  # type: ignore[no-untyped-def]
        """Doc."""

    def no_doc(x: str) -> None:
        pass

    def var_args(*xs: str) -> None:
        """Doc."""

    with pytest.raises(TypeError, match="needs a type hint"):
        client_tool(no_hint)
    with pytest.raises(TypeError, match="docstring or pass description="):
        client_tool(no_doc)
    with pytest.raises(TypeError, match="passable by keyword"):
        client_tool(var_args)


def test_handler_drops_keys_the_function_does_not_take() -> None:
    params = {"tool_call_id": "call_1", "sku": "TSH-1", "quantity": 3}
    assert add_to_cart.handler(params) == {"sku": "TSH-1", "quantity": 3, "size": None, "store_id": ""}

    @client_tool
    def log(message: Annotated[str, Param("What to log")], **rest: typing.Any) -> typing.Dict[str, typing.Any]:
        """Log a line."""
        return rest

    assert log.handler({"tool_call_id": "call_2", "message": "hi"}) == {"tool_call_id": "call_2"}


def test_register_tools_runs_sync_and_async_functions() -> None:
    @client_tool
    async def cart_total(currency: Annotated[str, Param("ISO currency code")] = "EUR") -> str:
        """Read back the cart total."""
        return f"19.99 {currency}"

    tools = ClientTools()
    tools.register_tools(add_to_cart, cart_total)
    assert tools.is_registered("add_to_cart") and tools.is_registered("cart_total")

    async def run() -> typing.Tuple[typing.Any, typing.Any]:
        return (
            await tools.handle("add_to_cart", {"tool_call_id": "c1", "sku": "TSH-1"}),
            await tools.handle("cart_total", {"tool_call_id": "c2", "currency": "USD"}),
        )

    added, total = asyncio.run(run())
    assert added["sku"] == "TSH-1"
    assert total == "19.99 USD"
    tools.stop()


TOOL_RESPONSE = {
    "id": "tool_1",
    "tool_config": {"type": "client", "name": "add_to_cart", "description": "d"},
    "access_info": {"is_creator": True, "creator_name": "a", "creator_email": "a@example.com", "role": "admin"},
    "usage_stats": {"avg_latency_secs": 0.1},
}


def _recording_transport(requests: typing.List[httpx.Request]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=TOOL_RESPONSE)

    return httpx.MockTransport(handler)


def test_tools_create_and_update_take_the_function_or_the_model() -> None:
    requests: typing.List[httpx.Request] = []
    client = ElevenLabs(api_key="test", httpx_client=httpx.Client(transport=_recording_transport(requests)))
    expected = {"tool_config": add_to_cart.tool.to_json()}

    client.conversational_ai.tools.create(request=add_to_cart)
    client.conversational_ai.tools.create(request=add_to_cart.tool.build())
    client.conversational_ai.tools.update("tool_1", request=add_to_cart)

    assert [json.loads(r.content) for r in requests] == [expected] * 3
    assert requests[2].method == "PATCH" and requests[2].url.path.endswith("/tools/tool_1")


def test_tools_create_asks_for_build_on_a_chained_builder() -> None:
    requests: typing.List[httpx.Request] = []
    client = ElevenLabs(api_key="test", httpx_client=httpx.Client(transport=_recording_transport(requests)))
    with pytest.raises(TypeError, match=r"Call build\(\) on the tool builder for 'add_to_cart'"):
        client.conversational_ai.tools.create(request=add_to_cart.tool)  # type: ignore[arg-type]
    assert requests == []


def test_async_tools_create_takes_the_function() -> None:
    requests: typing.List[httpx.Request] = []
    client = AsyncElevenLabs(api_key="test", httpx_client=httpx.AsyncClient(transport=_recording_transport(requests)))

    async def run() -> None:
        await client.conversational_ai.tools.create(request=add_to_cart)
        await client.conversational_ai.tools.update("tool_1", request=add_to_cart)

    asyncio.run(run())
    assert [json.loads(r.content) for r in requests] == [{"tool_config": add_to_cart.tool.to_json()}] * 2


def test_typing_literal_and_typing_extensions_literal_both_work() -> None:
    @client_tool
    def pick(
        a: typing.Literal["x", "y"],
        b: Literal["x", "y"],
    ) -> None:
        """Pick.

        Args:
            a: First
            b: Second
        """

    props = pick.tool.to_json()["parameters"]["properties"]
    assert props["a"]["enum"] == props["b"]["enum"] == ["x", "y"]


def test_docstring_does_not_describe_variable_or_constant_params() -> None:
    @client_tool
    def greet(
        name: Annotated[str, Param(from_variable="user_name")],
        greeting: Annotated[str, Param(constant="hi")],
    ) -> None:
        """Greet the user.

        Args:
            name: The user's name, from the session
            greeting: Always "hi"
        """

    props = greet.tool.to_json()["parameters"]["properties"]
    assert props["name"] == {"dynamic_variable": "user_name", "type": "string"}
    assert props["greeting"] == {"constant_value": "hi", "type": "string"}


def test_param_inside_optional_beats_the_docstring() -> None:
    @client_tool
    def note(
        text: typing.Optional[Annotated[str, Param("From Param")]] = None,
        user: typing.Optional[Annotated[str, Param(from_variable="user_id")]] = None,
    ) -> None:
        """Take a note.

        Args:
            text: From the docstring
            user: Who is writing
        """

    props = note.tool.to_json()["parameters"]["properties"]
    assert props["text"]["description"] == "From Param"
    assert props["user"] == {"dynamic_variable": "user_id", "type": "string"}
