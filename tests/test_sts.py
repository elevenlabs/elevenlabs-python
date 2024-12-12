from elevenlabs import play
from elevenlabs.client import ElevenLabs

from .utils import IN_GITHUB, DEFAULT_VOICE, DEFAULT_VOICE_FILE


def test_sts() -> None:
    """Test basic speech-to-speech generation."""
    client = ElevenLabs()
    audio_file = open(DEFAULT_VOICE_FILE, "rb")
    try:
        audio_stream = client.speech_to_speech.convert(voice_id=DEFAULT_VOICE, audio=audio_file)
        audio = b"".join(chunk for chunk in audio_stream)
        assert isinstance(audio, bytes), "Combined audio should be bytes"
        if not IN_GITHUB:
            play(audio)
    finally:
        audio_file.close()


def test_sts_as_stream():
    client = ElevenLabs()
    audio_file = open(DEFAULT_VOICE_FILE, "rb")
    try:
        audio_stream = client.speech_to_speech.convert_as_stream(voice_id=DEFAULT_VOICE, audio=audio_file)
        audio = b"".join(chunk for chunk in audio_stream)
        assert isinstance(audio, bytes), "Combined audio should be bytes"
        if not IN_GITHUB:
            play(audio)
    finally:
        audio_file.close()
