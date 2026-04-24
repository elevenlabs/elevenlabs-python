"""Tests for SpeechEngineServer — mirrors SpeechEngineServer.test.ts."""

import asyncio
import json
import typing

import pytest
import websockets

from elevenlabs.speech_engine import SpeechEngineServer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _connect_and_send(
    port: int,
    messages: typing.List[typing.Dict[str, typing.Any]],
) -> typing.List[typing.Dict[str, typing.Any]]:
    """Open a client WS, send *messages*, and collect the first response."""
    uri = "ws://127.0.0.1:{}".format(port)
    received = []  # type: typing.List[typing.Dict[str, typing.Any]]
    async with websockets.connect(uri) as ws:  # type: ignore[attr-defined]
        for msg in messages:
            await ws.send(json.dumps(msg))
        # Give the server a moment to process and respond.
        try:
            while True:
                raw = await asyncio.wait_for(ws.recv(), timeout=0.2)
                received.append(json.loads(raw))
        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
            pass
    return received


# ---------------------------------------------------------------------------
# handleConnection
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_handle_connection_wraps_ws_and_calls_on_init() -> None:
    init_ids = []  # type: typing.List[str]

    async def on_init(conversation_id: str, session: typing.Any) -> None:
        init_ids.append(conversation_id)

    server = SpeechEngineServer(port=0, on_init=on_init)

    # Use port 0 to get an ephemeral port; start via websockets directly.
    started = asyncio.Event()
    actual_port = 0

    async def _handler(ws: typing.Any, *_args: typing.Any) -> None:
        session = server.handle_connection(ws)
        await session.run()

    ws_server = await websockets.serve(_handler, "127.0.0.1", 0)  # type: ignore[attr-defined]
    for sock in ws_server.sockets:
        actual_port = sock.getsockname()[1]
        break

    try:
        uri = "ws://127.0.0.1:{}".format(actual_port)
        async with websockets.connect(uri) as client:  # type: ignore[attr-defined]
            await client.send(
                json.dumps({"type": "init", "conversation_id": "conv_1"})
            )
            await asyncio.sleep(0.1)
    finally:
        ws_server.close()
        await ws_server.wait_closed()

    assert init_ids == ["conv_1"]


# ---------------------------------------------------------------------------
# Session responses are received by the client
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_session_responses_received_by_client() -> None:
    async def on_transcript(
        transcript: typing.Any, session: typing.Any
    ) -> None:
        last = transcript[-1]
        await session.send_response("echo: {}".format(last.content))

    server = SpeechEngineServer(port=0, on_transcript=on_transcript)

    async def _handler(ws: typing.Any, *_args: typing.Any) -> None:
        session = server.handle_connection(ws)
        await session.run()

    ws_server = await websockets.serve(_handler, "127.0.0.1", 0)  # type: ignore[attr-defined]
    actual_port = 0
    for sock in ws_server.sockets:
        actual_port = sock.getsockname()[1]
        break

    try:
        uri = "ws://127.0.0.1:{}".format(actual_port)
        async with websockets.connect(uri) as client:  # type: ignore[attr-defined]
            await client.send(
                json.dumps(
                    {
                        "type": "user_transcript",
                        "user_transcript": [{"role": "user", "content": "ping"}],
                        "event_id": 1,
                    }
                )
            )
            raw = await asyncio.wait_for(client.recv(), timeout=1.0)
            response = json.loads(raw)
    finally:
        ws_server.close()
        await ws_server.wait_closed()

    assert response == {
        "type": "agent_response",
        "content": "echo: ping",
        "event_id": 1,
        "is_final": False,
    }


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_stop_resolves_when_no_server_running() -> None:
    server = SpeechEngineServer()
    await server.stop()  # Should not raise.
