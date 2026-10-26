import asyncio
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import AsyncMock, MagicMock

import pytest
from websockets.exceptions import ConnectionClosedError
from websockets.frames import Close
from websockets.sync.server import serve

from elevenlabs.conversational_ai.conversation import AsyncConversation, Conversation, DisconnectionDetails


def test_missing_peer_close_frame_reports_abnormal_closure():
    error = ConnectionClosedError(None, Close(1000, "local shutdown"))
    details = DisconnectionDetails._from_exception(error)

    assert details.reason == "error"
    assert details.close_code == 1006
    assert details.close_reason == ""
    assert details.message == str(error)


@pytest.fixture
def websocket_server():
    servers = []

    def start(code=None, reason=""):
        connected = threading.Event()

        def handler(ws):
            ws.recv(timeout=5)
            connected.set()
            if code is None:
                ws.wait_closed()
            elif code == 1006:
                ws.socket.shutdown(socket.SHUT_RDWR)
                ws.socket.close()
            else:
                ws.close(code=code, reason=reason)

        server = serve(handler, "127.0.0.1", 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        servers.append((server, thread))
        return "http://127.0.0.1:{}".format(server.socket.getsockname()[1]), connected

    yield start

    for server, thread in servers:
        server.shutdown()
        thread.join(timeout=5)
        assert not thread.is_alive()


def make_client(url):
    client = MagicMock()
    client._client_wrapper.get_base_url.return_value = url
    return client


@pytest.mark.parametrize("code", [1000, 1001, 1006, 1008, 3000, 4001, 1011])
def test_sync_server_disconnect_details(websocket_server, code):
    url, _ = websocket_server(code, "session ended")
    disconnected = MagicMock()
    ended = MagicMock()
    conversation = Conversation(
        make_client(url),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    try:
        conversation.start_session()
        conversation._thread.join(timeout=5)
        assert not conversation._thread.is_alive()
    finally:
        conversation.end_session()

    ended.assert_called_once_with()
    disconnected.assert_called_once()
    details = disconnected.call_args.args[0]
    assert details.reason == ("agent" if code in (1000, 1001) else "error")
    assert details.close_code == code
    assert details.close_reason == ("" if code == 1006 else "session ended")
    assert bool(details.message) == (details.reason == "error")


@pytest.mark.parametrize("code", [1000, 1001, 1006, 1008, 3000, 4001, 1011])
@pytest.mark.asyncio
async def test_async_server_disconnect_details(websocket_server, code):
    url, _ = websocket_server(code, "session ended")
    disconnected = AsyncMock()
    ended = AsyncMock()
    conversation = AsyncConversation(
        make_client(url),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    try:
        await conversation.start_session()
        await asyncio.wait_for(conversation.wait_for_session_end(), timeout=5)
    finally:
        await conversation.end_session()

    ended.assert_awaited_once_with()
    disconnected.assert_awaited_once()
    details = disconnected.call_args.args[0]
    assert details.reason == ("agent" if code in (1000, 1001) else "error")
    assert details.close_code == code
    assert details.close_reason == ("" if code == 1006 else "session ended")
    assert bool(details.message) == (details.reason == "error")


def test_sync_user_disconnect_is_reported_once(websocket_server):
    url, connected = websocket_server()
    disconnected = MagicMock()
    ended = MagicMock()
    conversation = Conversation(
        make_client(url),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    try:
        conversation.start_session()
        assert connected.wait(timeout=5)
    finally:
        conversation.end_session()
        conversation.end_session()
        conversation._thread.join(timeout=5)
    assert not conversation._thread.is_alive()
    ended.assert_called_once_with()
    disconnected.assert_called_once()
    details = disconnected.call_args.args[0]
    assert details.reason == "user"
    assert details.close_code is None
    assert details.close_reason is None
    assert details.message is None


def test_sync_connection_failure_reports_error():
    with socket.socket() as unavailable:
        unavailable.bind(("127.0.0.1", 0))
        url = "http://127.0.0.1:{}".format(unavailable.getsockname()[1])
        disconnected = MagicMock()
        conversation = Conversation(
            make_client(url),
            "agent",
            requires_auth=False,
            client_tools=MagicMock(),
            callback_disconnect=disconnected,
        )
        try:
            conversation.start_session()
            conversation._thread.join(timeout=5)
            assert not conversation._thread.is_alive()
        finally:
            conversation.end_session()

    disconnected.assert_called_once()
    details = disconnected.call_args.args[0]
    assert details.reason == "error"
    assert details.close_code is None
    assert details.close_reason is None
    assert details.message


@pytest.mark.asyncio
async def test_async_connection_failure_reports_error():
    with socket.socket() as unavailable:
        unavailable.bind(("127.0.0.1", 0))
        url = "http://127.0.0.1:{}".format(unavailable.getsockname()[1])
        disconnected = AsyncMock()
        conversation = AsyncConversation(
            make_client(url),
            "agent",
            requires_auth=False,
            client_tools=MagicMock(),
            callback_disconnect=disconnected,
        )
        try:
            await conversation.start_session()
            await asyncio.wait_for(conversation.wait_for_session_end(), timeout=5)
        finally:
            await conversation.end_session()

    disconnected.assert_awaited_once()
    details = disconnected.call_args.args[0]
    assert details.reason == "error"
    assert details.close_code is None
    assert details.close_reason is None
    assert details.message


def test_sync_callback_type_error_is_not_retried():
    ended = MagicMock(side_effect=TypeError("callback failed"))
    disconnected = MagicMock()
    conversation = Conversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )

    with pytest.raises(TypeError, match="callback failed"):
        conversation.end_session()
    conversation.end_session()

    ended.assert_called_once_with()
    disconnected.assert_called_once()
    assert disconnected.call_args.args[0].reason == "user"


@pytest.mark.asyncio
async def test_async_callback_type_error_is_not_retried():
    ended = AsyncMock(side_effect=TypeError("callback failed"))
    disconnected = AsyncMock()
    conversation = AsyncConversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )

    with pytest.raises(TypeError, match="callback failed"):
        await conversation.end_session()
    await conversation.end_session()

    ended.assert_awaited_once_with()
    disconnected.assert_awaited_once()
    assert disconnected.call_args.args[0].reason == "user"


def test_sync_callbacks_can_end_session_again():
    ended = MagicMock(side_effect=lambda: conversation.end_session())
    disconnected = MagicMock(side_effect=lambda details: conversation.end_session())
    conversation = Conversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    conversation.end_session()

    ended.assert_called_once_with()
    disconnected.assert_called_once()


@pytest.mark.asyncio
async def test_async_callbacks_can_end_session_again():
    async def on_end():
        await conversation.end_session()

    async def on_disconnect(details):
        await conversation.end_session()

    ended = AsyncMock(side_effect=on_end)
    disconnected = AsyncMock(side_effect=on_disconnect)
    conversation = AsyncConversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    await conversation.end_session()

    ended.assert_awaited_once_with()
    disconnected.assert_awaited_once()


def test_sync_concurrent_shutdown_notifies_once():
    ended = MagicMock()
    disconnected = MagicMock()
    tools = MagicMock()
    conversation = Conversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=tools,
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    barrier = threading.Barrier(4, timeout=5)

    def stop():
        barrier.wait()
        conversation.end_session()

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(stop) for _ in range(4)]
        for future in futures:
            future.result(timeout=5)

    tools.stop.assert_called_once_with()
    ended.assert_called_once_with()
    disconnected.assert_called_once()


@pytest.mark.asyncio
async def test_async_concurrent_shutdown_notifies_once():
    async def stop_audio():
        await asyncio.sleep(0)

    audio = AsyncMock()
    audio.stop.side_effect = stop_audio
    ended = AsyncMock()
    disconnected = AsyncMock()
    conversation = AsyncConversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        audio_interface=audio,
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    await asyncio.gather(*(conversation.end_session() for _ in range(4)))

    audio.stop.assert_awaited_once_with()
    ended.assert_awaited_once_with()
    disconnected.assert_awaited_once()


def test_sync_cleanup_failure_still_notifies():
    tools = MagicMock()
    tools.stop.side_effect = RuntimeError("cleanup failed")
    ended = MagicMock()
    disconnected = MagicMock()
    conversation = Conversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=tools,
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    with pytest.raises(RuntimeError, match="cleanup failed"):
        conversation.end_session()
    conversation.end_session()

    assert conversation._ws is None
    ended.assert_called_once_with()
    disconnected.assert_called_once()


@pytest.mark.asyncio
async def test_async_cleanup_failure_still_notifies():
    tools = MagicMock()
    tools.stop.side_effect = RuntimeError("cleanup failed")
    ended = AsyncMock()
    disconnected = AsyncMock()
    conversation = AsyncConversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=tools,
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    with pytest.raises(RuntimeError, match="cleanup failed"):
        await conversation.end_session()
    await conversation.end_session()

    assert conversation._ws is None
    ended.assert_awaited_once_with()
    disconnected.assert_awaited_once()


@pytest.mark.asyncio
async def test_async_user_disconnect_is_reported_once(websocket_server):
    url, connected = websocket_server()
    disconnected = AsyncMock()
    ended = AsyncMock()
    conversation = AsyncConversation(
        make_client(url),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    try:
        await conversation.start_session()
        assert await asyncio.get_running_loop().run_in_executor(None, connected.wait, 5)
    finally:
        await conversation.end_session()
        await conversation.end_session()
        await asyncio.wait_for(conversation.wait_for_session_end(), timeout=5)
    ended.assert_awaited_once_with()
    disconnected.assert_awaited_once()
    details = disconnected.call_args.args[0]
    assert details.reason == "user"
    assert details.close_code is None
    assert details.close_reason is None
    assert details.message is None
