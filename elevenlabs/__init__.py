import os
import wave
from collections.abc import Iterator
from typing import List, Optional, Union

from .api import TTS, Voice, VoiceClone, Voices, VoiceSettings
from .utils import *  # noqa F403


def set_api_key(api_key: str) -> None:
    os.environ["ELEVEN_API_KEY"] = api_key


def get_api_key() -> Optional[str]:
    return os.environ.get("ELEVEN_API_KEY")


# Save default voices to avoid querying the API for unathorized users
DEFAULT_VOICES = [
    Voice(
        voice_id="21m00Tcm4TlvDq8ikWAM",
        name="Rachel",
        category="premade",
        settings=VoiceSettings(stability=0.75, similarity_boost=0.75),
    ),
    Voice(
        voice_id="AZnzlk1XvdvUeBnXmlld",
        name="Domi",
        category="premade",
        settings=VoiceSettings(stability=0.1, similarity_boost=0.75),
    ),
    Voice(
        voice_id="EXAVITQu4vr4xnSDxMaL",
        name="Bella",
        category="premade",
        settings=VoiceSettings(stability=0.245, similarity_boost=0.75),
    ),
    Voice(
        voice_id="ErXwobaYiN019PkySvjV",
        name="Antoni",
        category="premade",
        settings=VoiceSettings(stability=0.195, similarity_boost=0.75),
    ),
    Voice(
        voice_id="MF3mGyEYCl7XYWbV9V6O",
        name="Elli",
        category="premade",
        settings=VoiceSettings(stability=0.755, similarity_boost=0.75),
    ),
    Voice(
        voice_id="TxGEqnHWrfWFTfGW9XjX",
        name="Josh",
        category="premade",
        settings=VoiceSettings(stability=0.15, similarity_boost=0.51),
    ),
    Voice(
        voice_id="VR6AewLTigWG4xSOukaG",
        name="Arnold",
        category="premade",
        settings=VoiceSettings(stability=0.15, similarity_boost=0.75),
    ),
    Voice(
        voice_id="pNInz6obpgDQGcFmaJgB",
        name="Adam",
        category="premade",
        settings=VoiceSettings(stability=0.2, similarity_boost=0.75),
    ),
    Voice(
        voice_id="yoZ06aMxZJJ28mfd3POQ",
        name="Sam",
        category="premade",
        settings=VoiceSettings(stability=0.25, similarity_boost=0.75),
    ),
]


def get_all_voices(api_key: Optional[str] = None) -> List[Voice]:
    if api_key:
        set_api_key(api_key)
    api_key = get_api_key()
    return Voices.from_api() if api_key else DEFAULT_VOICES


def clone(**kwargs) -> Voice:
    return Voice.from_clone(VoiceClone(**kwargs))


def generate(
    text: str,
    api_key: Optional[str] = None,
    voice: Union[str, Voice] = DEFAULT_VOICES[2],  # Bella
    stream: bool = False,
    stream_chunk_size: int = 2048,
) -> Union[bytes, Iterator[bytes]]:
    if api_key:
        set_api_key(api_key)

    # Find first voice with matching name or id if string provided
    if isinstance(voice, str):
        voice_str = voice
        voice = next((v for v in get_all_voices() if v.name == voice or v.voice_id == voice), None)  # type: ignore # noqa E501
        if not voice:
            raise ValueError(f"Voice '{voice_str}' not found.")

    assert isinstance(voice, Voice)

    if stream:
        return TTS.generate_stream(text, voice, stream_chunk_size)
    else:
        return TTS.generate(text, voice)
