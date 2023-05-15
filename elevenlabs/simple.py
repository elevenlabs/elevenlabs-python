import os
import re
from typing import Iterator, List, Optional, Union

from .api import TTS, Model, Voice, VoiceClone, Voices, VoiceSettings


def set_api_key(api_key: str) -> None:
    os.environ["ELEVEN_API_KEY"] = api_key


def get_api_key() -> Optional[str]:
    return os.environ.get("ELEVEN_API_KEY")


# Save default voices to avoid querying the API for unathorized users
VOICES_CACHE = [
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


def voices(api_key: Optional[str] = None) -> List[Voice]:
    """Lists all voices in the API, if authenticated for the current user"""
    if api_key:
        set_api_key(api_key)
    api_key = get_api_key()
    global VOICES_CACHE
    VOICES_CACHE = Voices.from_api() if api_key else VOICES_CACHE
    return VOICES_CACHE


def clone(**kwargs) -> Voice:
    return Voice.from_clone(VoiceClone(**kwargs))


def is_voice_id(val: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9]{20}$", val))


def generate(
    text: str,
    api_key: Optional[str] = None,
    voice: Union[str, Voice] = VOICES_CACHE[2],  # Bella
    model: Union[str, Model] = "eleven_monolingual_v1",
    stream: bool = False,
    stream_chunk_size: int = 2048,
) -> Union[bytes, Iterator[bytes]]:
    if api_key:
        set_api_key(api_key)

    if isinstance(voice, str):
        voice_str = voice
        # If voice is valid voice_id, use it
        if is_voice_id(voice):
            voice = Voice(voice_id=voice)
        # Otherwise, search voice by name
        else:
            # Check if voice is in cache
            voice = next((v for v in VOICES_CACHE if v.name == voice), None)  # type: ignore # noqa E501
            # If not, query API
            voice = next((v for v in voices() if v.name == voice), None) if not voice else voice  # type: ignore # noqa E501
        # Raise error if voice not found
        if not voice:
            raise ValueError(f"Voice '{voice_str}' not found.")

    if isinstance(model, str):
        model = Model(model_id=model)

    assert isinstance(voice, Voice)
    assert isinstance(model, Model)

    if stream:
        return TTS.generate_stream(text, voice, model, stream_chunk_size)
    else:
        return TTS.generate(text, voice, model)
