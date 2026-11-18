import json
import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from elevenlabs.conversational_ai.conversation import AsyncConversation, Conversation

TEST_AGENT_ID = "test_agent"

# Every subscribe message on /v1/convai/conversation in the published AsyncAPI document.
SERVER_MESSAGES = [
    {"type": "conversation_initiation_metadata", "conversation_initiation_metadata_event": {"conversation_id": "conv_1"}},
    {"type": "user_transcript", "user_transcription_event": {"user_transcript": "Hello"}},
    {"type": "agent_response", "agent_response_event": {"agent_response": "Hi there"}},
    {"type": "agent_chat_response_part", "text_response_part": {"text": "Hi", "type": "delta"}},
    {"type": "agent_response_correction", "agent_response_correction_event": {"original_agent_response": "Hi there", "corrected_agent_response": "Hi"}},
    {"type": "agent_response_metadata", "agent_response_metadata_event": {"event_id": 1}},
    {"type": "agent_response_complete", "agent_response_complete_event": {"event_id": 1}},
    {"type": "audio", "audio_event": {"event_id": 2, "audio_base_64": "AAAA"}},
    {"type": "interruption", "interruption_event": {"event_id": 3}},
    {"type": "vad_score", "vad_score_event": {"vad_score": 0.5}},
    {"type": "ping", "ping_event": {"event_id": 4, "ping_ms": 20}},
    {"type": "client_tool_call", "client_tool_call": {"tool_name": "unregistered_tool", "tool_call_id": "tool_call_1", "parameters": {}, "expects_response": True}},
    {"type": "agent_tool_request", "agent_tool_request": {"tool_name": "search", "tool_call_id": "tool_call_2"}},
    {"type": "agent_tool_response", "agent_tool_response": {"tool_name": "search", "tool_call_id": "tool_call_2"}},
    {"type": "agent_tool_response_full_payload", "agent_tool_response_full_payload": {"tool_call_id": "tool_call_2"}},
    {"type": "mcp_tool_call", "mcp_tool_call": {"tool_call_id": "tool_call_3"}},
    {"type": "mcp_connection_status", "mcp_connection_status": {"integrations": []}},
    {"type": "context_usage", "context_usage_event": {"used_tokens": 10}},
    {"type": "guardrail_triggered", "guardrail_triggered_event": {}},
    {"type": "queue_status", "queue_status_event": {"position": 1}},
    {"type": "client_error", "client_error_event": {"message": "bad request"}},
]


def wait_for(predicate, timeout=5.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return False


def sent_types(ws):
    return [json.loads(call[0][0])["type"] for call in ws.send.call_args_list]


def test_message_received_callback_gets_every_server_message():
    received = []
    conversation = Conversation(
        client=MagicMock(),
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=MagicMock(),
        callback_message_received=received.append,
    )
    ws = MagicMock()

    try:
        for message in SERVER_MESSAGES:
            conversation._handle_message(message, ws)
        assert wait_for(lambda: "client_tool_result" in sent_types(ws)), "Agent did not receive a client_tool_result"
    finally:
        conversation.client_tools.stop()

    assert received == SERVER_MESSAGES
    ws.send.assert_any_call(json.dumps({"type": "pong", "event_id": 4}))


def test_message_received_callback_runs_after_dedicated_callback():
    calls = []
    conversation = Conversation(
        client=MagicMock(),
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        callback_agent_response=lambda response: calls.append(("agent_response", response)),
        callback_message_received=lambda message: calls.append(("message", message["type"])),
    )

    try:
        conversation._handle_message({"type": "agent_response", "agent_response_event": {"agent_response": "Hi"}}, MagicMock())
    finally:
        conversation.client_tools.stop()

    assert calls == [("agent_response", "Hi"), ("message", "agent_response")]


def test_message_received_callback_gets_audio_dropped_after_interruption():
    audio_interface = MagicMock()
    received = []
    conversation = Conversation(
        client=MagicMock(),
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=audio_interface,
        callback_message_received=received.append,
    )
    stale_audio = {"type": "audio", "audio_event": {"event_id": 1, "audio_base_64": "AAAA"}}

    try:
        conversation._handle_message({"type": "interruption", "interruption_event": {"event_id": 2}}, MagicMock())
        conversation._handle_message(stale_audio, MagicMock())
    finally:
        conversation.client_tools.stop()

    audio_interface.output.assert_not_called()
    assert received[-1] == stale_audio


@pytest.mark.asyncio
async def test_async_message_received_callback_gets_every_server_message():
    received = []

    async def on_message(message):
        received.append(message)

    conversation = AsyncConversation(
        client=MagicMock(),
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=AsyncMock(),
        callback_message_received=on_message,
    )
    ws = AsyncMock()

    try:
        for message in SERVER_MESSAGES:
            await conversation._handle_message(message, ws)
        assert wait_for(lambda: ws.send.await_count == 2), "Agent did not receive a pong and a client_tool_result"
    finally:
        conversation.client_tools.stop()

    assert received == SERVER_MESSAGES
    ws.send.assert_any_await(json.dumps({"type": "pong", "event_id": 4}))
