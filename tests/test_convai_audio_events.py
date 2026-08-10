import base64
from unittest.mock import AsyncMock, MagicMock

import pytest

from elevenlabs.conversational_ai.conversation import BaseConversation


def _conversation_with_interrupt(event_id: int) -> BaseConversation:
    conversation = BaseConversation.__new__(BaseConversation)
    conversation._last_interrupt_id = event_id
    return conversation


def _audio_message(event_id: int) -> dict:
    return {
        "type": "audio",
        "audio_event": {
            "event_id": str(event_id),
            "audio_base_64": base64.b64encode(b"reply audio").decode("ascii"),
        },
    }


def _interruption_message(event_id: int) -> dict:
    return {
        "type": "interruption",
        "interruption_event": {"event_id": str(event_id)},
    }


def test_sync_conversation_keeps_audio_with_interruption_event_id():
    conversation = _conversation_with_interrupt(0)
    message_handler = MagicMock()
    message_handler.callback_audio_alignment = None

    conversation._handle_message_core(_interruption_message(87), message_handler)
    conversation._handle_message_core(_audio_message(87), message_handler)

    message_handler.handle_audio_output.assert_called_once_with(b"reply audio")


def test_sync_conversation_discards_audio_older_than_interruption():
    conversation = _conversation_with_interrupt(87)
    message_handler = MagicMock()
    message_handler.callback_audio_alignment = None

    conversation._handle_message_core(_audio_message(86), message_handler)

    message_handler.handle_audio_output.assert_not_called()


@pytest.mark.asyncio
async def test_async_conversation_keeps_audio_with_interruption_event_id():
    conversation = _conversation_with_interrupt(0)
    message_handler = MagicMock()
    message_handler.callback_audio_alignment = None
    message_handler.handle_audio_output = AsyncMock()
    message_handler.handle_interruption = AsyncMock()

    await conversation._handle_message_core_async(_interruption_message(87), message_handler)
    await conversation._handle_message_core_async(_audio_message(87), message_handler)

    message_handler.handle_audio_output.assert_awaited_once_with(b"reply audio")


@pytest.mark.asyncio
async def test_async_conversation_discards_audio_older_than_interruption():
    conversation = _conversation_with_interrupt(87)
    message_handler = MagicMock()
    message_handler.callback_audio_alignment = None
    message_handler.handle_audio_output = AsyncMock()

    await conversation._handle_message_core_async(_audio_message(86), message_handler)

    message_handler.handle_audio_output.assert_not_awaited()
