import asyncio

from elevenlabs import VoiceSettings, play, Voice
from elevenlabs.client import AsyncElevenLabs, ElevenLabs

from .utils import IN_GITHUB, DEFAULT_TEXT, DEFAULT_VOICE, DEFAULT_MODEL
import base64


def test_tts_convert() -> None:
    """Test basic text-to-speech generation."""
    client = ElevenLabs()
    audio_generator = client.text_to_speech.convert(text=DEFAULT_TEXT, voice_id=DEFAULT_VOICE, model_id=DEFAULT_MODEL)
    audio = b"".join(audio_generator)
    assert isinstance(audio, bytes), "TTS should return bytes"
    if not IN_GITHUB:
        play(audio)


def test_tts_generate() -> None:
    """Test basic text-to-speech generation w/ custom generate."""
    client = ElevenLabs()
    audio_generator = client.generate(text=DEFAULT_TEXT, voice="Brian", model=DEFAULT_MODEL)
    audio = b"".join(audio_generator)
    assert isinstance(audio, bytes), "TTS should return bytes"
    if not IN_GITHUB:
        play(audio)


def test_tts_generate_with_voice_settings() -> None:
    """Test basic text-to-speech generation."""
    client = ElevenLabs()
    audio_generator = client.generate(
        text=DEFAULT_TEXT,
        model=DEFAULT_MODEL,
        voice=Voice(
            voice_id="nPczCjzI2devNBz1zQrb",
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True),
        ),
    )
    audio = b"".join(audio_generator)
    assert isinstance(audio, bytes), "TTS should return bytes"
    if not IN_GITHUB:
        play(audio)


def test_tts_convert_with_voice_settings() -> None:
    """Test TTS with custom voice settings."""
    client = ElevenLabs()
    audio_generator = client.text_to_speech.convert(
        text=DEFAULT_TEXT,
        voice_id=DEFAULT_VOICE,
        model_id=DEFAULT_MODEL,
        voice_settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True),
    )
    audio = b"".join(audio_generator)
    assert isinstance(audio, bytes), "TTS with voice settings should return bytes"
    if not IN_GITHUB:
        play(audio)


def test_tts_convert_as_stream():
    async def main():
        async_client = AsyncElevenLabs()
        results = async_client.text_to_speech.convert_as_stream(
            text=DEFAULT_TEXT, voice_id=DEFAULT_VOICE, model_id=DEFAULT_MODEL
        )
        out = b""
        async for value in results:
            assert isinstance(value, bytes), "Stream chunks should be bytes"
            out += value
        if not IN_GITHUB:
            play(out)

    asyncio.run(main())


def test_tts_convert_with_timestamps() -> None:
    """Test TTS generation with timestamps."""
    client = ElevenLabs()
    result = client.text_to_speech.convert_with_timestamps(
        text=DEFAULT_TEXT, voice_id=DEFAULT_VOICE, model_id=DEFAULT_MODEL
    )

    assert "alignment" in result  # type: ignore
    assert "characters" in result["alignment"]  # type: ignore

    if not IN_GITHUB:
        audio_bytes = base64.b64decode(result["audio_base64"])  # type: ignore
        play(audio_bytes)


def test_tts_stream_with_timestamps():
    async def main():
        async_client = AsyncElevenLabs()
        audio_data = b""
        async_stream = async_client.text_to_speech.stream_with_timestamps(
            voice_id=DEFAULT_VOICE,
            text=DEFAULT_TEXT,
            model_id=DEFAULT_MODEL,
        )
        async for chunk in async_stream:
            if hasattr(chunk, "audio_base_64"):
                audio_bytes = base64.b64decode(chunk.audio_base_64)
                audio_data += audio_bytes

        if not IN_GITHUB:
            play(audio_data)

    asyncio.run(main())
