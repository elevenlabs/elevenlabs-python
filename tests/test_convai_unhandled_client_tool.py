import json
import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from elevenlabs.conversational_ai.conversation import AsyncConversation, ClientTools, Conversation

TEST_AGENT_ID = "test_agent"
TOOL_CALL_ID = "tool_call_1"
TOOL_PARAMETERS = {"city": "London"}


def client_tool_call_message(tool_name):
    return {
        "type": "client_tool_call",
        "client_tool_call": {
            "tool_name": tool_name,
            "tool_call_id": TOOL_CALL_ID,
            "parameters": TOOL_PARAMETERS,
            "expects_response": True,
        },
    }


def wait_for(predicate, timeout=5.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return False


def test_unhandled_client_tool_call_invokes_callback():
    client_tools = ClientTools()
    client_tools.register("registered_tool", lambda parameters: "ok")
    unhandled = MagicMock()
    conversation = Conversation(
        client=MagicMock(),
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        client_tools=client_tools,
        callback_unhandled_client_tool_call=unhandled,
    )
    ws = MagicMock()

    try:
        message = client_tool_call_message("unregistered_tool")
        conversation._handle_message(message, ws)

        unhandled.assert_called_once_with(message["client_tool_call"])
        assert wait_for(lambda: ws.send.called), "Agent did not receive a client_tool_result"
        result = json.loads(ws.send.call_args[0][0])
        assert result["type"] == "client_tool_result"
        assert result["tool_call_id"] == TOOL_CALL_ID
        assert result["is_error"] is True
    finally:
        client_tools.stop()


def test_registered_client_tool_call_does_not_invoke_unhandled_callback():
    client_tools = ClientTools()
    client_tools.register("registered_tool", lambda parameters: "ok")
    unhandled = MagicMock()
    conversation = Conversation(
        client=MagicMock(),
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        client_tools=client_tools,
        callback_unhandled_client_tool_call=unhandled,
    )
    ws = MagicMock()

    try:
        conversation._handle_message(client_tool_call_message("registered_tool"), ws)

        assert wait_for(lambda: ws.send.called), "Agent did not receive a client_tool_result"
        assert json.loads(ws.send.call_args[0][0])["is_error"] is False
        unhandled.assert_not_called()
    finally:
        client_tools.stop()


@pytest.mark.asyncio
async def test_async_unhandled_client_tool_call_invokes_callback():
    client_tools = ClientTools()
    client_tools.register("registered_tool", lambda parameters: "ok")
    unhandled = AsyncMock()
    conversation = AsyncConversation(
        client=MagicMock(),
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        client_tools=client_tools,
        callback_unhandled_client_tool_call=unhandled,
    )

    ws = AsyncMock()

    try:
        message = client_tool_call_message("unregistered_tool")
        await conversation._handle_message(message, ws)
        unhandled.assert_awaited_once_with(message["client_tool_call"])

        await conversation._handle_message(client_tool_call_message("registered_tool"), ws)
        assert unhandled.await_count == 1

        assert wait_for(lambda: ws.send.await_count == 2), "Agent did not receive both client_tool_results"
        results = sorted((json.loads(call[0][0]) for call in ws.send.await_args_list), key=lambda r: r["is_error"])
        assert [r["is_error"] for r in results] == [False, True]
    finally:
        client_tools.stop()
