import re
import os

from typing import Iterator, Optional, Union

from .tts import TTS
from .types import VoiceSettings, Model
from .voice import Voice, voices


DEFAULT_VOICE = Voice(
    voice_id="EXAVITQu4vr4xnSDxMaL",
    name="Bella",
    settings=VoiceSettings(
        stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True
    ),
)


def is_voice_id(val: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9]{20}$", val))


def generate(
    text: Union[str, Iterator[str]],
    api_key: Optional[str] = os.getenv("ELEVEN_API_KEY"),
    voice: Union[str, Voice] = DEFAULT_VOICE,
    model: Union[str, Model] = "eleven_monolingual_v1",
    stream: bool = False,
    latency: int = 1,
    stream_chunk_size: int = 2048,
    output_format: Optional[str] = "mp3_44100_128",
) -> Union[bytes, Iterator[bytes]]:

    if isinstance(voice, str):
        voice_str = voice
        # If voice is valid voice_id, use it
        if is_voice_id(voice):
            voice = Voice(voice_id=voice)
        else:
            voice = next((v for v in voices() if v.name == voice_str), None)  # type: ignore # noqa E501

        # Raise error if voice not found
        if not voice:
            raise ValueError(f"Voice '{voice_str}' not found.")

    if isinstance(model, str):
        model = Model(model_id=model) # type: ignore

    if stream:
        if isinstance(text, str):
            return TTS.generate_stream(text, voice, model, stream_chunk_size, api_key=api_key, latency=latency, output_format=output_format)  # type: ignore
        elif isinstance(text, Iterator):
            return TTS.generate_stream_input(text, voice, model, api_key=api_key)  # type: ignore
    else:
        assert isinstance(text, str)
        return TTS.generate(text, voice, model, api_key=api_key)  # type: ignore
