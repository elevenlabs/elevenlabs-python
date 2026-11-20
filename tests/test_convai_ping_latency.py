import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from elevenlabs.conversational_ai.conversation import AsyncConversation, Conversation


@pytest.mark.parametrize(
    "event",
    [
        {"event_id": 123},
        {"event_id": 123, "ping_ms": None},
        {"event_id": 123, "ping_ms": 0},
        {"event_id": 123, "ping_ms": 50},
    ],
)
def test_sync_ping_optional_latency(event):
    tools = MagicMock()
    callback = MagicMock()
    response = MagicMock()
    conversation = Conversation(
        client=MagicMock(),
        agent_id="test-agent",
        requires_auth=False,
        client_tools=tools,
        callback_latency_measurement=callback,
        callback_agent_response=response,
    )
    ws = MagicMock()
    conversation._handle_message({"type": "ping", "ping_event": event}, ws)
    ws.send.assert_called_once_with(json.dumps({"type": "pong", "event_id": 123}))
    if event.get("ping_ms") is None:
        callback.assert_not_called()
    else:
        callback.assert_called_once_with(event["ping_ms"])
    conversation._handle_message(
        {"type": "agent_response", "agent_response_event": {"agent_response": "still connected"}}, ws
    )
    response.assert_called_once_with("still connected")


@pytest.mark.parametrize(
    "event",
    [
        {"event_id": 123},
        {"event_id": 123, "ping_ms": None},
        {"event_id": 123, "ping_ms": 0},
        {"event_id": 123, "ping_ms": 50},
    ],
)
async def test_async_ping_optional_latency(event):
    tools = MagicMock()
    callback = AsyncMock()
    response = AsyncMock()
    conversation = AsyncConversation(
        client=MagicMock(),
        agent_id="test-agent",
        requires_auth=False,
        client_tools=tools,
        callback_latency_measurement=callback,
        callback_agent_response=response,
    )
    ws = AsyncMock()
    await conversation._handle_message({"type": "ping", "ping_event": event}, ws)
    ws.send.assert_awaited_once_with(json.dumps({"type": "pong", "event_id": 123}))
    if event.get("ping_ms") is None:
        callback.assert_not_awaited()
    else:
        callback.assert_awaited_once_with(event["ping_ms"])
    await conversation._handle_message(
        {"type": "agent_response", "agent_response_event": {"agent_response": "still connected"}}, ws
    )
    response.assert_awaited_once_with("still connected")
