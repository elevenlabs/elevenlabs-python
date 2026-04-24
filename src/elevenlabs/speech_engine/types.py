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

    Compatible with ``websockets.WebSocketServerProtocol`` out of the box.
    For FastAPI/Starlette ``WebSocket``, provide a thin adapter that maps
    ``receive_text`` -> ``recv`` and ``send_text`` -> ``send``.
    """

    async def recv(self) -> typing.Union[str, bytes]:
        ...  # pragma: no cover

    async def send(self, data: str) -> None:
        ...  # pragma: no cover

    async def close(self) -> None:
        ...  # pragma: no cover
