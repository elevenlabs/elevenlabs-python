import os
import wave
from collections.abc import Iterator
from typing import Optional, Union

import requests  # type: ignore

from .utils import *  # noqa F403

ELEVEN_API_KEY = os.environ.get("ELEVEN_API_KEY")

DEFAULT_VOICES = dict(
    Rachel="21m00Tcm4TlvDq8ikWAM",
    Domi="AZnzlk1XvdvUeBnXmlld",
    Bella="EXAVITQu4vr4xnSDxMaL",
    Antoni="ErXwobaYiN019PkySvjV",
    Elli="MF3mGyEYCl7XYWbV9V6O",
    Josh="TxGEqnHWrfWFTfGW9XjX",
    Arnold="VR6AewLTigWG4xSOukaG",
    Adam="pNInz6obpgDQGcFmaJgB",
    Sam="yoZ06aMxZJJ28mfd3POQ",
)

TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"


def generate(
    text: str,
    api_key: Optional[str] = ELEVEN_API_KEY,
    voice: str = "Rachel",
    stability: float = 0.3,
    similarity_boost: float = 0.6,
    stream: bool = False,
    stream_chunk_size: int = 2048,
) -> Union[bytes, Iterator[bytes]]:

    voice_id = DEFAULT_VOICES[voice] if voice in DEFAULT_VOICES else voice

    data = dict(
        text=text,
        voice_settings=dict(
            stability=stability,
            similarity_boost=similarity_boost,
        ),
    )

    headers = {
        "Accept": "application/json",
        "xi-api-key": api_key,
    }

    def generate_stream():
        url = f"{TTS_URL}/{voice_id}/stream"
        with requests.post(url, json=data, headers=headers, stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=stream_chunk_size):
                if chunk:
                    yield chunk

    if stream:
        return generate_stream()
    else:
        url = f"{TTS_URL}/{voice_id}"
        with requests.post(url, json=data, headers=headers) as response:
            response.raise_for_status()  # raise exception if status code is not 200
            return response.content
