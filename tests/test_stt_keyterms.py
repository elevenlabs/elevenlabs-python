import httpx
import pytest

from elevenlabs import AsyncElevenLabs, ElevenLabs
from elevenlabs.core.api_error import ApiError


def _assert_repeated_keyterms(request: httpx.Request) -> None:
    body = request.content
    assert body.count(b'name="keyterms"') == 2
    assert b"hello" in body
    assert b"world" in body
    assert b'["hello", "world"]' not in body


def test_convert_sends_keyterms_as_repeated_multipart_fields() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        _assert_repeated_keyterms(request)
        return httpx.Response(400, json={})

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = ElevenLabs(api_key="test", httpx_client=http_client)
        with pytest.raises(ApiError):
            client.speech_to_text.convert(
                file=b"audio",
                model_id="scribe_v2",
                keyterms=["hello", "world"],
            )


@pytest.mark.asyncio
async def test_async_convert_sends_keyterms_as_repeated_multipart_fields() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        _assert_repeated_keyterms(request)
        return httpx.Response(400, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        client = AsyncElevenLabs(api_key="test", httpx_client=http_client)
        with pytest.raises(ApiError):
            await client.speech_to_text.convert(
                file=b"audio",
                model_id="scribe_v2",
                keyterms=["hello", "world"],
            )
