"""convert_realtime must not leak the OMIT sentinel into the URL or the first frame."""

import base64
import json
from unittest.mock import MagicMock, patch

from elevenlabs.realtime_tts import RealtimeTextToSpeechClient
from elevenlabs.types.voice_settings import VoiceSettings

AUDIO = b"audio chunk"


def _run(**kwargs):
    """Drive convert_realtime to its first yield, returning the URL, the frames sent, and that chunk."""
    captured = {}
    socket = MagicMock()
    socket.__enter__.return_value = socket
    socket.recv.return_value = json.dumps({"audio": base64.b64encode(AUDIO).decode()})

    def connect(url, **_):
        captured["url"] = url
        return socket

    client = object.__new__(RealtimeTextToSpeechClient)
    client._client_wrapper = MagicMock()
    client._client_wrapper.get_headers.return_value = {}
    client._ws_base_url = "wss://api.elevenlabs.io"

    with patch("elevenlabs.realtime_tts.connect", connect):
        stream = client.convert_realtime("VOICE", text=iter(["hello there."]), **kwargs)
        chunk = next(stream)
        stream.close()

    frames = [json.loads(call.args[0]) for call in socket.send.call_args_list]
    return captured["url"], frames, chunk


def test_omitted_model_id_is_not_sent():
    url, _, chunk = _run()
    assert "model_id" not in url, "OMIT sentinel leaked into the URL: {}".format(url)
    assert chunk == AUDIO


def test_omitted_voice_settings_serialize_to_null():
    _, frames, _ = _run()
    assert frames[0]["voice_settings"] is None


def test_explicit_model_id_is_sent():
    url, _, _ = _run(model_id="eleven_flash_v2_5")
    assert "model_id=eleven_flash_v2_5" in url


def test_explicit_voice_settings_are_sent():
    _, frames, _ = _run(voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75))
    assert frames[0]["voice_settings"]["stability"] == 0.5


def test_output_format_still_sent():
    url, _, _ = _run()
    assert "output_format=mp3_44100_128" in url


def test_omitted_model_id_with_explicit_voice_settings():
    """The URL defect on its own: voice_settings supplied, so nothing else fails first."""
    url, _, _ = _run(voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75))
    assert "model_id" not in url, "OMIT sentinel leaked into the URL: {}".format(url)
