"""SpeechEngineServer — standalone WebSocket server for Speech Engine."""

import asyncio
import os
import typing

from .session import SpeechEngineSession, _make_log, _wire_handlers
from .types import WebSocketLike


class SpeechEngineServer:
    """Standalone WebSocket server that produces :class:`SpeechEngineSession`
    instances for each incoming connection from the ElevenLabs Speech Engine
    API.

    Every incoming connection is verified against the ElevenLabs API using
    the configured API key before being accepted.

    Example::

        server = SpeechEngineServer(
            port=3001,
            api_key="sk_...",
            debug=True,
            on_transcript=handle_transcript,
        )
        await server.serve()
    """

    def __init__(
        self,
        *,
        port: int = 3001,
        path: typing.Optional[str] = None,
        api_key: typing.Optional[str] = None,
        debug: bool = False,
        **handlers: typing.Any,
    ) -> None:
        self._port = port
        self._path = path
        self._api_key = api_key
        self._debug = debug
        self._handlers = handlers
        self._stop_event = None  # type: typing.Optional[asyncio.Event]
        self._server = None  # type: typing.Any
        self._log = _make_log(debug)

    def handle_connection(self, ws: WebSocketLike) -> SpeechEngineSession:
        """Wrap *ws* in a :class:`SpeechEngineSession` with the server's
        handlers wired up.

        Use this when you manage your own WebSocket server and want to wrap
        individual connections.  The returned session's :meth:`run` must
        still be awaited by the caller.
        """
        self._log("creating new session")
        session = SpeechEngineSession(ws, debug=self._debug)
        _wire_handlers(session, self._handlers)
        return session

    async def serve(self) -> None:
        """Start the WebSocket server.  Blocks until :meth:`stop` is called."""
        from .resource import verify_speech_engine_jwt  # noqa: E402

        import websockets  # noqa: E402 — keep import lazy

        api_key = self._api_key or os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            raise RuntimeError(
                "SpeechEngineServer requires an API key to verify incoming "
                "connections. Pass api_key= or set the ELEVENLABS_API_KEY "
                "environment variable."
            )

        self._stop_event = asyncio.Event()

        async def _handler(websocket: typing.Any, *_args: typing.Any) -> None:
            if self._path is not None and websocket.request.path != self._path:
                await websocket.close(4000, "not found")
                return

            header_value = websocket.request.headers.get(
                "x-elevenlabs-speech-engine-authorization"
            )
            if not header_value:
                self._log(
                    "rejected connection — missing "
                    "X-Elevenlabs-Speech-Engine-Authorization header"
                )
                await websocket.close(
                    4001, "missing authorization header"
                )
                return

            try:
                verify_speech_engine_jwt(header_value, api_key)
            except ValueError as e:
                self._log("rejected connection — %s", e)
                await websocket.close(4001, str(e))
                return

            self._log("verified connection, accepting WebSocket")
            session = self.handle_connection(websocket)
            await session.run()

        self._server = await websockets.serve(  # type: ignore[attr-defined]
            _handler,
            "",
            self._port,
        )
        self._log("speech engine server listening on port %d", self._port)
        try:
            await self._stop_event.wait()
        finally:
            self._server.close()
            await self._server.wait_closed()

    async def stop(self) -> None:
        """Signal the server to shut down gracefully."""
        if self._stop_event is not None:
            self._stop_event.set()
