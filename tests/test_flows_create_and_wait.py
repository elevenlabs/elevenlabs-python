"""Tests for the flows `create_and_wait` helpers in flows_custom.py."""

import typing
from unittest.mock import patch

import httpx
import pytest

from elevenlabs import AsyncElevenLabs, ElevenLabs
from elevenlabs.flows_custom import FlowsWaitTimeoutError, _poll_delay

Reply = typing.Tuple[int, typing.Dict[str, typing.Any], typing.Dict[str, str]]


def _transport(replies: typing.List[Reply], seen: typing.List[httpx.Request]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        status_code, body, headers = replies.pop(0)
        return httpx.Response(status_code, json=body, headers=headers)

    return httpx.MockTransport(handler)


def _sync_client(replies: typing.List[Reply], seen: typing.List[httpx.Request]) -> ElevenLabs:
    return ElevenLabs(
        api_key="test", base_url="https://api.test", httpx_client=httpx.Client(transport=_transport(replies, seen))
    )


def _async_client(replies: typing.List[Reply], seen: typing.List[httpx.Request]) -> AsyncElevenLabs:
    return AsyncElevenLabs(
        api_key="test",
        base_url="https://api.test",
        httpx_client=httpx.AsyncClient(transport=_transport(replies, seen)),
    )


def _run(status: str) -> typing.Dict[str, typing.Any]:
    return {"id": "run_1", "template_id": "tpl_1", "version_id": "ver_1", "status": status, "outputs": {}}


COMPLETED_IMAGE = {
    "id": "gen_1",
    "status": "completed",
    "content_url": "https://cdn.test/out.png",
    "content_mime_type": "image/png",
}

IMAGE_REQUEST = {"model_id": "bytedance-seedream-5-lite", "prompt": "a corgi"}


def test_poll_delay_uses_retry_after_with_jitter() -> None:
    with patch("elevenlabs.core.http_client.random", return_value=0.5):
        assert _poll_delay({"retry-after": "5"}, 1.0) == pytest.approx(5.5)


def test_poll_delay_falls_back_to_minimum() -> None:
    with patch("elevenlabs.core.http_client.random", return_value=0.0):
        assert _poll_delay({}, 2.0) == 2.0
        assert _poll_delay({"retry-after": "0"}, 2.0) == 2.0
        assert _poll_delay({"retry-after": "not-a-date"}, 2.0) == 2.0


def test_image_create_and_wait_polls_until_completed() -> None:
    seen: typing.List[httpx.Request] = []
    replies: typing.List[Reply] = [
        (200, {"id": "gen_1", "status": "pending"}, {"retry-after": "3"}),
        (200, {"id": "gen_1", "status": "generating"}, {"retry-after": "7"}),
        (200, COMPLETED_IMAGE, {}),
    ]
    client = _sync_client(replies, seen)

    with patch("elevenlabs.flows_custom.time.sleep") as sleep, patch(
        "elevenlabs.core.http_client.random", return_value=0.0
    ):
        result = client.flows.image.create_and_wait(request=IMAGE_REQUEST)  # type: ignore[arg-type]

    assert result.status == "completed"
    assert result.id == "gen_1"
    assert [call.args[0] for call in sleep.call_args_list] == [3.0, 7.0]
    assert [(r.method, r.url.path) for r in seen] == [
        ("POST", "/v1/flows/image"),
        ("GET", "/v1/flows/image/gen_1"),
        ("GET", "/v1/flows/image/gen_1"),
    ]


def test_failed_generation_is_returned_not_raised() -> None:
    seen: typing.List[httpx.Request] = []
    replies: typing.List[Reply] = [
        (200, {"id": "gen_1", "status": "pending"}, {}),
        (
            200,
            {"id": "gen_1", "status": "failed", "failure_reason": "content_moderation", "error_message": "nope"},
            {},
        ),
    ]
    client = _sync_client(replies, seen)

    with patch("elevenlabs.flows_custom.time.sleep"):
        result = client.flows.video.create_and_wait(request={"model_id": "bytedance-seedance-v2", "prompt": "a corgi"})  # type: ignore[arg-type]

    assert result.status == "failed"
    assert seen[1].url.path == "/v1/flows/video/gen_1"


def test_timeout_raises_with_generation_id() -> None:
    seen: typing.List[httpx.Request] = []
    replies: typing.List[Reply] = [
        (200, {"id": "gen_1", "status": "pending"}, {"retry-after": "30"}),
        (200, {"id": "gen_1", "status": "generating"}, {"retry-after": "30"}),
    ]
    client = _sync_client(replies, seen)
    clock = iter([0.0, 0.0, 10.0])

    with patch("elevenlabs.flows_custom.time.monotonic", side_effect=lambda: next(clock)), patch(
        "elevenlabs.flows_custom.time.sleep"
    ) as sleep:
        with pytest.raises(FlowsWaitTimeoutError) as exc_info:
            client.flows.text_to_speech.create_and_wait(request={"model_id": "eleven_flash_v2_5", "text": "hi", "voice": "JBFqnCBsd6RMkjVDRZzb"}, timeout=10)  # type: ignore[arg-type]

    # The last sleep is cut short to land on the deadline, then one final GET runs.
    assert [call.args[0] for call in sleep.call_args_list] == [10.0]
    assert exc_info.value.id == "gen_1"
    assert exc_info.value.template_id is None
    assert exc_info.value.last_response.status == "generating"
    assert len(seen) == 2


def test_template_run_create_and_wait() -> None:
    seen: typing.List[httpx.Request] = []
    replies: typing.List[Reply] = [
        (200, _run("pending"), {"retry-after": "2"}),
        (200, _run("completed"), {}),
    ]
    client = _sync_client(replies, seen)

    with patch("elevenlabs.flows_custom.time.sleep"):
        result = client.flows.templates.runs.create_and_wait("tpl_1", inputs={})

    assert result.status == "completed"
    assert [(r.method, r.url.path) for r in seen] == [
        ("POST", "/v1/flows/templates/tpl_1/runs"),
        ("GET", "/v1/flows/templates/tpl_1/runs/run_1"),
    ]


def test_template_run_already_terminal_on_create_skips_polling() -> None:
    seen: typing.List[httpx.Request] = []
    client = _sync_client([(200, _run("completed"), {})], seen)

    with patch("elevenlabs.flows_custom.time.sleep") as sleep:
        result = client.flows.templates.runs.create_and_wait("tpl_1", inputs={})

    assert result.status == "completed"
    sleep.assert_not_called()
    assert len(seen) == 1


def test_template_run_timeout_carries_template_id() -> None:
    seen: typing.List[httpx.Request] = []
    client = _sync_client([(200, _run("pending"), {})], seen)

    with pytest.raises(FlowsWaitTimeoutError) as exc_info:
        client.flows.templates.runs.create_and_wait("tpl_1", inputs={}, timeout=0)

    assert exc_info.value.id == "run_1"
    assert exc_info.value.template_id == "tpl_1"


async def test_async_image_create_and_wait() -> None:
    seen: typing.List[httpx.Request] = []
    replies: typing.List[Reply] = [
        (200, {"id": "gen_1", "status": "pending"}, {"retry-after": "4"}),
        (200, COMPLETED_IMAGE, {}),
    ]
    client = _async_client(replies, seen)

    with patch("elevenlabs.flows_custom.asyncio.sleep") as sleep, patch(
        "elevenlabs.core.http_client.random", return_value=0.0
    ):
        result = await client.flows.image.create_and_wait(request=IMAGE_REQUEST)  # type: ignore[arg-type]

    assert result.status == "completed"
    assert [call.args[0] for call in sleep.call_args_list] == [4.0]


async def test_async_template_run_create_and_wait() -> None:
    seen: typing.List[httpx.Request] = []
    replies: typing.List[Reply] = [
        (200, _run("generating"), {}),
        (200, _run("failed"), {}),
    ]
    client = _async_client(replies, seen)

    with patch("elevenlabs.flows_custom.asyncio.sleep"):
        result = await client.flows.templates.runs.create_and_wait("tpl_1", inputs={})

    assert result.status == "failed"
    assert seen[1].url.path == "/v1/flows/templates/tpl_1/runs/run_1"
