"""Tests for Speech Engine JWT verification."""

import base64
import hashlib
import hmac
import json
import time
import typing

import pytest

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


class TestVerifyRequest:
    def test_valid_header(self) -> None:
        resource = SpeechEngineResource(
            "seng_test", client_options=_FakeClientWrapper(TEST_API_KEY)
        )
        token = _create_test_jwt(_valid_payload())
        assert resource.verify_request(
            {"x-elevenlabs-speech-engine-authorization": token}
        )

    def test_missing_header(self) -> None:
        resource = SpeechEngineResource(
            "seng_test", client_options=_FakeClientWrapper(TEST_API_KEY)
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
            "seng_test", client_options=_FakeClientWrapper(TEST_API_KEY)
        )
        assert not resource.verify_request(
            {"x-elevenlabs-speech-engine-authorization": "bad-token"}
        )


# ---------------------------------------------------------------------------
# SpeechEngineServer — api_key requirement
# ---------------------------------------------------------------------------


class TestServerApiKeyRequirement:
    @pytest.mark.asyncio
    async def test_raises_without_api_key(self) -> None:
        from elevenlabs.speech_engine import SpeechEngineServer

        server = SpeechEngineServer(port=0)
        with pytest.raises(RuntimeError, match="API key"):
            await server.serve()
