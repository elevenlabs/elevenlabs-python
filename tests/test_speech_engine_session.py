"""Tests for SpeechEngineSession — mirrors SpeechEngineSession.test.ts."""

import asyncio
import json
import typing

import pytest

from elevenlabs.speech_engine import (
    CLOSE,
    DISCONNECTED,
    ERROR,
    INIT,
    USER_TRANSCRIPT,
    ConversationMessage,
    SpeechEngineSession,
)


# ---------------------------------------------------------------------------
# MockWebSocket
# ---------------------------------------------------------------------------


class MockWebSocket:
    """In-memory WebSocket stand-in backed by an asyncio.Queue."""

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

    # -- test helpers --

    def receive_message(self, msg: typing.Dict[str, typing.Any]) -> None:
        """Inject an incoming message from the "ElevenLabs API"."""
        self._inbox.put_nowait(json.dumps(msg))

    def receive_raw(self, data: str) -> None:
        """Inject raw (possibly invalid) data."""
        self._inbox.put_nowait(data)

    def simulate_disconnect(self) -> None:
        """Simulate a WebSocket disconnection."""
        self._inbox.put_nowait(_CLOSE_SENTINEL)


_CLOSE_SENTINEL = object()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TRANSCRIPT = [
    {"role": "agent", "content": "how can I help you today?"},
    {"role": "user", "content": "I need a pizza"},
]

TRANSCRIPT_2 = [
    {"role": "agent", "content": "how can I help you today?"},
    {"role": "user", "content": "I need a pizza"},
    {"role": "agent", "content": "what size?"},
    {"role": "user", "content": "large"},
]


@pytest.fixture
def ws() -> MockWebSocket:
    return MockWebSocket()


@pytest.fixture
def session(ws: MockWebSocket) -> SpeechEngineSession:
    return SpeechEngineSession(ws)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parsed_sent(ws: MockWebSocket) -> typing.List[typing.Dict[str, typing.Any]]:
    return [json.loads(s) for s in ws.sent]


async def _run_until_idle(session: SpeechEngineSession, ws: MockWebSocket) -> None:
    """Drive the session run loop, then disconnect so it returns."""
    ws.simulate_disconnect()
    await session.run()


# ---------------------------------------------------------------------------
# init event
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_emits_init_with_conversation_id(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    captured = []  # type: typing.List[str]

    async def handler(conversation_id: str) -> None:
        captured.append(conversation_id)

    session.on(INIT, handler)
    ws.receive_message({"type": "init", "conversation_id": "conv_42"})
    await _run_until_idle(session, ws)

    assert captured == ["conv_42"]
    assert session.conversation_id == "conv_42"


# ---------------------------------------------------------------------------
# user_transcript events
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_emits_user_transcript_with_conversation_history(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    captured = []  # type: typing.List[typing.List[ConversationMessage]]

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        captured.append(transcript)

    session.on(USER_TRANSCRIPT, handler)
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 1}
    )
    await _run_until_idle(session, ws)

    assert len(captured) == 1
    assert len(captured[0]) == 2
    assert captured[0][0].role == "agent"
    assert captured[0][0].content == "how can I help you today?"
    assert captured[0][1].role == "user"
    assert captured[0][1].content == "I need a pizza"


@pytest.mark.asyncio
async def test_cancels_previous_handler_on_new_transcript(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    """When a new transcript arrives the previous handler task is cancelled."""
    cancelled = asyncio.Event()

    async def slow_handler(transcript: typing.List[ConversationMessage]) -> None:
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            cancelled.set()
            raise

    session.on(USER_TRANSCRIPT, slow_handler)
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 1}
    )
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT_2, "event_id": 2}
    )
    await _run_until_idle(session, ws)

    assert cancelled.is_set()


# ---------------------------------------------------------------------------
# ping / pong
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_auto_responds_to_ping(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message({"type": "ping"})
    await _run_until_idle(session, ws)

    assert len(ws.sent) == 1
    assert json.loads(ws.sent[0]) == {"type": "pong"}


# ---------------------------------------------------------------------------
# close event (protocol-level)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_emits_close_and_cancels_handler_on_close_message(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    close_called = asyncio.Event()
    cancelled = asyncio.Event()

    async def close_handler() -> None:
        close_called.set()

    async def slow_handler(transcript: typing.List[ConversationMessage]) -> None:
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            cancelled.set()
            raise

    session.on(CLOSE, close_handler)
    session.on(USER_TRANSCRIPT, slow_handler)

    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 1}
    )
    ws.receive_message({"type": "close"})
    await _run_until_idle(session, ws)

    assert close_called.is_set()
    assert cancelled.is_set()


# ---------------------------------------------------------------------------
# error event (protocol-level)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_emits_error_on_protocol_error_message(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    errors = []  # type: typing.List[Exception]

    async def handler(err: Exception) -> None:
        errors.append(err)

    session.on(ERROR, handler)
    ws.receive_message({"type": "error", "message": "something went wrong"})
    await _run_until_idle(session, ws)

    assert len(errors) == 1
    assert isinstance(errors[0], Exception)
    assert str(errors[0]) == "something went wrong"


# ---------------------------------------------------------------------------
# WebSocket-level events
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_emits_disconnected_when_websocket_closes(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    disconnected = asyncio.Event()

    async def handler() -> None:
        disconnected.set()

    session.on(DISCONNECTED, handler)
    ws.simulate_disconnect()
    await session.run()

    assert disconnected.is_set()
    assert not session.is_open


@pytest.mark.asyncio
async def test_cancels_handler_when_websocket_closes(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    cancelled = asyncio.Event()

    async def slow_handler(transcript: typing.List[ConversationMessage]) -> None:
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            cancelled.set()
            raise

    session.on(USER_TRANSCRIPT, slow_handler)
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 1}
    )
    # Give the handler task a moment to start before disconnecting.
    await asyncio.sleep(0)
    ws.simulate_disconnect()
    await session.run()

    # The disconnect triggers _cancel_current in the finally block.
    assert cancelled.is_set()


@pytest.mark.asyncio
async def test_emits_error_on_malformed_json(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    errors = []  # type: typing.List[Exception]

    async def handler(err: Exception) -> None:
        errors.append(err)

    session.on(ERROR, handler)
    ws.receive_raw("not json")
    await _run_until_idle(session, ws)

    assert len(errors) == 1


@pytest.mark.asyncio
async def test_ignores_unknown_message_types(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    errors = []  # type: typing.List[Exception]

    async def handler(err: Exception) -> None:
        errors.append(err)

    session.on(ERROR, handler)
    ws.receive_message({"type": "unknown_future_event", "data": 123})
    await _run_until_idle(session, ws)

    assert len(errors) == 0


# ---------------------------------------------------------------------------
# sendResponse (string)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_sends_string_response_with_event_id_and_is_final(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 5}
    )

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        await session.send_response("The answer is 42")

    session.on(USER_TRANSCRIPT, handler)
    await _run_until_idle(session, ws)

    sent = _parsed_sent(ws)
    assert len(sent) == 2
    assert sent[0] == {
        "type": "agent_response",
        "content": "The answer is 42",
        "event_id": 5,
        "is_final": False,
    }
    assert sent[1] == {
        "type": "agent_response",
        "content": "",
        "event_id": 5,
        "is_final": True,
    }


@pytest.mark.asyncio
async def test_raises_when_sending_after_close(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    session.close()
    with pytest.raises(RuntimeError, match="session is closed"):
        await session.send_response("too late")


# ---------------------------------------------------------------------------
# sendResponse (streaming)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_streams_chunks_with_is_final_false_then_terminator(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 3}
    )

    async def tokens():  # type: ignore[return]
        yield "Hello"
        yield " world"

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        await session.send_response(tokens())

    session.on(USER_TRANSCRIPT, handler)
    await _run_until_idle(session, ws)

    sent = _parsed_sent(ws)
    assert len(sent) == 3
    assert sent[0] == {
        "type": "agent_response",
        "content": "Hello",
        "event_id": 3,
        "is_final": False,
    }
    assert sent[1] == {
        "type": "agent_response",
        "content": " world",
        "event_id": 3,
        "is_final": False,
    }
    assert sent[2] == {
        "type": "agent_response",
        "content": "",
        "event_id": 3,
        "is_final": True,
    }


@pytest.mark.asyncio
async def test_stops_streaming_when_session_closed_mid_stream(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 7}
    )

    async def slow_tokens():  # type: ignore[return]
        yield "first"
        yield "second"
        await asyncio.sleep(0.1)
        yield "third"

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        await session.send_response(slow_tokens())

    session.on(USER_TRANSCRIPT, handler)

    # Start the run loop in the background.
    task = asyncio.create_task(session.run())
    # Let the handler task progress through the first two yields.
    await asyncio.sleep(0.05)
    session.close()
    await asyncio.sleep(0.15)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    sent = _parsed_sent(ws)
    chunks = [m for m in sent if m.get("type") == "agent_response"]
    # "first" and "second" are sent; session closes before "third".
    assert len(chunks) == 2
    assert chunks[0] == {
        "type": "agent_response",
        "content": "first",
        "event_id": 7,
        "is_final": False,
    }
    assert chunks[1] == {
        "type": "agent_response",
        "content": "second",
        "event_id": 7,
        "is_final": False,
    }


# ---------------------------------------------------------------------------
# sendResponse (LLM stream formats)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_extracts_text_from_openai_responses_api(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 10}
    )

    async def openai_responses_stream():  # type: ignore[return]
        yield {"type": "response.created", "response": {}}
        yield {"type": "response.output_text.delta", "delta": "Hello"}
        yield {"type": "response.output_text.delta", "delta": " world"}
        yield {"type": "response.output_text.done", "text": "Hello world"}
        yield {"type": "response.completed", "response": {}}

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        await session.send_response(openai_responses_stream())

    session.on(USER_TRANSCRIPT, handler)
    await _run_until_idle(session, ws)

    sent = _parsed_sent(ws)
    assert len(sent) == 3
    assert sent[0] == {
        "type": "agent_response",
        "content": "Hello",
        "event_id": 10,
        "is_final": False,
    }
    assert sent[1] == {
        "type": "agent_response",
        "content": " world",
        "event_id": 10,
        "is_final": False,
    }
    assert sent[2] == {
        "type": "agent_response",
        "content": "",
        "event_id": 10,
        "is_final": True,
    }


@pytest.mark.asyncio
async def test_extracts_text_from_openai_chat_completions_api(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 11}
    )

    async def openai_chat_stream():  # type: ignore[return]
        yield {"choices": [{"delta": {"role": "assistant"}}]}
        yield {"choices": [{"delta": {"content": "Hi"}}]}
        yield {"choices": [{"delta": {"content": " there"}}]}
        yield {"choices": [{"delta": {}}]}

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        await session.send_response(openai_chat_stream())

    session.on(USER_TRANSCRIPT, handler)
    await _run_until_idle(session, ws)

    sent = _parsed_sent(ws)
    assert len(sent) == 3
    assert sent[0] == {
        "type": "agent_response",
        "content": "Hi",
        "event_id": 11,
        "is_final": False,
    }
    assert sent[1] == {
        "type": "agent_response",
        "content": " there",
        "event_id": 11,
        "is_final": False,
    }
    assert sent[2] == {
        "type": "agent_response",
        "content": "",
        "event_id": 11,
        "is_final": True,
    }


@pytest.mark.asyncio
async def test_extracts_text_from_anthropic_messages_api(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 12}
    )

    async def anthropic_stream():  # type: ignore[return]
        yield {"type": "message_start", "message": {}}
        yield {"type": "content_block_start", "content_block": {"type": "text", "text": ""}}
        yield {"type": "content_block_delta", "delta": {"type": "text_delta", "text": "Good"}}
        yield {"type": "content_block_delta", "delta": {"type": "text_delta", "text": " morning"}}
        yield {"type": "content_block_stop"}
        yield {"type": "message_stop"}

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        await session.send_response(anthropic_stream())

    session.on(USER_TRANSCRIPT, handler)
    await _run_until_idle(session, ws)

    sent = _parsed_sent(ws)
    assert len(sent) == 3
    assert sent[0] == {
        "type": "agent_response",
        "content": "Good",
        "event_id": 12,
        "is_final": False,
    }
    assert sent[1] == {
        "type": "agent_response",
        "content": " morning",
        "event_id": 12,
        "is_final": False,
    }
    assert sent[2] == {
        "type": "agent_response",
        "content": "",
        "event_id": 12,
        "is_final": True,
    }


@pytest.mark.asyncio
async def test_extracts_text_from_gemini_api(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 13}
    )

    async def gemini_stream():  # type: ignore[return]
        yield {"candidates": [{"content": {"parts": [{"text": "Hey"}], "role": "model"}}]}
        yield {"candidates": [{"content": {"parts": [{"text": " buddy"}], "role": "model"}}]}

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        await session.send_response(gemini_stream())

    session.on(USER_TRANSCRIPT, handler)
    await _run_until_idle(session, ws)

    sent = _parsed_sent(ws)
    assert len(sent) == 3
    assert sent[0] == {
        "type": "agent_response",
        "content": "Hey",
        "event_id": 13,
        "is_final": False,
    }
    assert sent[1] == {
        "type": "agent_response",
        "content": " buddy",
        "event_id": 13,
        "is_final": False,
    }
    assert sent[2] == {
        "type": "agent_response",
        "content": "",
        "event_id": 13,
        "is_final": True,
    }


@pytest.mark.asyncio
async def test_skips_unrecognized_stream_events(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 14}
    )

    async def mixed_stream():  # type: ignore[return]
        yield {"type": "unknown_event", "data": 123}
        yield {"type": "response.output_text.delta", "delta": "text"}
        yield 42
        yield None

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        await session.send_response(mixed_stream())

    session.on(USER_TRANSCRIPT, handler)
    await _run_until_idle(session, ws)

    sent = _parsed_sent(ws)
    assert len(sent) == 2
    assert sent[0] == {
        "type": "agent_response",
        "content": "text",
        "event_id": 14,
        "is_final": False,
    }
    assert sent[1] == {
        "type": "agent_response",
        "content": "",
        "event_id": 14,
        "is_final": True,
    }


# ---------------------------------------------------------------------------
# event_id tracking across interrupts
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_stamps_correct_event_id_after_interrupt(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 1}
    )
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT_2, "event_id": 2}
    )

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        # Non-blocking so both handlers complete within the run loop.
        await session.send_response("response")

    session.on(USER_TRANSCRIPT, handler)
    await _run_until_idle(session, ws)

    sent = _parsed_sent(ws)
    # Each sendResponse emits content + terminator = 2 messages.
    # The first handler's task may or may not complete before cancellation;
    # the second handler's response should use event_id 2.
    # Filter to the final handler's messages (event_id=2):
    id2 = [m for m in sent if m.get("event_id") == 2]
    assert len(id2) == 2
    assert id2[0]["content"] == "response"
    assert id2[0]["is_final"] is False
    assert id2[1]["content"] == ""
    assert id2[1]["is_final"] is True


# ---------------------------------------------------------------------------
# close()
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_close_is_idempotent(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    session.close()
    session.close()
    assert not session.is_open


# ---------------------------------------------------------------------------
# Event constants
# ---------------------------------------------------------------------------


def test_event_constants() -> None:
    assert INIT == "init"
    assert USER_TRANSCRIPT == "user_transcript"
    assert CLOSE == "close"
    assert ERROR == "error"
    assert DISCONNECTED == "disconnected"


# ---------------------------------------------------------------------------
# on / off / once
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_off_removes_handler(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    calls = []  # type: typing.List[str]

    async def handler(conversation_id: str) -> None:
        calls.append(conversation_id)

    session.on(INIT, handler)
    session.off(INIT, handler)

    ws.receive_message({"type": "init", "conversation_id": "conv_1"})
    await _run_until_idle(session, ws)

    assert calls == []


@pytest.mark.asyncio
async def test_once_fires_only_once(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    calls = []  # type: typing.List[str]

    async def handler(conversation_id: str) -> None:
        calls.append(conversation_id)

    session.once(INIT, handler)

    ws.receive_message({"type": "init", "conversation_id": "conv_1"})
    ws.receive_message({"type": "init", "conversation_id": "conv_2"})
    await _run_until_idle(session, ws)

    assert calls == ["conv_1"]


# ---------------------------------------------------------------------------
# Transcript deduplication
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_skips_duplicate_event_id(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    """Duplicate transcripts with the same event_id are ignored."""
    call_count = 0

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.5)

    session.on(USER_TRANSCRIPT, handler)
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 30}
    )
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 30}
    )
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 30}
    )
    await _run_until_idle(session, ws)

    assert call_count == 1


@pytest.mark.asyncio
async def test_does_not_skip_different_event_id(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    """Different event_ids are processed normally."""
    call_count = 0

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        nonlocal call_count
        call_count += 1

    session.on(USER_TRANSCRIPT, handler)
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT, "event_id": 1}
    )
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT_2, "event_id": 2}
    )
    await _run_until_idle(session, ws)

    assert call_count == 2


@pytest.mark.asyncio
async def test_does_not_deduplicate_when_event_id_is_none(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    """Transcripts without event_id should never be deduplicated."""
    call_count = 0

    async def handler(transcript: typing.List[ConversationMessage]) -> None:
        nonlocal call_count
        call_count += 1

    session.on(USER_TRANSCRIPT, handler)
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT}
    )
    ws.receive_message(
        {"type": "user_transcript", "user_transcript": TRANSCRIPT_2}
    )
    await _run_until_idle(session, ws)

    assert call_count == 2


# ---------------------------------------------------------------------------
# send_response outside on_transcript
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_send_response_warns_outside_transcript(
    ws: MockWebSocket, session: SpeechEngineSession
) -> None:
    """send_response before any transcript should warn and not send."""
    await session.send_response("hello")
    assert len(ws.sent) == 0
