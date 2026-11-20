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
    return asyncio.run(coro)


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


def test_async_handlers_are_awaited_for_close_and_other_events():
    conn = RealtimeConnection(FakeWebSocket(), 16000)
    calls = []

    async def on_close(info):
        calls.append(("close", info))

    async def on_open():
        calls.append("open")

    conn.on(RealtimeEvents.CLOSE, on_close)
    conn.on(RealtimeEvents.OPEN, on_open)

    async def main():
        conn._emit(RealtimeEvents.OPEN)
        await conn._start_message_handler()
        await asyncio.sleep(0)

    run(main())
    assert "open" in calls
    assert ("close", {"code": 1000, "reason": "normal closure"}) in calls


def test_suspended_async_handler_survives_gc():
    import gc
    import weakref

    conn = RealtimeConnection(FakeWebSocket(), 16000)
    done = []
    refs = []

    async def on_open():
        fut = asyncio.get_running_loop().create_future()
        refs.append(weakref.ref(fut))
        await fut
        done.append(True)

    conn.on(RealtimeEvents.OPEN, on_open)

    async def main():
        conn._emit(RealtimeEvents.OPEN)
        await asyncio.sleep(0)
        gc.collect()
        fut = refs[0]()
        assert fut is not None
        fut.set_result(None)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        assert not conn._handler_tasks

    run(main())
    assert done == [True]
