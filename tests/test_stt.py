import pytest
from elevenlabs.client import AsyncElevenLabs, ElevenLabs

from .utils import DEFAULT_VOICE_FILE

DEFAULT_EXT_AUDIO = "https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3"



@pytest.mark.asyncio
async def test_stt_convert():
    """Test basic speech-to-text conversion."""
    client = ElevenLabs()
    
    audio_file = open(DEFAULT_VOICE_FILE, "rb")
    
    transcription = client.speech_to_text.convert(
        file=audio_file,
        model_id="scribe_v1"
    )
    
    assert isinstance(transcription.text, str)
    assert len(transcription.text) > 0
    assert isinstance(transcription.words, list)
    assert len(transcription.words) > 0

@pytest.mark.asyncio
async def test_stt_convert_as_stream():
    """Test speech-to-text conversion as stream."""
    client = AsyncElevenLabs()
    
    audio_file = open(DEFAULT_VOICE_FILE, "rb")
    
    stream = client.speech_to_text.convert_as_stream(
        file=audio_file,
        model_id="scribe_v1"
    )
    
    transcription_text = ""
    async for chunk in stream:
        assert isinstance(chunk.text, str)
        transcription_text += chunk.text
    
    assert len(transcription_text) > 0