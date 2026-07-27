"""Regression tests for issue #819: keyterms must be repeated multipart fields."""

from __future__ import annotations

import json
import re
import typing

import httpx
import pytest

from elevenlabs.client import AsyncElevenLabs, ElevenLabs

SAMPLE_TRANSCRIPT = {
    "language_code": "eng",
    "language_probability": 0.99,
    "text": "hello world",
    "words": [],
}


def _form_field_values(body: bytes, name: str) -> typing.List[str]:
    """Extract values for a multipart form field by name."""
    pattern = (
        rb'Content-Disposition: form-data; name="'
        + name.encode()
        + rb'"(?:; filename="[^"]*")?\r\n(?:Content-Type: [^\r\n]+\r\n)?\r\n'
    )
    values: typing.List[str] = []
    for match in re.finditer(pattern, body):
        start = match.end()
        end = body.find(b"\r\n--", start)
        if end == -1:
            end = len(body)
        values.append(body[start:end].decode())
    return values


def _sync_client_capturing_body(captured: typing.Dict[str, typing.Any]) -> ElevenLabs:
    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = request.read()
        captured["url"] = str(request.url)
        return httpx.Response(200, json=SAMPLE_TRANSCRIPT)

    return ElevenLabs(
        api_key="test-key",
        httpx_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def _async_client_capturing_body(captured: typing.Dict[str, typing.Any]) -> AsyncElevenLabs:
    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = request.read()
        captured["url"] = str(request.url)
        return httpx.Response(200, json=SAMPLE_TRANSCRIPT)

    return AsyncElevenLabs(
        api_key="test-key",
        httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


def test_keyterms_sent_as_repeated_multipart_fields() -> None:
    """Each keyterm must be its own form field, not a JSON array string."""
    captured: typing.Dict[str, typing.Any] = {}
    client = _sync_client_capturing_body(captured)

    result = client.speech_to_text.convert(
        model_id="scribe_v2",
        file=("audio.mp3", b"fake-audio", "audio/mpeg"),
        keyterms=["hello", "world", "technical term"],
    )

    assert result.text == "hello world"
    body = captured["body"]
    assert _form_field_values(body, "keyterms") == ["hello", "world", "technical term"]
    assert b'name="keyterms"\r\n\r\n[' not in body
    assert json.dumps(["hello", "world", "technical term"]).encode() not in body


def test_keyterms_omitted_when_not_provided() -> None:
    """Omitted keyterms must not be sent as the literal string 'null'."""
    captured: typing.Dict[str, typing.Any] = {}
    client = _sync_client_capturing_body(captured)

    client.speech_to_text.convert(
        model_id="scribe_v2",
        file=("audio.mp3", b"fake-audio", "audio/mpeg"),
    )

    body = captured["body"]
    assert _form_field_values(body, "keyterms") == []
    assert b'name="keyterms"' not in body


def test_raw_response_convert_also_fixes_keyterms() -> None:
    """with_raw_response.convert must use the same multipart encoding."""
    captured: typing.Dict[str, typing.Any] = {}
    client = _sync_client_capturing_body(captured)

    response = client.speech_to_text.with_raw_response.convert(
        model_id="scribe_v2",
        file=("audio.mp3", b"fake-audio", "audio/mpeg"),
        keyterms=["ElevenLabs", "Scribe"],
    )

    assert response.data.text == "hello world"
    assert _form_field_values(captured["body"], "keyterms") == ["ElevenLabs", "Scribe"]


@pytest.mark.asyncio
async def test_async_keyterms_sent_as_repeated_multipart_fields() -> None:
    captured: typing.Dict[str, typing.Any] = {}
    client = _async_client_capturing_body(captured)

    result = await client.speech_to_text.convert(
        model_id="scribe_v2",
        file=("audio.mp3", b"fake-audio", "audio/mpeg"),
        keyterms=["hello", "world"],
    )

    assert result.text == "hello world"
    assert _form_field_values(captured["body"], "keyterms") == ["hello", "world"]
    await client._client_wrapper.httpx_client.httpx_client.aclose()
