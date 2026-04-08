import os
from unittest import mock

import pytest

from elevenlabs.client import ElevenLabs, AsyncElevenLabs, _resolve_api_key


class TestResolveApiKey:
    def test_explicit_key(self):
        assert _resolve_api_key("my-key") == "my-key"

    def test_env_var_fallback(self):
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "env-key"}):
            assert _resolve_api_key(None) == "env-key"

    def test_explicit_key_takes_precedence_over_env(self):
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "env-key"}):
            assert _resolve_api_key("explicit-key") == "explicit-key"

    def test_missing_key_raises(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="API Key"):
                _resolve_api_key(None)

    def test_empty_string_key_raises(self):
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": ""}, clear=True):
            with pytest.raises(ValueError, match="API Key"):
                _resolve_api_key(None)


class TestElevenLabsInit:
    def test_explicit_api_key(self):
        client = ElevenLabs(api_key="test-key")
        headers = client._client_wrapper.get_headers()
        assert headers["xi-api-key"] == "test-key"

    def test_env_var_api_key(self):
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "env-key"}):
            client = ElevenLabs()
            headers = client._client_wrapper.get_headers()
            assert headers["xi-api-key"] == "env-key"

    def test_missing_api_key_raises(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="API Key"):
                ElevenLabs()


class TestAsyncElevenLabsInit:
    def test_explicit_api_key(self):
        client = AsyncElevenLabs(api_key="test-key")
        headers = client._client_wrapper.get_headers()
        assert headers["xi-api-key"] == "test-key"

    def test_env_var_api_key(self):
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "env-key"}):
            client = AsyncElevenLabs()
            headers = client._client_wrapper.get_headers()
            assert headers["xi-api-key"] == "env-key"

    def test_missing_api_key_raises(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="API Key"):
                AsyncElevenLabs()
