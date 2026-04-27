"""ElevenLabs Speech Engine SDK module."""

from .resource import SpeechEngineResource, verify_speech_engine_jwt
from .server import SpeechEngineServer
from .session import SpeechEngineSession
from .types import (
    CLOSE,
    DISCONNECTED,
    ERROR,
    INIT,
    USER_TRANSCRIPT,
    ConversationMessage,
    WebSocketLike,
)

__all__ = [
    "ConversationMessage",
    "SpeechEngineResource",
    "SpeechEngineServer",
    "SpeechEngineSession",
    "WebSocketLike",
    "verify_speech_engine_jwt",
    "CLOSE",
    "DISCONNECTED",
    "ERROR",
    "INIT",
    "USER_TRANSCRIPT",
]
