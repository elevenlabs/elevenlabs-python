"""Regression test for #854: RealtimeEvents.CLOSE must expose close code/reason."""

import asyncio

from elevenlabs.realtime.connection import RealtimeConnection, RealtimeEvents


class FakeWebSocket:
    """Immediately-closed stand-in for websockets' ClientConnection."""

    close_code = 1000
    close_reason = "normal closure"

    def __aiter__(self):
        async def _empty():
            return
            yield

        return _empty()


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def test_close_handler_receives_code_and_reason():
    conn = RealtimeConnection(FakeWebSocket(), 16000)
    received = []
    conn.on(RealtimeEvents.CLOSE, lambda info: received.append(info))
    run(conn._start_message_handler())
    assert received == [{"code": 1000, "reason": "normal closure"}]


def test_zero_arg_close_handler_still_works():
    conn = RealtimeConnection(FakeWebSocket(), 16000)
    calls = []
    conn.on(RealtimeEvents.CLOSE, lambda: calls.append("closed"))
    run(conn._start_message_handler())
    assert calls == ["closed"]


class FakeProtocol:
    close_code = 1011
    close_reason = "server error"


class FakeWebSocket13:
    """websockets 13.x asyncio Connection: close info lives only on .protocol."""

    def __init__(self):
        self.protocol = FakeProtocol()

    def __aiter__(self):
        return FakeWebSocket().__aiter__()


def test_close_handler_reads_protocol_close_info_on_websockets_13():
    conn = RealtimeConnection(FakeWebSocket13(), 16000)
    received = []
    conn.on(RealtimeEvents.CLOSE, lambda info: received.append(info))
    run(conn._start_message_handler())
    assert received == [{"code": 1011, "reason": "server error"}]
