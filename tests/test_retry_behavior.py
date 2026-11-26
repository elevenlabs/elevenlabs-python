"""Characterisation tests for the core HTTP retry policy.

Two separate questions are pinned down here, prompted by a user report of a
regression between v2.58.0 and v2.59.0:

1. Does the SDK retry a *cancelled* in-flight request? (It must not — a
   cancellation is the caller's decision, and retrying it would re-send an
   upload the caller explicitly abandoned.)
2. How many times does the SDK retry a genuinely retryable *response*?
   v2.58.0 defaulted to 0 effective retries; v2.59.0 defaults to 2.
"""

import asyncio
import typing

import httpx
import pytest

from elevenlabs.core import http_client as http_client_module
from elevenlabs.core.http_client import AsyncHttpClient, HttpClient


@pytest.fixture(autouse=True)
def _negligible_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    """Collapse the exponential backoff so retrying tests stay fast."""
    monkeypatch.setattr(http_client_module, "INITIAL_RETRY_DELAY_SECONDS", 0.001)


class _AttemptCounter:
    """Counts how many times the transport was asked to send the request."""

    def __init__(self) -> None:
        self.attempts = 0

    def record(self) -> None:
        self.attempts += 1


def _sync_client(handler: typing.Callable[[httpx.Request], httpx.Response]) -> HttpClient:
    return HttpClient(
        httpx_client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_timeout=lambda: None,
        base_headers=lambda: {},
        base_url=lambda: "https://api.elevenlabs.io",
    )


def _async_client(handler: typing.Callable[[httpx.Request], typing.Any]) -> AsyncHttpClient:
    return AsyncHttpClient(
        httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        base_timeout=lambda: None,
        base_headers=lambda: {},
        base_url=lambda: "https://api.elevenlabs.io",
    )


# ---------------------------------------------------------------------------
# 1. Cancellation must never be retried
# ---------------------------------------------------------------------------


async def test_task_cancellation_mid_flight_is_not_retried() -> None:
    """The reported scenario: cancel the task after the upload, before the response.

    The transport reads the full request body (upload complete), then hangs.
    Cancelling the awaiting task must surface CancelledError and leave the
    request at exactly one attempt -- no re-upload.
    """
    counter = _AttemptCounter()
    upload_received = asyncio.Event()

    async def handler(request: httpx.Request) -> httpx.Response:
        counter.record()
        assert request.content == b"audio-bytes"  # body was fully sent
        upload_received.set()
        await asyncio.Event().wait()  # hang, as a slow server would
        raise AssertionError("unreachable")

    client = _async_client(handler)
    task = asyncio.create_task(
        client.request(path="v1/speech-to-text", method="POST", content=b"audio-bytes")
    )

    await asyncio.wait_for(upload_received.wait(), timeout=5)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert counter.attempts == 1, "a cancelled request must not be re-sent"


async def test_cancelled_error_from_transport_is_not_retried() -> None:
    """CancelledError raised inside the transport propagates without a retry."""
    counter = _AttemptCounter()

    async def handler(request: httpx.Request) -> httpx.Response:
        counter.record()
        raise asyncio.CancelledError()

    with pytest.raises(asyncio.CancelledError):
        await _async_client(handler).request(path="v1/speech-to-text", method="POST")

    assert counter.attempts == 1


@pytest.mark.parametrize(
    "error",
    [
        httpx.ReadError("connection torn down while reading response"),
        httpx.WriteError("connection torn down while writing request"),
        httpx.RemoteProtocolError("server disconnected without sending a response"),
        httpx.ConnectError("connection refused"),
        httpx.ReadTimeout("timed out waiting for response"),
    ],
    ids=lambda e: type(e).__name__,
)
async def test_transport_errors_are_not_retried(error: Exception) -> None:
    """Connection-teardown style errors raise; they are not treated as retryable.

    ``_should_retry`` only ever inspects a *response* status code, so an
    exception short-circuits the retry logic entirely.
    """
    counter = _AttemptCounter()

    async def handler(request: httpx.Request) -> httpx.Response:
        counter.record()
        raise error

    with pytest.raises(type(error)):
        await _async_client(handler).request(path="v1/speech-to-text", method="POST")

    assert counter.attempts == 1


# ---------------------------------------------------------------------------
# 2. Retryable responses: the actual default-count change
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("status_code", [408, 409, 429, 500, 502, 503])
def test_retryable_status_is_retried_twice_by_default_sync(status_code: int) -> None:
    counter = _AttemptCounter()

    def handler(request: httpx.Request) -> httpx.Response:
        counter.record()
        return httpx.Response(status_code)

    response = _sync_client(handler).request(path="v1/speech-to-text", method="POST")

    assert response.status_code == status_code
    assert counter.attempts == 3, "one initial attempt plus two retries"


@pytest.mark.parametrize("status_code", [408, 409, 429, 500, 502, 503])
async def test_retryable_status_is_retried_twice_by_default_async(status_code: int) -> None:
    counter = _AttemptCounter()

    async def handler(request: httpx.Request) -> httpx.Response:
        counter.record()
        return httpx.Response(status_code)

    response = await _async_client(handler).request(path="v1/speech-to-text", method="POST")

    assert response.status_code == status_code
    assert counter.attempts == 3


@pytest.mark.parametrize("status_code", [200, 400, 401, 403, 404, 422])
async def test_non_retryable_status_is_not_retried(status_code: int) -> None:
    counter = _AttemptCounter()

    async def handler(request: httpx.Request) -> httpx.Response:
        counter.record()
        return httpx.Response(status_code)

    await _async_client(handler).request(path="v1/speech-to-text", method="POST")

    assert counter.attempts == 1


async def test_max_retries_zero_opts_out_of_retries() -> None:
    """Callers can restore the pre-v2.59.0 behaviour with max_retries=0."""
    counter = _AttemptCounter()

    async def handler(request: httpx.Request) -> httpx.Response:
        counter.record()
        return httpx.Response(500)

    await _async_client(handler).request(
        path="v1/speech-to-text", method="POST", request_options={"max_retries": 0}
    )

    assert counter.attempts == 1


async def test_retry_resends_the_full_request_body() -> None:
    """Each retry re-uploads the body -- the cost that makes the default matter."""
    bodies: typing.List[bytes] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        bodies.append(request.content)
        return httpx.Response(503)

    await _async_client(handler).request(
        path="v1/speech-to-text", method="POST", content=b"audio-bytes"
    )

    assert bodies == [b"audio-bytes"] * 3
