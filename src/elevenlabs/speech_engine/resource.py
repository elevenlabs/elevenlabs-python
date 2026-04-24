"""SpeechEngineResource — client-facing handle for a speech engine instance."""

import typing

from .server import SpeechEngineServer
from .session import SpeechEngineSession
from .types import WebSocketLike


class SpeechEngineResource:
    """Represents a speech engine instance.

    Returned by ``await client.speech_engine.get("seng_123")``.

    Use :meth:`serve` to start a standalone WebSocket server, or
    :meth:`create_session` to wrap an existing WebSocket for custom
    server integration (FastAPI, Starlette, etc.).

    Example::

        engine = await elevenlabs.speech_engine.get("seng_123")

        async def on_transcript(transcript, session):
            stream = await openai.responses.create(...)
            await session.send_response(stream)

        await engine.serve(
            port=3001,
            debug=True,
            on_transcript=on_transcript,
        )
    """

    def __init__(
        self,
        engine_id: str,
        client_options: typing.Any = None,
    ) -> None:
        self.engine_id = engine_id
        self._options = client_options

    async def serve(
        self,
        *,
        port: int = 3001,
        debug: bool = False,
        **handlers: typing.Any,
    ) -> None:
        """Start a standalone WebSocket server.  Blocks until stopped."""
        server = SpeechEngineServer(port=port, debug=debug, **handlers)
        await server.serve()

    def create_session(
        self,
        ws: WebSocketLike,
        *,
        debug: bool = False,
    ) -> SpeechEngineSession:
        """Wrap *ws* in a :class:`SpeechEngineSession`.

        Use this for custom server integration (e.g. FastAPI, Starlette).
        Wire handlers via :meth:`~SpeechEngineSession.on` then ``await
        session.run()``.
        """
        return SpeechEngineSession(ws, debug=debug)
