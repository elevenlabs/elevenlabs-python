"""Tests for SpeechEngineResource — mirrors SpeechEngineResource.test.ts."""

import asyncio
import json
import typing

import pytest

from elevenlabs.speech_engine import SpeechEngineResource, SpeechEngineSession


# ---------------------------------------------------------------------------
# MockWebSocket (same as session tests)
# ---------------------------------------------------------------------------

_CLOSE_SENTINEL = object()


class MockWebSocket:
    def __init__(self) -> None:
        self._inbox = asyncio.Queue()  # type: asyncio.Queue[typing.Any]
        self.sent = []  # type: typing.List[str]
        self.closed = False

    async def recv(self) -> str:
        msg = await self._inbox.get()
        if msg is _CLOSE_SENTINEL:
            raise ConnectionError("connection closed")
        return msg

    async def send(self, data: str) -> None:
        self.sent.append(data)

    async def close(self) -> None:
        self.closed = True

    def receive_message(self, msg: typing.Dict[str, typing.Any]) -> None:
        self._inbox.put_nowait(json.dumps(msg))

    def simulate_disconnect(self) -> None:
        self._inbox.put_nowait(_CLOSE_SENTINEL)


# ---------------------------------------------------------------------------
# create_session
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_session_returns_speech_engine_session() -> None:
    resource = SpeechEngineResource("seng_test")
    ws = MockWebSocket()
    session = resource.create_session(ws)
    assert isinstance(session, SpeechEngineSession)


@pytest.mark.asyncio
async def test_create_session_protocol_works() -> None:
    """Full send/receive cycle through a session created by the resource."""
    resource = SpeechEngineResource("seng_test")
    ws = MockWebSocket()
    session = resource.create_session(ws, debug=False)

    async def handler(transcript: typing.Any) -> None:
        last = transcript[-1]
        await session.send_response("echo: {}".format(last.content))

    session.on("user_transcript", handler)

    ws.receive_message(
        {
            "type": "user_transcript",
            "user_transcript": [{"role": "user", "content": "hello"}],
            "event_id": 1,
        }
    )
    ws.simulate_disconnect()
    await session.run()

    sent = [json.loads(s) for s in ws.sent]
    assert sent[0] == {
        "type": "agent_response",
        "content": "echo: hello",
        "event_id": 1,
        "is_final": False,
    }


# ---------------------------------------------------------------------------
# client accessor stub
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_client_speech_engine_get() -> None:
    """The AsyncElevenLabs.speech_engine.get() stub returns a resource."""
    from elevenlabs import AsyncElevenLabs

    client = AsyncElevenLabs(api_key="test-key")
    resource = await client.speech_engine.get("seng_123")

    assert isinstance(resource, SpeechEngineResource)
    assert resource.engine_id == "seng_123"
