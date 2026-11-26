import typing

import httpx
import pytest

from elevenlabs.client import AsyncElevenLabs, ElevenLabs


@pytest.mark.parametrize("custom_timeout", [7.0, None])
@pytest.mark.parametrize(
    "timeout_kwargs, expected_override", [({}, None), ({"timeout": None}, None), ({"timeout": 11}, 11)]
)
def test_sync_client_uses_custom_http_client_timeout(
    custom_timeout: typing.Optional[float],
    timeout_kwargs: typing.Dict[str, typing.Any],
    expected_override: typing.Optional[float],
) -> None:
    seen: typing.List[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=[])

    with httpx.Client(transport=httpx.MockTransport(handler), timeout=custom_timeout) as http:
        client = ElevenLabs(api_key="test", httpx_client=http, **timeout_kwargs)
        client.models.list()
        client.models.list(request_options={"timeout_in_seconds": 2})

    expected = custom_timeout if expected_override is None else expected_override
    assert seen[0].extensions["timeout"] == dict.fromkeys(["connect", "read", "write", "pool"], expected)
    assert seen[1].extensions["timeout"] == dict.fromkeys(["connect", "read", "write", "pool"], 2)


@pytest.mark.parametrize("custom_timeout", [7.0, None])
@pytest.mark.parametrize(
    "timeout_kwargs, expected_override", [({}, None), ({"timeout": None}, None), ({"timeout": 11}, 11)]
)
async def test_async_client_uses_custom_http_client_timeout(
    custom_timeout: typing.Optional[float],
    timeout_kwargs: typing.Dict[str, typing.Any],
    expected_override: typing.Optional[float],
) -> None:
    seen: typing.List[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=[])

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler), timeout=custom_timeout) as http:
        client = AsyncElevenLabs(api_key="test", httpx_client=http, **timeout_kwargs)
        await client.models.list()
        await client.models.list(request_options={"timeout_in_seconds": 2})

    expected = custom_timeout if expected_override is None else expected_override
    assert seen[0].extensions["timeout"] == dict.fromkeys(["connect", "read", "write", "pool"], expected)
    assert seen[1].extensions["timeout"] == dict.fromkeys(["connect", "read", "write", "pool"], 2)


@pytest.mark.parametrize("client_cls", [ElevenLabs, AsyncElevenLabs])
def test_default_http_client_keeps_240_second_timeout(client_cls: typing.Any) -> None:
    client = client_cls(api_key="test")
    assert client._client_wrapper.get_timeout() == 240
