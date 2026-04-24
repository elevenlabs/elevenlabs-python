"""SpeechEngineServer — standalone WebSocket server for Speech Engine."""

import asyncio
import logging
import typing

from .session import SpeechEngineSession, _wire_handlers
from .types import WebSocketLike

logger = logging.getLogger("elevenlabs.speech_engine")


class SpeechEngineServer:
    """Standalone WebSocket server that produces :class:`SpeechEngineSession`
    instances for each incoming connection from the ElevenLabs Speech Engine
    API.

    Example::

        server = SpeechEngineServer(
            port=3001,
            debug=True,
            on_transcript=handle_transcript,
        )
        await server.serve()
    """

    def __init__(
        self,
        *,
        port: int = 3001,
        debug: bool = False,
        **handlers: typing.Any,
    ) -> None:
        self._port = port
        self._debug = debug
        self._handlers = handlers
        self._stop_event = asyncio.Event()
        self._server = None  # type: typing.Any

    def handle_connection(self, ws: WebSocketLike) -> SpeechEngineSession:
        """Wrap *ws* in a :class:`SpeechEngineSession` with the server's
        handlers wired up.

        Use this when you manage your own WebSocket server and want to wrap
        individual connections.  The returned session's :meth:`run` must
        still be awaited by the caller.
        """
        session = SpeechEngineSession(ws, debug=self._debug)
        _wire_handlers(session, self._handlers)
        return session

    async def serve(self) -> None:
        """Start the WebSocket server.  Blocks until :meth:`stop` is called."""
        import websockets  # noqa: E402 — keep import lazy

        async def _handler(websocket: typing.Any, *_args: typing.Any) -> None:
            session = self.handle_connection(websocket)
            await session.run()

        self._server = await websockets.serve(  # type: ignore[attr-defined]
            _handler,
            "",
            self._port,
        )
        logger.debug("speech engine server listening on port %d", self._port)
        try:
            await self._stop_event.wait()
        finally:
            self._server.close()
            await self._server.wait_closed()

    async def stop(self) -> None:
        """Signal the server to shut down gracefully."""
        self._stop_event.set()
