"""SpeechEngineResource — client-facing handle for a speech engine instance."""

import base64
import hashlib
import hmac
import json
import logging
import time
import typing

from .server import SpeechEngineServer
from .session import SpeechEngineSession
from .types import WebSocketLike

logger = logging.getLogger("elevenlabs.speech_engine")

_ISSUER = "https://api.elevenlabs.io/convai/speech-engine"
_SUBJECT = "convai_speech_engine_upstream"
_LEEWAY_SECONDS = 60


def _base64url_decode(data: str) -> bytes:
    padded = data.replace("-", "+").replace("_", "/")
    remainder = len(padded) % 4
    if remainder:
        padded += "=" * (4 - remainder)
    return base64.b64decode(padded)


def verify_speech_engine_jwt(value: str, api_key: str) -> typing.Dict[str, typing.Any]:
    """Verify an HS256 JWT from the ElevenLabs Speech Engine API.

    The HMAC secret is the SHA-256 hash of the API key.  Returns the
    decoded payload on success, raises :class:`ValueError` on failure.
    """
    token = value.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT: expected 3 parts")

    header_b64, payload_b64, signature_b64 = parts

    try:
        payload = json.loads(_base64url_decode(payload_b64))
    except Exception:
        raise ValueError("Invalid JWT: failed to decode payload")

    trimmed_key = api_key.strip()
    secret = hashlib.sha256(trimmed_key.encode("utf-8")).digest()

    expected_sig = hmac.new(
        secret, f"{header_b64}.{payload_b64}".encode(), hashlib.sha256
    ).digest()
    actual_sig = _base64url_decode(signature_b64)

    if not hmac.compare_digest(expected_sig, actual_sig):
        raise ValueError(
            "Invalid JWT: signature mismatch — make sure the API key used "
            "by your Speech Engine server matches the one used to create "
            "the engine."
        )

    if payload.get("iss") != _ISSUER:
        raise ValueError(
            f'Invalid JWT: expected issuer "{_ISSUER}", got "{payload.get("iss")}"'
        )
    if payload.get("sub") != _SUBJECT:
        raise ValueError(
            f'Invalid JWT: expected subject "{_SUBJECT}", got "{payload.get("sub")}"'
        )

    now = int(time.time())

    exp = payload.get("exp")
    if not isinstance(exp, (int, float)):
        raise ValueError("Invalid JWT: missing exp claim")
    iat = payload.get("iat")
    if not isinstance(iat, (int, float)):
        raise ValueError("Invalid JWT: missing iat claim")
    if exp + _LEEWAY_SECONDS < now:
        raise ValueError("Invalid JWT: token has expired")
    if iat - _LEEWAY_SECONDS > now:
        raise ValueError("Invalid JWT: iat is in the future")

    return payload


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
        client_wrapper: typing.Any = None,
    ) -> None:
        self.engine_id = engine_id
        self._client_wrapper = client_wrapper

    def _get_api_key(self) -> typing.Optional[str]:
        if self._client_wrapper is None:
            return None
        headers = self._client_wrapper.get_headers()
        return headers.get("xi-api-key")

    def verify_request(
        self, headers: typing.Dict[str, typing.Any]
    ) -> bool:
        """Verify that an incoming request is from the ElevenLabs API.

        Checks the ``X-Elevenlabs-Speech-Engine-Authorization`` header
        for a valid JWT signed with the SHA-256 hash of the API key.

        Only needed when managing the WebSocket upgrade yourself.
        When using :meth:`serve`, verification is handled automatically.
        """
        api_key = self._get_api_key()
        if not api_key:
            return False
        raw = headers.get("x-elevenlabs-speech-engine-authorization")
        if isinstance(raw, list):
            raw = raw[0] if raw else None
        if not raw:
            return False
        try:
            verify_speech_engine_jwt(raw, api_key)
            return True
        except ValueError:
            return False

    async def serve(
        self,
        *,
        port: int = 3001,
        path: typing.Optional[str] = None,
        debug: bool = False,
        **handlers: typing.Any,
    ) -> None:
        """Start a standalone WebSocket server.  Blocks until stopped."""
        api_key = self._get_api_key()
        server = SpeechEngineServer(
            port=port, path=path, debug=debug, api_key=api_key, **handlers
        )
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
