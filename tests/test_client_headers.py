"""Tests that the user-facing ElevenLabs / AsyncElevenLabs classes forward
the ``headers`` and ``follow_redirects`` kwargs through to the underlying
client wrapper / httpx client.

Regression coverage for the case where ``ElevenLabs(headers={...})`` and
``ElevenLabs(follow_redirects=False)`` raised TypeError because the
subclass's hand-rolled ``__init__`` did not accept or forward kwargs that
``BaseElevenLabs`` supports.
"""

import pytest

from elevenlabs.client import AsyncElevenLabs, ElevenLabs


def test_sync_client_accepts_headers_kwarg():
    """ElevenLabs(headers=...) does not raise and stores the headers."""
    custom = {"x-trace-id": "abc-123", "x-tenant": "acme"}
    client = ElevenLabs(api_key="sk-test", headers=custom)
    assert client._client_wrapper.get_custom_headers() == custom


def test_sync_client_headers_default_is_none():
    """Omitting headers leaves the wrapper's custom headers unset (backward-compatible)."""
    client = ElevenLabs(api_key="sk-test")
    assert client._client_wrapper.get_custom_headers() is None


def test_sync_client_custom_headers_appear_in_merged_headers():
    """Headers from the constructor are merged into get_headers() output."""
    client = ElevenLabs(api_key="sk-test", headers={"x-trace-id": "abc-123"})
    merged = client._client_wrapper.get_headers()
    assert merged.get("x-trace-id") == "abc-123"


async def test_async_client_accepts_headers_kwarg():
    """AsyncElevenLabs(headers=...) does not raise and stores the headers."""
    custom = {"x-trace-id": "abc-123"}
    client = AsyncElevenLabs(api_key="sk-test", headers=custom)
    assert client._client_wrapper.get_custom_headers() == custom


async def test_async_client_headers_default_is_none():
    """Omitting headers on AsyncElevenLabs leaves custom headers unset."""
    client = AsyncElevenLabs(api_key="sk-test")
    assert client._client_wrapper.get_custom_headers() is None


def test_sync_constructor_signature_advertises_headers():
    """`headers` is a documented keyword-only parameter on ElevenLabs.__init__."""
    import inspect

    sig = inspect.signature(ElevenLabs.__init__)
    assert "headers" in sig.parameters
    assert sig.parameters["headers"].kind == inspect.Parameter.KEYWORD_ONLY


def test_async_constructor_signature_advertises_headers():
    """`headers` is a documented keyword-only parameter on AsyncElevenLabs.__init__."""
    import inspect

    sig = inspect.signature(AsyncElevenLabs.__init__)
    assert "headers" in sig.parameters
    assert sig.parameters["headers"].kind == inspect.Parameter.KEYWORD_ONLY


def test_sync_client_accepts_follow_redirects_false():
    """ElevenLabs(follow_redirects=False) propagates to the default httpx client."""
    client = ElevenLabs(api_key="sk-test", follow_redirects=False)
    assert client._client_wrapper.httpx_client.httpx_client.follow_redirects is False


def test_sync_client_follow_redirects_default_is_true():
    """Omitting follow_redirects keeps the parent's default of True."""
    client = ElevenLabs(api_key="sk-test")
    assert client._client_wrapper.httpx_client.httpx_client.follow_redirects is True


def test_async_client_accepts_follow_redirects_false():
    """AsyncElevenLabs(follow_redirects=False) propagates to the default httpx client."""
    client = AsyncElevenLabs(api_key="sk-test", follow_redirects=False)
    assert client._client_wrapper.httpx_client.httpx_client.follow_redirects is False


def test_async_client_follow_redirects_default_is_true():
    """Omitting follow_redirects on AsyncElevenLabs keeps the parent's default of True."""
    client = AsyncElevenLabs(api_key="sk-test")
    assert client._client_wrapper.httpx_client.httpx_client.follow_redirects is True


def test_sync_constructor_signature_advertises_follow_redirects():
    """`follow_redirects` is a documented keyword-only parameter on ElevenLabs.__init__."""
    import inspect

    sig = inspect.signature(ElevenLabs.__init__)
    assert "follow_redirects" in sig.parameters
    assert sig.parameters["follow_redirects"].kind == inspect.Parameter.KEYWORD_ONLY


def test_async_constructor_signature_advertises_follow_redirects():
    """`follow_redirects` is a documented keyword-only parameter on AsyncElevenLabs.__init__."""
    import inspect

    sig = inspect.signature(AsyncElevenLabs.__init__)
    assert "follow_redirects" in sig.parameters
    assert sig.parameters["follow_redirects"].kind == inspect.Parameter.KEYWORD_ONLY
