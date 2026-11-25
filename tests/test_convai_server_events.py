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
