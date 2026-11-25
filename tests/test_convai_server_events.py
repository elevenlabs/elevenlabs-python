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
