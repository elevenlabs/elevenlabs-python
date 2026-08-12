# Hand-maintained (.fernignore): merges the hand-written session/server layer
# exports with the generated socket message types. When the generated
# speech_engine exports change, mirror them here.

# isort: skip_file

"""ElevenLabs Speech Engine SDK module."""

from .resource import SpeechEngineResource, verify_speech_engine_jwt
from .server import SpeechEngineServer
from .session import SpeechEngineSession
from .session_types import (
    CLOSE,
    DISCONNECTED,
    ERROR,
    INIT,
    USER_TRANSCRIPT,
    ConversationMessage,
    WebSocketLike,
)
from .types import ReceiveUpstreamMessage, SendUpstreamMessage

__all__ = [
    "ConversationMessage",
    "ReceiveUpstreamMessage",
    "SendUpstreamMessage",
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
