from __future__ import annotations

from collections.abc import Iterator

from .base import API, api_base_url_v1
from .voice import Voice


class TTS(API):
    @staticmethod
    def generate(text: str, voice: Voice) -> bytes:
        url = f"{api_base_url_v1}/text-to-speech/{voice.voice_id}"
        data = dict(
            text=text, voice_settings=voice.settings.dict() if voice.settings else None
        )  # type: ignore
        response = API.post(url, json=data)
        return response.content

    @staticmethod
    def generate_stream(
        text: str, voice: Voice, stream_chunk_size: int = 2048
    ) -> Iterator[bytes]:
        url = f"{api_base_url_v1}/text-to-speech/{voice.voice_id}/stream"
        data = dict(
            text=text, voice_settings=voice.settings.dict() if voice.settings else None
        )  # type: ignore
        response = API.post(url, json=data, stream=True)
        for chunk in response.iter_content(chunk_size=stream_chunk_size):
            if chunk:
                yield chunk
