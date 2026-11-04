"""Regression tests for list-of-primitive multipart form fields.

Generator ``fern-python-sdk`` 4.46.9 started serializing every non-scalar
multipart form field with ``json.dumps(jsonable_encoder(...))``. ``List[str]``
fields are not scalars, so ``speech_to_text.convert(keyterms=["a", "b"])`` went
over the wire as a single ``["a", "b"]`` string instead of two ``keyterms``
form fields, and the API validated the whole JSON array against its per-item
limits (``invalid_keyword_length``).

See https://github.com/elevenlabs/elevenlabs-python/issues/819 and the fix in
https://github.com/elevenlabs/elevenlabs-python/pull/825. The fields live in
Fern-generated ``raw_client.py`` files and the fix is re-applied on every
regeneration by Fern Replay, so these tests guard against a regeneration
silently reverting it.
"""

import email
import email.message
import json
import typing

import httpx
import pytest

from elevenlabs.client import AsyncElevenLabs, ElevenLabs

KEYTERMS = ["hello world", "ElevenLabs"]
TAGS = ["ambient", "lo-fi"]
GENRES = ["fiction", "sci-fi"]
LOCATORS = ['{"pronunciation_dictionary_id": "abc", "version_id": "def"}']


class _RequestCaptured(Exception):
    """Raised from the mock transport once the outgoing request is recorded."""

    def __init__(self, request: httpx.Request) -> None:
        super().__init__("request captured")
        self.request = request


def _capture_sync(call: typing.Callable[[ElevenLabs], typing.Any]) -> httpx.Request:
    """Run ``call`` against a client whose transport records and aborts the request."""

    def handler(request: httpx.Request) -> httpx.Response:
        request.read()
        raise _RequestCaptured(request)

    client = ElevenLabs(api_key="sk-test", httpx_client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(_RequestCaptured) as excinfo:
        call(client)
    return excinfo.value.request


async def _capture_async(call: typing.Callable[[AsyncElevenLabs], typing.Awaitable[typing.Any]]) -> httpx.Request:
    """Async counterpart of :func:`_capture_sync`."""

    async def handler(request: httpx.Request) -> httpx.Response:
        await request.aread()
        raise _RequestCaptured(request)

    client = AsyncElevenLabs(api_key="sk-test", httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    with pytest.raises(_RequestCaptured) as excinfo:
        await call(client)
    return excinfo.value.request


def _form_fields(request: httpx.Request) -> typing.List[typing.Tuple[str, str]]:
    """Parse a multipart request body into an ordered list of (name, value) pairs."""
    content_type = request.headers["content-type"]
    assert content_type.startswith("multipart/form-data"), content_type

    message = email.message_from_bytes(b"Content-Type: " + content_type.encode() + b"\r\n\r\n" + request.content)
    fields: typing.List[typing.Tuple[str, str]] = []
    for part in typing.cast(typing.List[email.message.Message], message.get_payload()):
        name = part.get_param("name", header="content-disposition")
        payload = part.get_payload(decode=True)
        if name is None or not isinstance(payload, bytes):
            continue
        fields.append((str(name), payload.decode("utf-8")))
    return fields


def _values(request: httpx.Request, name: str) -> typing.List[str]:
    return [value for field_name, value in _form_fields(request) if field_name == name]


def _stt_convert(client: ElevenLabs) -> typing.Any:
    return client.speech_to_text.convert(model_id="scribe_v1", keyterms=KEYTERMS)


async def _stt_convert_async(client: AsyncElevenLabs) -> typing.Any:
    return await client.speech_to_text.convert(model_id="scribe_v1", keyterms=KEYTERMS)


def test_speech_to_text_keyterms_are_repeated_form_fields():
    """The exact reproduction from #819: keyterms must not be one JSON-array field."""
    request = _capture_sync(_stt_convert)
    assert _values(request, "keyterms") == KEYTERMS


def test_speech_to_text_keyterms_are_not_json_encoded():
    """A single field holding ``'["hello world", "ElevenLabs"]'`` is the bug."""
    request = _capture_sync(_stt_convert)
    assert json.dumps(KEYTERMS) not in [value for _, value in _form_fields(request)]


async def test_speech_to_text_keyterms_are_repeated_form_fields_async():
    request = await _capture_async(_stt_convert_async)
    assert _values(request, "keyterms") == KEYTERMS


def test_speech_to_text_object_fields_stay_json_encoded():
    """Only lists of primitives changed; object fields are still JSON blobs."""
    request = _capture_sync(
        lambda client: client.speech_to_text.convert(
            model_id="scribe_v1",
            keyterms=KEYTERMS,
            entity_detection={"entity_types": ["person"]},
        )
    )
    assert _values(request, "entity_detection") == [json.dumps({"entity_types": ["person"]})]


def test_dubbing_project_keyterms_are_repeated_form_fields():
    request = _capture_sync(
        lambda client: client.dubbing.project.create(source_url="https://e.com/a.mp4", keyterms=KEYTERMS)
    )
    assert _values(request, "keyterms") == KEYTERMS


def test_music_video_to_music_tags_are_repeated_form_fields():
    def call(client: ElevenLabs) -> typing.Any:
        with client.music.with_raw_response.video_to_music(videos=[("clip.mp4", b"video")], tags=TAGS):
            pass

    request = _capture_sync(call)
    assert _values(request, "tags") == TAGS


def test_music_finetunes_tags_are_repeated_form_fields():
    request = _capture_sync(
        lambda client: client.music.finetunes.create(name="My finetune", primary_genre="rock", tags=TAGS)
    )
    assert _values(request, "tags") == TAGS


def test_studio_projects_list_fields_are_repeated_form_fields():
    request = _capture_sync(
        lambda client: client.studio.projects.create(
            name="My project",
            genres=GENRES,
            pronunciation_dictionary_locators=LOCATORS,
            voice_settings=['{"stability": 0.5}'],
        )
    )
    assert _values(request, "genres") == GENRES
    assert _values(request, "pronunciation_dictionary_locators") == LOCATORS
    assert _values(request, "voice_settings") == ['{"stability": 0.5}']


def test_audio_native_pronunciation_dictionary_locators_are_repeated_form_fields():
    request = _capture_sync(
        lambda client: client.audio_native.create(name="My project", pronunciation_dictionary_locators=LOCATORS)
    )
    assert _values(request, "pronunciation_dictionary_locators") == LOCATORS
