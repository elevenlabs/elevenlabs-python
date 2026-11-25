import asyncio
from unittest.mock import AsyncMock, MagicMock, call

from elevenlabs.conversational_ai.conversation import AsyncConversation, Conversation

TEST_AGENT_ID = "test_agent"


def assert_delivered(callback_name, messages, expected_args):
    """Feed messages to a Conversation and an AsyncConversation, then check what the callback received."""
    sync_callback = MagicMock()
    conversation = Conversation(
        client=MagicMock(), agent_id=TEST_AGENT_ID, requires_auth=False, **{callback_name: sync_callback}
    )
    try:
        for message in messages:
            conversation._handle_message(message, MagicMock())
    finally:
        conversation.client_tools.stop()
    assert sync_callback.call_args_list == [call(arg) for arg in expected_args]

    async_callback = AsyncMock()

    async def run():
        async_conversation = AsyncConversation(
            client=MagicMock(), agent_id=TEST_AGENT_ID, requires_auth=False, **{callback_name: async_callback}
        )
        try:
            for message in messages:
                await async_conversation._handle_message(message, AsyncMock())
        finally:
            async_conversation.client_tools.stop()

    asyncio.run(run())
    assert async_callback.await_args_list == [call(arg) for arg in expected_args]


def test_agent_response_metadata_reaches_callback():
    event = {"metadata": {"source": "llm", "latency_ms": 120}, "event_id": 3}
    assert_delivered(
        "callback_agent_response_metadata",
        [{"type": "agent_response_metadata", "agent_response_metadata_event": event}],
        [event],
    )


def test_interruption_reaches_callback_in_text_only_mode():
    assert_delivered(
        "callback_interruption",
        [{"type": "interruption", "interruption_event": {"event_id": 7}}],
        [7],
    )


def test_interruption_reaches_audio_interface_and_callback():
    audio_interface = MagicMock()
    callback = MagicMock()
    conversation = Conversation(
        client=MagicMock(),
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=audio_interface,
        callback_interruption=callback,
    )
    try:
        conversation._handle_message({"type": "interruption", "interruption_event": {"event_id": 7}}, MagicMock())
    finally:
        conversation.client_tools.stop()
    audio_interface.interrupt.assert_called_once_with()
    callback.assert_called_once_with(7)


def test_async_interruption_reaches_audio_interface_and_callback():
    audio_interface = AsyncMock()
    callback = AsyncMock()

    async def run():
        conversation = AsyncConversation(
            client=MagicMock(),
            agent_id=TEST_AGENT_ID,
            requires_auth=False,
            audio_interface=audio_interface,
            callback_interruption=callback,
        )
        try:
            await conversation._handle_message(
                {"type": "interruption", "interruption_event": {"event_id": 7}}, AsyncMock()
            )
        finally:
            conversation.client_tools.stop()

    asyncio.run(run())
    audio_interface.interrupt.assert_awaited_once_with()
    callback.assert_awaited_once_with(7)


def test_vad_score_reaches_callback():
    assert_delivered(
        "callback_vad_score",
        [
            {"type": "vad_score", "vad_score_event": {"vad_score": 0.87}},
            {"type": "vad_score", "vad_score_event": {"vad_score": 0}},
        ],
        [0.87, 0.0],
    )


def agent_tool_response(tool_call_id, is_error):
    return {
        "tool_name": "lookup_order",
        "tool_call_id": tool_call_id,
        "tool_type": "webhook",
        "is_error": is_error,
        "is_called": True,
        "event_id": 4,
        "status": "error" if is_error else "success",
    }


def test_agent_tool_response_reaches_callback_with_is_error():
    succeeded = agent_tool_response("call_1", is_error=False)
    failed = agent_tool_response("call_2", is_error=True)
    assert_delivered(
        "callback_agent_tool_response",
        [
            {"type": "agent_tool_response", "agent_tool_response": succeeded},
            {"type": "agent_tool_response", "agent_tool_response": failed},
        ],
        [succeeded, failed],
    )


def test_agent_tool_response_full_payload_reaches_callback():
    payload = {
        **agent_tool_response("call_1", is_error=False),
        "full_tool_result": '{"order": "shipped"}',
        "truncated": False,
    }
    truncated = {
        **agent_tool_response("call_2", is_error=True),
        "full_tool_result": "Internal Server Error <html>",
        "truncated": True,
    }
    assert_delivered(
        "callback_agent_tool_response_full_payload",
        [
            {"type": "agent_tool_response_full_payload", "agent_tool_response_full_payload": payload},
            {"type": "agent_tool_response_full_payload", "agent_tool_response_full_payload": truncated},
        ],
        [payload, truncated],
    )


def test_mcp_tool_call_reaches_callback_for_every_state():
    base = {
        "service_id": "service_1",
        "tool_call_id": "mcp_call_1",
        "tool_name": "search",
        "parameters": {"query": "weather"},
        "timestamp": "2026-11-25T05:00:00Z",
    }
    states = [
        {**base, "state": "loading"},
        {**base, "state": "awaiting_approval", "approval_timeout_secs": 300},
        {**base, "state": "success", "result": [{"type": "text", "text": "Sunny"}]},
        {**base, "state": "failure", "error_message": "Timed out"},
    ]
    assert_delivered(
        "callback_mcp_tool_call",
        [{"type": "mcp_tool_call", "mcp_tool_call": state} for state in states],
        states,
    )


def test_mcp_connection_status_reaches_callback():
    status = {
        "integrations": [
            {"integration_id": "mcp_1", "integration_type": "mcp_server", "is_connected": True, "tool_count": 3},
            {"integration_id": "mcp_2", "integration_type": "mcp_integration", "is_connected": False, "tool_count": 0},
        ]
    }
    assert_delivered(
        "callback_mcp_connection_status",
        [{"type": "mcp_connection_status", "mcp_connection_status": status}],
        [status],
    )
