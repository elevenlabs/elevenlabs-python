import os
import re
from typing import Iterator, Literal, Optional, Union

from .api import TTS, Model, Voice, VoiceClone, Voices, VoiceSettings

DEFAULT_VOICE = Voice(
    voice_id="EXAVITQu4vr4xnSDxMaL",
    name="Bella",
    settings=VoiceSettings(
        stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True
    ),
)


def set_api_key(api_key: str) -> None:
    os.environ["ELEVEN_API_KEY"] = api_key


def get_api_key() -> Optional[str]:
    return os.environ.get("ELEVEN_API_KEY")


def voices() -> Voices:
    return Voices.from_api()


def clone(**kwargs) -> Voice:
    return Voice.from_clone(VoiceClone(**kwargs))


def is_voice_id(val: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9]{20}$", val))


def generate(
    text: Union[str, Iterator[str]],
    api_key: Optional[str] = None,
    voice: Union[str, Voice] = DEFAULT_VOICE,
    model: Union[str, Model] = "eleven_monolingual_v1",
    stream: bool = False,
    latency: int = 1,
    output_format: TTS.OutputFormat = "mp3_44100_128",
    stream_chunk_size: int = 2048,
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
        model = Model(model_id=model)

    assert isinstance(voice, Voice)
    assert isinstance(model, Model)

    if stream:
        if isinstance(text, str):
            return TTS.generate_stream(
                text, voice, model, stream_chunk_size, api_key=api_key, latency=latency, output_format=output_format
            )  # noqa E501
        elif isinstance(text, Iterator):
            return TTS.generate_stream_input(text, voice, model, api_key=api_key, output_format=output_format)
    else:
        assert isinstance(text, str)
        return TTS.generate(text, voice, model, api_key=api_key, output_format=output_format)
