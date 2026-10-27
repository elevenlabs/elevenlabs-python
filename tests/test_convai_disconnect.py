import asyncio
import socket
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from websockets.exceptions import ConnectionClosedError
from websockets.frames import Close
from websockets.sync.server import serve

from elevenlabs.conversational_ai.conversation import AsyncConversation, Conversation, DisconnectionDetails
from elevenlabs.conversational_ai.default_audio_interface import AsyncDefaultAudioInterface, DefaultAudioInterface

pytestmark = pytest.mark.filterwarnings("ignore:callback_end_session is deprecated:DeprecationWarning")


@pytest.fixture
def default_audio_interfaces(monkeypatch):
    monkeypatch.setitem(sys.modules, "pyaudio", MagicMock())
    sync_audio = DefaultAudioInterface()
    sync_audio.start = MagicMock(wraps=sync_audio.start)
    sync_audio.stop = MagicMock(wraps=sync_audio.stop)
    async_audio = AsyncDefaultAudioInterface()
    async_audio.start = AsyncMock(wraps=async_audio.start)
    async_audio.stop = AsyncMock(wraps=async_audio.stop)
    return sync_audio, async_audio


@pytest.mark.parametrize("stage", ["connect", "init-message", "audio-start"])
def test_sync_setup_failure_does_not_stop_unstarted_audio(default_audio_interfaces, stage):
    audio, _ = default_audio_interfaces
    ended = MagicMock()
    disconnected = MagicMock()
    conversation = Conversation(
        make_client("http://localhost"),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        audio_interface=audio,
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    error = OSError("original setup error")
    with patch("elevenlabs.conversational_ai.conversation.connect") as connect:
        if stage == "connect":
            connect.side_effect = error
        elif stage == "init-message":
            connect.return_value.__enter__.return_value.send.side_effect = error
        else:
            audio.start.side_effect = error
        conversation._run("ws://localhost")
    conversation.end_session()

    if stage == "audio-start":
        audio.start.assert_called_once()
    else:
        audio.start.assert_not_called()
    audio.stop.assert_not_called()
    ended.assert_called_once_with()
    disconnected.assert_called_once()
    assert disconnected.call_args.args[0] == DisconnectionDetails(reason="error", message=str(error))
    assert conversation._ws is None


@pytest.mark.parametrize("stage", ["connect", "init-message", "audio-start"])
@pytest.mark.asyncio
async def test_async_setup_failure_does_not_stop_unstarted_audio(default_audio_interfaces, stage):
    _, audio = default_audio_interfaces
    ended = AsyncMock()
    disconnected = AsyncMock()
    conversation = AsyncConversation(
        make_client("http://localhost"),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        audio_interface=audio,
        callback_end_session=ended,
        callback_disconnect=disconnected,
    )
    error = OSError("original setup error")
    with patch("elevenlabs.conversational_ai.conversation.websockets.connect") as connect:
        if stage == "connect":
            connect.side_effect = error
        elif stage == "init-message":
            connect.return_value.__aenter__.return_value.send.side_effect = error
        else:
            audio.start.side_effect = error
        await conversation.start_session()
        await asyncio.wait_for(conversation.wait_for_session_end(), timeout=5)
    await conversation.end_session()

    if stage == "audio-start":
        audio.start.assert_awaited_once()
    else:
        audio.start.assert_not_awaited()
    audio.stop.assert_not_awaited()
    ended.assert_awaited_once_with()
    disconnected.assert_awaited_once()
    assert disconnected.call_args.args[0] == DisconnectionDetails(reason="error", message=str(error))
    assert conversation._ws is None


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


@pytest.mark.filterwarnings("default")
@pytest.mark.parametrize("conversation_class", [Conversation, AsyncConversation])
def test_callback_end_session_is_deprecated(conversation_class):
    with pytest.warns(DeprecationWarning, match="use callback_disconnect instead"):
        conversation_class(make_client("http://localhost"), "agent", requires_auth=False, callback_end_session=MagicMock())


def test_sync_close_stops_started_default_audio_once(websocket_server, default_audio_interfaces):
    url, _ = websocket_server(1000)
    audio, _ = default_audio_interfaces
    disconnected = MagicMock()
    conversation = Conversation(
        make_client(url),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        audio_interface=audio,
        callback_disconnect=disconnected,
    )
    try:
        conversation.start_session()
        conversation._thread.join(timeout=5)
        assert not conversation._thread.is_alive()
    finally:
        conversation.end_session()

    audio.start.assert_called_once()
    audio.stop.assert_called_once_with()
    assert not audio.output_thread.is_alive()
    disconnected.assert_called_once()
    assert disconnected.call_args.args[0].reason == "agent"


@pytest.mark.asyncio
async def test_async_close_stops_started_default_audio_once(websocket_server, default_audio_interfaces):
    url, _ = websocket_server(1000)
    _, audio = default_audio_interfaces
    disconnected = AsyncMock()
    conversation = AsyncConversation(
        make_client(url),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        audio_interface=audio,
        callback_disconnect=disconnected,
    )
    try:
        await conversation.start_session()
        await asyncio.wait_for(conversation.wait_for_session_end(), timeout=5)
    finally:
        await conversation.end_session()

    audio.start.assert_awaited_once()
    audio.stop.assert_awaited_once_with()
    assert audio.output_task.done()
    disconnected.assert_awaited_once()
    assert disconnected.call_args.args[0].reason == "agent"


def test_sync_shutdown_before_start_does_not_stop_audio(default_audio_interfaces):
    audio, _ = default_audio_interfaces
    disconnected = MagicMock()
    conversation = Conversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        audio_interface=audio,
        callback_disconnect=disconnected,
    )
    conversation.end_session()
    conversation.end_session()

    audio.start.assert_not_called()
    audio.stop.assert_not_called()
    disconnected.assert_called_once()
    assert disconnected.call_args.args[0].reason == "user"


@pytest.mark.asyncio
async def test_async_shutdown_before_start_does_not_stop_audio(default_audio_interfaces):
    _, audio = default_audio_interfaces
    disconnected = AsyncMock()
    conversation = AsyncConversation(
        MagicMock(),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        audio_interface=audio,
        callback_disconnect=disconnected,
    )
    await conversation.end_session()
    await conversation.end_session()

    audio.start.assert_not_awaited()
    audio.stop.assert_not_awaited()
    disconnected.assert_awaited_once()
    assert disconnected.call_args.args[0].reason == "user"


def test_sync_shutdown_during_audio_start_cleans_up(websocket_server, default_audio_interfaces):
    url, _ = websocket_server()
    audio, _ = default_audio_interfaces
    starting = threading.Event()
    release = threading.Event()
    start_audio = audio.start

    def delayed_start(callback):
        starting.set()
        assert release.wait(timeout=5)
        start_audio(callback)

    audio.start = MagicMock(side_effect=delayed_start)
    disconnected = MagicMock()
    conversation = Conversation(
        make_client(url),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        audio_interface=audio,
        callback_disconnect=disconnected,
    )
    try:
        conversation.start_session()
        assert starting.wait(timeout=5)
        conversation.end_session()
        audio.stop.assert_not_called()
        release.set()
        conversation._thread.join(timeout=5)

        assert not conversation._thread.is_alive()
        audio.stop.assert_called_once_with()
        assert not audio.output_thread.is_alive()
        disconnected.assert_called_once()
        assert disconnected.call_args.args[0].reason == "user"
    finally:
        release.set()
        conversation.end_session()
        conversation._thread.join(timeout=5)
        if hasattr(audio, "should_stop") and not audio.should_stop.is_set():
            audio.stop()


@pytest.mark.asyncio
async def test_async_shutdown_during_audio_start_cleans_up(websocket_server, default_audio_interfaces):
    url, _ = websocket_server()
    _, audio = default_audio_interfaces
    starting = asyncio.Event()
    release = asyncio.Event()
    start_audio = audio.start

    async def delayed_start(callback):
        starting.set()
        await asyncio.wait_for(release.wait(), timeout=5)
        await start_audio(callback)

    audio.start = AsyncMock(side_effect=delayed_start)
    disconnected = AsyncMock()
    conversation = AsyncConversation(
        make_client(url),
        "agent",
        requires_auth=False,
        client_tools=MagicMock(),
        audio_interface=audio,
        callback_disconnect=disconnected,
    )
    try:
        await conversation.start_session()
        await asyncio.wait_for(starting.wait(), timeout=5)
        await conversation.end_session()
        audio.stop.assert_not_awaited()
        release.set()
        await asyncio.wait_for(conversation.wait_for_session_end(), timeout=5)

        audio.stop.assert_awaited_once_with()
        assert audio.output_task.done()
        disconnected.assert_awaited_once()
        assert disconnected.call_args.args[0].reason == "user"
    finally:
        release.set()
        await conversation.end_session()
        await asyncio.wait_for(conversation.wait_for_session_end(), timeout=5)
        if hasattr(audio, "should_stop") and not audio.should_stop.is_set():
            await audio.stop()


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
    async def on_end():
        await asyncio.sleep(0)

    audio = AsyncMock()
    ended = AsyncMock(side_effect=on_end)
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

    audio.stop.assert_not_awaited()
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
