import typing

import httpx
import pytest
import typing_extensions

from elevenlabs.core.http_sse import aconnect_sse, connect_sse
from elevenlabs.core.http_sse._exceptions import SSEError


class _SyncFakeResponse:
    headers = {"content-type": "text/event-stream"}

    def iter_bytes(self) -> typing.Iterator[bytes]:
        return iter([b"data: hello\n\n"])


class _AsyncFakeResponse:
    headers = {"content-type": "text/event-stream"}

    async def aiter_lines(self) -> typing.AsyncIterator[str]:
        yield "data: hello\n"
        yield "\n"


class _SyncFakeStream:
    def __init__(self, method: str, url: str, headers: typing.Optional[typing.Dict[str, str]] = None, **kwargs: typing.Any):
        self._headers = headers

    def __enter__(self) -> _SyncFakeResponse:
        return _SyncFakeResponse()

    def __exit__(self, exc_type: typing.Any, exc: typing.Any, tb: typing.Any) -> typing_extensions.Literal[False]:
        return False


class _AsyncFakeStream:
    def __init__(self, method: str, url: str, headers: typing.Optional[typing.Dict[str, str]] = None, **kwargs: typing.Any):
        self._headers = headers

    async def __aenter__(self) -> _AsyncFakeResponse:
        return _AsyncFakeResponse()

    async def __aexit__(self, exc_type: typing.Any, exc: typing.Any, tb: typing.Any) -> bool:
        return False


def test_connect_sse_accept_header(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: typing.Dict[str, typing.Any] = {}

    class FakeStream(_SyncFakeStream):
        def __init__(self, method: str, url: str, headers: typing.Optional[typing.Dict[str, str]] = None, **kwargs: typing.Any):
            super().__init__(method, url, headers=headers, **kwargs)
            captured["headers"] = headers

    monkeypatch.setattr(httpx.Client, "stream", FakeStream)

    client = httpx.Client()
    with connect_sse(client, "GET", "https://example.com/events") as es:
        events = list(es.iter_sse())

    assert captured["headers"]["Accept"] == "application/json, text/event-stream"
    assert [event.data for event in events] == ["hello"]


def test_connect_sse_preserves_other_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: typing.Dict[str, typing.Any] = {}

    class FakeStream(_SyncFakeStream):
        def __init__(self, method: str, url: str, headers: typing.Optional[typing.Dict[str, str]] = None, **kwargs: typing.Any):
            super().__init__(method, url, headers=headers, **kwargs)
            captured["headers"] = headers

    monkeypatch.setattr(httpx.Client, "stream", FakeStream)

    client = httpx.Client()
    with connect_sse(client, "GET", "https://example.com/events", headers={"X-Custom": "v"}) as es:
        list(es.iter_sse())

    assert captured["headers"]["X-Custom"] == "v"
    assert captured["headers"]["Cache-Control"] == "no-store"


def test_connect_sse_rejects_non_sse_content_type(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeResponse(_SyncFakeResponse):
        headers = {"content-type": "application/json"}

    class FakeStream(_SyncFakeStream):
        def __enter__(self) -> FakeResponse:
            return FakeResponse()

    monkeypatch.setattr(httpx.Client, "stream", FakeStream)

    client = httpx.Client()
    with connect_sse(client, "GET", "https://example.com/events") as es:
        with pytest.raises(SSEError):
            list(es.iter_sse())


async def test_aconnect_sse_accept_header(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: typing.Dict[str, typing.Any] = {}

    class FakeStream(_AsyncFakeStream):
        def __init__(self, method: str, url: str, headers: typing.Optional[typing.Dict[str, str]] = None, **kwargs: typing.Any):
            super().__init__(method, url, headers=headers, **kwargs)
            captured["headers"] = headers

    monkeypatch.setattr(httpx.AsyncClient, "stream", FakeStream)

    client = httpx.AsyncClient()
    async with aconnect_sse(client, "GET", "https://example.com/events") as es:
        events = [event async for event in es.aiter_sse()]

    assert captured["headers"]["Accept"] == "application/json, text/event-stream"
    assert [event.data for event in events] == ["hello"]


async def test_aconnect_sse_preserves_other_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: typing.Dict[str, typing.Any] = {}

    class FakeStream(_AsyncFakeStream):
        def __init__(self, method: str, url: str, headers: typing.Optional[typing.Dict[str, str]] = None, **kwargs: typing.Any):
            super().__init__(method, url, headers=headers, **kwargs)
            captured["headers"] = headers

    monkeypatch.setattr(httpx.AsyncClient, "stream", FakeStream)

    client = httpx.AsyncClient()
    async with aconnect_sse(client, "GET", "https://example.com/events", headers={"X-Custom": "v"}) as es:
        list([event async for event in es.aiter_sse()])

    assert captured["headers"]["X-Custom"] == "v"
    assert captured["headers"]["Cache-Control"] == "no-store"
    assert captured["headers"]["Accept"] == "application/json, text/event-stream"


async def test_aconnect_sse_rejects_non_sse_content_type(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeResponse(_AsyncFakeResponse):
        headers = {"content-type": "application/json"}

    class FakeStream(_AsyncFakeStream):
        async def __aenter__(self) -> FakeResponse:
            return FakeResponse()

    monkeypatch.setattr(httpx.AsyncClient, "stream", FakeStream)

    client = httpx.AsyncClient()
    async with aconnect_sse(client, "GET", "https://example.com/events") as es:
        with pytest.raises(SSEError):
            list([event async for event in es.aiter_sse()])
