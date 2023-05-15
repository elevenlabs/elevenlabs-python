from __future__ import annotations

from typing import Iterator, Optional

from .base import API, api_base_url_v1
from .model import Model
from .voice import Voice


class TTS(API):
    @staticmethod
    def generate(
        text: str, voice: Voice, model: Model, api_key: Optional[str] = None
    ) -> bytes:
        url = f"{api_base_url_v1}/text-to-speech/{voice.voice_id}"
        data = dict(
            text=text,
            model_id=model.model_id,
            voice_settings=voice.settings.dict() if voice.settings else None,
        )  # type: ignore
        response = API.post(url, json=data, api_key=api_key)
        return response.content

    @staticmethod
    def generate_stream(
        text: str,
        voice: Voice,
        model: Model,
        stream_chunk_size: int = 2048,
        api_key: Optional[str] = None,
    ) -> Iterator[bytes]:
        url = f"{api_base_url_v1}/text-to-speech/{voice.voice_id}/stream"
        data = dict(
            text=text,
            model_id=model.model_id,
            voice_settings=voice.settings.dict() if voice.settings else None,
        )  # type: ignore
        response = API.post(url, json=data, stream=True, api_key=api_key)
        for chunk in response.iter_content(chunk_size=stream_chunk_size):
            if chunk:
                yield chunk
