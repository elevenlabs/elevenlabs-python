import pytest
import os
from unittest.mock import patch, MagicMock
from elevenlabs.client import AsyncElevenLabs, ElevenLabs
from elevenlabs.types.speech_to_text_chunk_response_model import SpeechToTextChunkResponseModel
from elevenlabs.core.api_error import ApiError
import requests
import tempfile
from typing import Union

from .utils import DEFAULT_VOICE_FILE

DEFAULT_EXT_AUDIO = "https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3"

def handle_api_error(e: ApiError) -> None:
    """Handle common API error patterns."""
    if e.status_code == 401:
        pytest.skip("Invalid API key")
    raise e

async def convert_audio_file(
    client: Union[ElevenLabs, AsyncElevenLabs],
    file: Union[str, bytes, os.PathLike],
    model_id: str = "scribe_v1",
    is_async: bool = False
) -> SpeechToTextChunkResponseModel:
    """Helper function to convert audio file to text.
    
    Args:
        client: ElevenLabs client instance
        file: Audio file path or file-like object
        model_id: Model ID to use for conversion
        is_async: Whether to use async conversion
    
    Returns:
        SpeechToTextChunkResponseModel: Transcription response
    """
    try:
        if isinstance(file, (str, os.PathLike)) and not hasattr(file, 'read'):
            with open(file, "rb") as audio_file:
                if is_async:
                    return await client.speech_to_text.convert(
                        file=audio_file,
                        model_id=model_id
                    )
                return client.speech_to_text.convert(
                    file=audio_file,
                    model_id=model_id
                )
        else:
            if is_async:
                return await client.speech_to_text.convert(
                    file=file,
                    model_id=model_id
                )
            return client.speech_to_text.convert(
                file=file,
                model_id=model_id
            )
    except ApiError as e:
        handle_api_error(e)

def download_audio_file(url: str) -> tempfile._TemporaryFileWrapper:
    """Download audio file from URL and return a temporary file.
    
    Args:
        url: URL to download from
    
    Returns:
        tempfile._TemporaryFileWrapper: Temporary file containing downloaded audio
    """
    response = requests.get(url)
    response.raise_for_status()
    
    temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=True)
    temp_file.write(response.content)
    temp_file.flush()
    temp_file.seek(0)
    return temp_file

@pytest.fixture
async def eleven_client():
    """Fixture to provide an ElevenLabs client instance."""
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        pytest.skip("ELEVEN_API_KEY environment variable not set")
    client = ElevenLabs(api_key=api_key)
    yield client

@pytest.fixture
async def async_eleven_client():
    """Fixture to provide an AsyncElevenLabs client instance."""
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        pytest.skip("ELEVEN_API_KEY environment variable not set")
    client = AsyncElevenLabs(api_key=api_key)
    yield client

@pytest.fixture
def mock_response():
    """Fixture to provide a mock response for speech-to-text conversion."""
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        "language_code": "eng",
        "language_probability": 0.9,
        "text": "This is a test transcription",
        "words": [
            {
                "text": "This",
                "start": 0.0,
                "end": 0.2,
                "type": "word"
            },
            {
                "text": "is",
                "start": 0.2,
                "end": 0.3,
                "type": "word"
            },
            {
                "text": "a",
                "start": 0.3,
                "end": 0.4,
                "type": "word"
            },
            {
                "text": "test",
                "start": 0.4,
                "end": 0.6,
                "type": "word"
            },
            {
                "text": "transcription",
                "start": 0.6,
                "end": 0.9,
                "type": "word"
            }
        ]
    }
    return mock

@pytest.fixture
def mock_error_response():
    """Fixture to provide a mock error response."""
    mock = MagicMock()
    mock.status_code = 400
    mock.json.return_value = {"detail": "Invalid file format"}
    return mock

@pytest.mark.asyncio
async def test_stt_convert_local_file(eleven_client):
    """Test speech-to-text conversion with a local audio file."""
    transcription = await convert_audio_file(eleven_client, DEFAULT_VOICE_FILE)
    assert isinstance(transcription, SpeechToTextChunkResponseModel)
    assert transcription.text is not None

@pytest.mark.asyncio
async def test_stt_convert_external_url(eleven_client):
    """Test speech-to-text conversion with an external audio URL."""
    with download_audio_file(DEFAULT_EXT_AUDIO) as temp_file:
        transcription = await convert_audio_file(eleven_client, temp_file)
        assert isinstance(transcription, SpeechToTextChunkResponseModel)
        assert transcription.text is not None

@pytest.mark.asyncio
async def test_async_stt_convert(async_eleven_client):
    """Test async speech-to-text conversion."""
    transcription = await convert_audio_file(async_eleven_client, DEFAULT_VOICE_FILE, is_async=True)
    assert isinstance(transcription, SpeechToTextChunkResponseModel)
    assert transcription.text is not None

@pytest.mark.asyncio
async def test_stt_convert_different_models(eleven_client):
    """Test speech-to-text conversion with different model IDs."""
    model_ids = ["scribe_v1"]  

    for model_id in model_ids:
        transcription = await convert_audio_file(eleven_client, DEFAULT_VOICE_FILE, model_id=model_id)
        assert isinstance(transcription, SpeechToTextChunkResponseModel)
        assert transcription.text is not None

@pytest.mark.asyncio
async def test_stt_convert_invalid_file(eleven_client):
    """Test speech-to-text conversion with invalid file input."""
    with pytest.raises(Exception):  
        await convert_audio_file(eleven_client, "nonexistent_file.mp3")

@pytest.mark.asyncio
async def test_stt_convert_invalid_model(eleven_client):
    """Test speech-to-text conversion with invalid model ID."""
    with pytest.raises(Exception):  
        await convert_audio_file(eleven_client, DEFAULT_VOICE_FILE, model_id="nonexistent_model")

@pytest.mark.asyncio
async def test_stt_convert_local_file_handling(eleven_client):
    """Test speech-to-text conversion with different local file scenarios."""
    transcription = await convert_audio_file(eleven_client, DEFAULT_VOICE_FILE)
    assert isinstance(transcription, SpeechToTextChunkResponseModel)
    assert transcription.text is not None
