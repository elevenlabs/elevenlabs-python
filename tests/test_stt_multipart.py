"""Multipart encoding of the speech-to-text convert body.

Regression tests for https://github.com/elevenlabs/elevenlabs-python/issues/819, where the
generated client JSON-encoded list-valued form fields instead of repeating them.
"""

import typing

import httpx
import pytest

from elevenlabs.client import AsyncElevenLabs, ElevenLabs

TRANSCRIPTION = {
    "language_code": "en",
    "language_probability": 1.0,
    "text": "Hello world",
    "words": [],
}


def _parse_fields(request: httpx.Request) -> typing.List[typing.Tuple[str, str]]:
    """Return the (name, value) pairs of a multipart body, in order, excluding file parts."""
    content_type = request.headers["content-type"]
    boundary = content_type.split("boundary=")[1].encode("utf-8")

    fields = []
    for part in request.content.split(b"--" + boundary):
        headers, _, body = part.partition(b"\r\n\r\n")
        if b'name="' not in headers or b"filename=" in headers:
            continue
        name = headers.split(b'name="')[1].split(b'"')[0]
        fields.append((name.decode("utf-8"), body.rstrip(b"\r\n").decode("utf-8")))
    return fields


class _Recorder:
    def __init__(self) -> None:
        self.fields: typing.List[typing.Tuple[str, str]] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.fields = _parse_fields(request)
        return httpx.Response(200, json=TRANSCRIPTION)

    @property
    def names(self) -> typing.List[str]:
        return [name for name, _ in self.fields]

    def values(self, name: str) -> typing.List[str]:
        return [value for field_name, value in self.fields if field_name == name]


def _client(recorder: _Recorder) -> ElevenLabs:
    return ElevenLabs(api_key="test", httpx_client=httpx.Client(transport=httpx.MockTransport(recorder)))


def _async_client(recorder: _Recorder) -> AsyncElevenLabs:
    return AsyncElevenLabs(
        api_key="test", httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(recorder))
    )


def test_keyterms_are_repeated_fields():
    recorder = _Recorder()
    _client(recorder).speech_to_text.convert(file=b"audio", model_id="scribe_v2", keyterms=["hello", "world"])

    assert recorder.values("keyterms") == ["hello", "world"]


def test_keyterms_are_repeated_fields_on_raw_response_client():
    recorder = _Recorder()
    _client(recorder).speech_to_text.with_raw_response.convert(
        file=b"audio", model_id="scribe_v2", keyterms=["hello", "world"]
    )

    assert recorder.values("keyterms") == ["hello", "world"]


@pytest.mark.asyncio
async def test_keyterms_are_repeated_fields_async():
    recorder = _Recorder()
    await _async_client(recorder).speech_to_text.convert(
        file=b"audio", model_id="scribe_v2", keyterms=["hello", "world"]
    )

    assert recorder.values("keyterms") == ["hello", "world"]


def test_keyterms_containing_json_characters_are_sent_verbatim():
    recorder = _Recorder()
    _client(recorder).speech_to_text.convert(file=b"audio", model_id="scribe_v2", keyterms=['a "quoted" term'])

    assert recorder.values("keyterms") == ['a "quoted" term']


def test_omitted_fields_are_not_sent():
    recorder = _Recorder()
    _client(recorder).speech_to_text.convert(file=b"audio", model_id="scribe_v2")

    assert recorder.names == ["model_id"]


def test_entity_detection_string_is_not_quoted():
    recorder = _Recorder()
    _client(recorder).speech_to_text.convert(file=b"audio", model_id="scribe_v2", entity_detection="pii")

    assert recorder.values("entity_detection") == ["pii"]


def test_entity_redaction_list_is_repeated():
    recorder = _Recorder()
    _client(recorder).speech_to_text.convert(
        file=b"audio", model_id="scribe_v2", entity_detection=["pii", "phi"], entity_redaction=["pii"]
    )

    assert recorder.values("entity_detection") == ["pii", "phi"]
    assert recorder.values("entity_redaction") == ["pii"]


def test_webhook_metadata_object_stays_json_encoded():
    recorder = _Recorder()
    _client(recorder).speech_to_text.convert(
        file=b"audio", model_id="scribe_v2", webhook=True, webhook_metadata={"job_id": "abc"}
    )

    assert recorder.values("webhook_metadata") == ['{"job_id": "abc"}']


def test_webhook_metadata_string_is_not_quoted():
    recorder = _Recorder()
    _client(recorder).speech_to_text.convert(
        file=b"audio", model_id="scribe_v2", webhook=True, webhook_metadata='{"job_id": "abc"}'
    )

    assert recorder.values("webhook_metadata") == ['{"job_id": "abc"}']


def test_other_fields_are_untouched():
    recorder = _Recorder()
    _client(recorder).speech_to_text.convert(
        file=b"audio", model_id="scribe_v2", language_code="en", diarize=True, num_speakers=2
    )

    assert dict(recorder.fields) == {
        "model_id": "scribe_v2",
        "language_code": "en",
        "diarize": "true",
        "num_speakers": "2",
    }
