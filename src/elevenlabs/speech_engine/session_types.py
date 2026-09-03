"""Types for the Speech Engine module."""

import typing

import pydantic

# ---------------------------------------------------------------------------
# Event name constants
# ---------------------------------------------------------------------------

INIT = "init"
USER_TRANSCRIPT = "user_transcript"
CLOSE = "close"
ERROR = "error"
DISCONNECTED = "disconnected"

# ---------------------------------------------------------------------------
# Wire protocol — incoming (ElevenLabs API -> developer server)
# ---------------------------------------------------------------------------
#
# InitMessage:           {"type": "init", "conversation_id": "..."}
# UserTranscriptMessage: {"type": "user_transcript", "user_transcript": [...], "event_id": N}
# PingMessage:           {"type": "ping"}
# CloseMessage:          {"type": "close"}
# ErrorMessage:          {"type": "error", "message": "..."}
#
# ---------------------------------------------------------------------------
# Wire protocol — outgoing (developer server -> ElevenLabs API)
# ---------------------------------------------------------------------------
#
# AgentResponseMessage:  {"type": "agent_response", "content": "...", "event_id": N, "is_final": bool}
# PongMessage:           {"type": "pong"}
#

# ---------------------------------------------------------------------------
# ConversationMessage
# ---------------------------------------------------------------------------


class ConversationMessage(pydantic.BaseModel):
    """A single message in a speech engine conversation.

    Attributes:
        role: Either ``"user"`` or ``"agent"``.
        content: The text content of the message.
    """

    role: str
    content: str


# ---------------------------------------------------------------------------
# WebSocket abstraction
# ---------------------------------------------------------------------------


class WebSocketLike(typing.Protocol):
    """Protocol for WebSocket-like objects.

    Compatible with ``websockets.WebSocketServerProtocol`` and
    FastAPI/Starlette ``WebSocket`` out of the box (auto-detected).
    """

    async def recv(self) -> typing.Union[str, bytes]:
        ...  # pragma: no cover

    async def send(self, data: str) -> None:
        ...  # pragma: no cover

    async def close(self) -> None:
        ...  # pragma: no cover


class _ASGIWebSocketAdapter:
    """Adapts a FastAPI/Starlette WebSocket to the :class:`WebSocketLike`
    interface expected by :class:`~.session.SpeechEngineSession`."""

    def __init__(self, ws: typing.Any) -> None:
        self._ws = ws

    async def recv(self) -> typing.Union[str, bytes]:
        return await self._ws.receive_text()

    async def send(self, data: str) -> None:
        await self._ws.send_text(data)

    async def close(self) -> None:
        await self._ws.close()


def wrap_websocket(ws: typing.Any) -> WebSocketLike:
    """Return a :class:`WebSocketLike` wrapper for *ws*.

    If *ws* already has ``recv``/``send`` (e.g. the ``websockets`` library),
    it is returned as-is.  If it has ``receive_text``/``send_text`` (e.g.
    FastAPI/Starlette), it is wrapped with :class:`_ASGIWebSocketAdapter`.
    """
    if hasattr(ws, "recv"):
        return ws
    if hasattr(ws, "receive_text"):
        return _ASGIWebSocketAdapter(ws)
    raise TypeError(
        f"Cannot wrap {type(ws).__name__}: expected a websockets-style "
        f"object (recv/send) or an ASGI-style object (receive_text/send_text)"
    )
