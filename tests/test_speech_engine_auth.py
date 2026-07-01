"""Tests for Speech Engine JWT verification."""

import asyncio
import base64
import hashlib
import hmac
import json
import time
import typing
import warnings

import pytest
import websockets

from elevenlabs.speech_engine import SpeechEngineServer
from elevenlabs.speech_engine.resource import (
    SpeechEngineResource,
    verify_speech_engine_jwt,
)

TEST_API_KEY = "test-key"
JWT_ISSUER = "https://api.elevenlabs.io/convai/speech-engine"
JWT_SUBJECT = "convai_speech_engine_upstream"


# ---------------------------------------------------------------------------
# JWT test helpers
# ---------------------------------------------------------------------------


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _create_test_jwt(
    payload: typing.Dict[str, typing.Any],
    api_key: str = TEST_API_KEY,
) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _base64url_encode(json.dumps(header).encode())
    payload_b64 = _base64url_encode(json.dumps(payload).encode())
    secret = hashlib.sha256(api_key.encode("utf-8")).digest()
    signature = hmac.new(
        secret, f"{header_b64}.{payload_b64}".encode(), hashlib.sha256
    ).digest()
    return f"{header_b64}.{payload_b64}.{_base64url_encode(signature)}"


def _valid_payload(**overrides: typing.Any) -> typing.Dict[str, typing.Any]:
    now = int(time.time())
    return {
        "iss": JWT_ISSUER,
        "sub": JWT_SUBJECT,
        "iat": now,
        "exp": now + 300,
        **overrides,
    }


# ---------------------------------------------------------------------------
# verify_speech_engine_jwt
# ---------------------------------------------------------------------------


class TestVerifySpeechEngineJwt:
    def test_valid_token(self) -> None:
        token = _create_test_jwt(_valid_payload())
        payload = verify_speech_engine_jwt(token, TEST_API_KEY)
        assert payload["iss"] == JWT_ISSUER
        assert payload["sub"] == JWT_SUBJECT

    def test_accepts_bearer_prefix(self) -> None:
        token = _create_test_jwt(_valid_payload())
        payload = verify_speech_engine_jwt(f"Bearer {token}", TEST_API_KEY)
        assert payload["iss"] == JWT_ISSUER

    def test_rejects_wrong_key(self) -> None:
        token = _create_test_jwt(_valid_payload(), api_key="other-key")
        with pytest.raises(ValueError, match="signature mismatch"):
            verify_speech_engine_jwt(token, TEST_API_KEY)

    def test_rejects_wrong_issuer(self) -> None:
        token = _create_test_jwt(_valid_payload(iss="https://evil.com"))
        with pytest.raises(ValueError, match="expected issuer"):
            verify_speech_engine_jwt(token, TEST_API_KEY)

    def test_rejects_wrong_subject(self) -> None:
        token = _create_test_jwt(_valid_payload(sub="wrong_subject"))
        with pytest.raises(ValueError, match="expected subject"):
            verify_speech_engine_jwt(token, TEST_API_KEY)

    def test_rejects_expired_token_beyond_leeway(self) -> None:
        now = int(time.time())
        token = _create_test_jwt(
            _valid_payload(exp=now - 120, iat=now - 420)
        )
        with pytest.raises(ValueError, match="expired"):
            verify_speech_engine_jwt(token, TEST_API_KEY)

    def test_accepts_expired_within_leeway(self) -> None:
        now = int(time.time())
        token = _create_test_jwt(
            _valid_payload(exp=now - 30, iat=now - 330)
        )
        payload = verify_speech_engine_jwt(token, TEST_API_KEY)
        assert payload["iss"] == JWT_ISSUER

    def test_rejects_future_iat_beyond_leeway(self) -> None:
        now = int(time.time())
        token = _create_test_jwt(
            _valid_payload(iat=now + 120, exp=now + 420)
        )
        with pytest.raises(ValueError, match="iat is in the future"):
            verify_speech_engine_jwt(token, TEST_API_KEY)

    def test_accepts_future_iat_within_leeway(self) -> None:
        now = int(time.time())
        token = _create_test_jwt(
            _valid_payload(iat=now + 30, exp=now + 330)
        )
        payload = verify_speech_engine_jwt(token, TEST_API_KEY)
        assert payload["iss"] == JWT_ISSUER

    def test_rejects_malformed_token(self) -> None:
        with pytest.raises(ValueError, match="expected 3 parts"):
            verify_speech_engine_jwt("not.a.valid.jwt.token", TEST_API_KEY)

    def test_rejects_missing_exp(self) -> None:
        payload = _valid_payload()
        del payload["exp"]
        token = _create_test_jwt(payload)
        with pytest.raises(ValueError, match="missing exp"):
            verify_speech_engine_jwt(token, TEST_API_KEY)

    def test_rejects_missing_iat(self) -> None:
        payload = _valid_payload()
        del payload["iat"]
        token = _create_test_jwt(payload)
        with pytest.raises(ValueError, match="missing iat"):
            verify_speech_engine_jwt(token, TEST_API_KEY)


# ---------------------------------------------------------------------------
# SpeechEngineResource.verify_request
# ---------------------------------------------------------------------------


class _FakeClientWrapper:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def get_headers(self) -> dict:
        return {"xi-api-key": self._api_key}


class TestVerifyRequest:
    def test_valid_header(self) -> None:
        resource = SpeechEngineResource(
            "seng_test", client_wrapper=_FakeClientWrapper(TEST_API_KEY)
        )
        token = _create_test_jwt(_valid_payload())
        assert resource.verify_request(
            {"x-elevenlabs-speech-engine-authorization": token}
        )

    def test_missing_header(self) -> None:
        resource = SpeechEngineResource(
            "seng_test", client_wrapper=_FakeClientWrapper(TEST_API_KEY)
        )
        assert not resource.verify_request({})

    def test_no_api_key(self) -> None:
        resource = SpeechEngineResource("seng_test")
        token = _create_test_jwt(_valid_payload())
        assert not resource.verify_request(
            {"x-elevenlabs-speech-engine-authorization": token}
        )

    def test_invalid_token(self) -> None:
        resource = SpeechEngineResource(
            "seng_test", client_wrapper=_FakeClientWrapper(TEST_API_KEY)
        )
        assert not resource.verify_request(
            {"x-elevenlabs-speech-engine-authorization": "bad-token"}
        )


# ---------------------------------------------------------------------------
# SpeechEngineServer — api_key requirement
# ---------------------------------------------------------------------------


class TestServerApiKeyRequirement:
    @pytest.mark.asyncio
    async def test_raises_without_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
        from elevenlabs.speech_engine import SpeechEngineServer

        server = SpeechEngineServer(port=0)
        with pytest.raises(RuntimeError, match="API key"):
            await server.serve()


# ---------------------------------------------------------------------------
# SpeechEngineServer — disable_auth
# ---------------------------------------------------------------------------


async def _run_server_briefly(server: SpeechEngineServer) -> asyncio.Task:
    """Start ``server`` in a background task and wait until it's listening."""
    task = asyncio.create_task(server.serve())
    # Give the server loop a moment to reach `await self._stop_event.wait()`.
    for _ in range(50):
        await asyncio.sleep(0.02)
        if server._server is not None:
            break
    return task


def _server_port(server: SpeechEngineServer) -> int:
    import socket as _socket

    # websockets.serve(host="") binds both IPv4 and IPv6; on macOS the first
    # socket is often IPv6. Prefer an IPv4 socket so the client can connect
    # via 127.0.0.1 reliably.
    ipv4 = [
        s for s in server._server.sockets if s.family == _socket.AF_INET
    ]
    chosen = ipv4[0] if ipv4 else next(iter(server._server.sockets), None)
    if chosen is None:
        raise RuntimeError("server has no sockets")
    return int(chosen.getsockname()[1])


class TestServerDisableAuth:
    @pytest.mark.asyncio
    async def test_serves_without_api_key_when_disable_auth(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
        server = SpeechEngineServer(port=0, disable_auth=True)
        task = None
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                task = await _run_server_briefly(server)
                assert server._server is not None
        finally:
            await server.stop()
            if task is not None:
                await task

    @pytest.mark.asyncio
    async def test_emits_warning_when_disable_auth(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
        server = SpeechEngineServer(port=0, disable_auth=True)
        task = None
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                task = await _run_server_briefly(server)
                messages = [str(w.message) for w in caught]
                assert any("authentication is disabled" in m for m in messages)
        finally:
            await server.stop()
            if task is not None:
                await task

    @pytest.mark.asyncio
    async def test_accepts_unauthenticated_connection(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)

        init_ids: typing.List[str] = []

        async def on_init(conversation_id: str, session: typing.Any) -> None:
            init_ids.append(conversation_id)

        server = SpeechEngineServer(port=0, disable_auth=True, on_init=on_init)
        task = None
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                task = await _run_server_briefly(server)
            port = _server_port(server)
            async with websockets.connect(f"ws://127.0.0.1:{port}") as ws:  # type: ignore[attr-defined]
                await ws.send(
                    json.dumps({"type": "init", "conversation_id": "conv_1"})
                )
                await asyncio.sleep(0.1)
            assert init_ids == ["conv_1"]
        finally:
            await server.stop()
            if task is not None:
                await task

    @pytest.mark.asyncio
    async def test_rejects_missing_header_when_auth_enabled(self) -> None:
        server = SpeechEngineServer(port=0, api_key=TEST_API_KEY)
        task = None
        try:
            task = await _run_server_briefly(server)
            port = _server_port(server)
            with pytest.raises(websockets.exceptions.InvalidStatus) as exc:  # type: ignore[attr-defined]
                async with websockets.connect(f"ws://127.0.0.1:{port}"):  # type: ignore[attr-defined]
                    pass
            assert exc.value.response.status_code == 401
        finally:
            await server.stop()
            if task is not None:
                await task

    @pytest.mark.asyncio
    async def test_rejects_invalid_jwt_when_auth_enabled(self) -> None:
        server = SpeechEngineServer(port=0, api_key=TEST_API_KEY)
        task = None
        try:
            task = await _run_server_briefly(server)
            port = _server_port(server)
            with pytest.raises(websockets.exceptions.InvalidStatus) as exc:  # type: ignore[attr-defined]
                async with websockets.connect(  # type: ignore[attr-defined]
                    f"ws://127.0.0.1:{port}",
                    additional_headers={
                        "X-Elevenlabs-Speech-Engine-Authorization": "not.a.jwt"
                    },
                ):
                    pass
            assert exc.value.response.status_code == 401
        finally:
            await server.stop()
            if task is not None:
                await task
