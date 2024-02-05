from __future__ import annotations

import base64
import json
import os
from typing import Iterator, Optional

import websockets
from websockets.sync.client import connect

from .client import ElevenLabs
from .voice import Voice
from .types import Model
from .core.remove_none_from_dict import remove_none_from_dict
from .core.api_error import ApiError


def text_chunker(chunks: Iterator[str]) -> Iterator[str]:
    """Used during input streaming to chunk text blocks and set last char to space"""
    splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]", "}", " ")
    buffer = ""
    for text in chunks:
        if buffer.endswith(splitters):
            yield buffer if buffer.endswith(" ") else buffer + " "
            buffer = text
        elif text.startswith(splitters):
            output = buffer + text[0]
            yield output if output.endswith(" ") else output + " "
            buffer = text[1:]
        else:
            buffer += text
    if buffer != "":
        yield buffer + " "


class TTS():
    @staticmethod
    def generate(
        text: str,
        voice: Voice,
        model: Model,
        api_key: Optional[str] = None,
        output_format: Optional[str] = "mp3_44100_128",
        latency: int = 1,
    ) -> bytes:
        client = ElevenLabs(api_key=api_key)
        response = client.text_to_speech.convert(
            voice.voice_id,
            text=text,
            model_id=model.model_id,
            voice_settings=voice.settings,
            optimize_streaming_latency=latency,
            output_format=output_format)
        return bytes(b"".join(response))

    @staticmethod
    def generate_stream(
        text: str,
        voice: Voice,
        model: Model,
        stream_chunk_size: int = 2048,
        api_key: Optional[str] = None,
        output_format: Optional[str] = "mp3_44100_128",
        latency: int = 1,
    ) -> Iterator[bytes]:
        client = ElevenLabs(api_key=api_key)
        return client.text_to_speech.convert_as_stream(
            voice.voice_id,
            optimize_streaming_latency=latency,
            text=text,
            model_id=model.model_id,
            output_format=output_format,
            voice_settings=voice.settings)

    @staticmethod
    def generate_stream_input(
        text: Iterator[str], voice: Voice, model: Model, api_key: Optional[str] = None
    ) -> Iterator[bytes]:
        BOS = json.dumps(
            dict(
                text=" ",
                try_trigger_generation=True,
                voice_settings=voice.settings.dict() if voice.settings else None,
                generation_config=dict(
                    chunk_length_schedule=[50],
                ),
            )
        )
        EOS = json.dumps(dict(text=""))
        with connect(
            f"wss://api.elevenlabs.io/v1/text-to-speech/{voice.voice_id}/stream-input?model_id={model.model_id}",
            additional_headers=remove_none_from_dict({
                "xi-api-key": api_key or os.environ.get("ELEVEN_API_KEY")
            })
        ) as websocket: 
            # Send beginning of stream
            websocket.send(BOS)

            # Stream text chunks and receive audio
            for text_chunk in text_chunker(text):
                data = dict(text=text_chunk, try_trigger_generation=True)
                websocket.send(json.dumps(data))
                try:
                    data = json.loads(websocket.recv(1e-4))
                    if "audio" in data and data["audio"]:
                        yield base64.b64decode(data["audio"])  # type: ignore
                except TimeoutError:
                    pass

            # Send end of stream
            websocket.send(EOS)

            # Receive remaining audio
            while True:
                try:
                    data = json.loads(websocket.recv())                   
                    if "audio" in data and data["audio"]:
                        yield base64.b64decode(data["audio"])  # type: ignore
                except websockets.exceptions.ConnectionClosed:
                    if "message" in data:
                        raise ApiError(body=data)
                    break
