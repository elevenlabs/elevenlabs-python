import base64
import json
from unittest.mock import MagicMock, patch

from elevenlabs.realtime_tts import RealtimeTextToSpeechClient


def test_convert_realtime_stops_after_final_message():
    audio = b"final audio"
    socket = MagicMock()
    socket.__enter__.return_value = socket
    socket.recv.side_effect = [
        json.dumps(
            {
                "audio": base64.b64encode(audio).decode(),
                "isFinal": True,
            }
        ),
        AssertionError("convert_realtime read past the final message"),
    ]

    client = object.__new__(RealtimeTextToSpeechClient)
    client._client_wrapper = MagicMock()
    client._client_wrapper.get_headers.return_value = {}
    client._ws_base_url = "wss://api.elevenlabs.io"

    with patch("elevenlabs.realtime_tts.connect", return_value=socket):
        result = list(
            client.convert_realtime(
                "voice-id",
                text=iter(()),
                model_id="eleven_flash_v2_5",
                voice_settings=None,
            )
        )

    assert result == [audio]
    assert socket.recv.call_count == 1
