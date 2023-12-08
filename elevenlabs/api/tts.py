from __future__ import annotations

import base64
import json
import os
from typing import Iterator, Literal, Optional

import websockets
from websockets.sync.client import connect

from .base import API, api_base_url_v1
from .model import Model
from .voice import Voice


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


class TTS(API):
    OutputFormat = Literal[
        "mp3_44100_64",
        "mp3_44100_96",
        "mp3_44100_128",
        "mp3_44100_192",
        "pcm_16000",
        "pcm_22050",
        "pcm_24000",
        "pcm_44100",
        "ulaw_8000",
    ]

    @staticmethod
    def generate(
        text: str,
        voice: Voice,
        model: Model,
        api_key: Optional[str] = None,
        output_format: TTS.OutputFormat = "mp3_44100_128",
    ) -> bytes:
        url = f"{api_base_url_v1}/text-to-speech/{voice.voice_id}?output_format={output_format}"
        data = dict(
            text=text,
            model_id=model.model_id,
            voice_settings=voice.settings.model_dump() if voice.settings else None,
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
        latency: int = 1,
        output_format: TTS.OutputFormat = "mp3_44100_128",
    ) -> Iterator[bytes]:
        url = f"{api_base_url_v1}/text-to-speech/{voice.voice_id}/stream?optimize_streaming_latency={latency}&output_format={output_format}"
        data = dict(
            text=text,
            model_id=model.model_id,
            voice_settings=voice.settings.model_dump() if voice.settings else None,
        )  # type: ignore
        response = API.post(url, json=data, stream=True, api_key=api_key)
        for chunk in response.iter_content(chunk_size=stream_chunk_size):
            if chunk:
                yield chunk

    @staticmethod
    def generate_stream_input(
        text: Iterator[str],
        voice: Voice,
        model: Model,
        api_key: Optional[str] = None,
        output_format: TTS.OutputFormat = "mp3_44100_128",
    ) -> Iterator[bytes]:
        BOS = json.dumps(
            dict(
                text=" ",
                try_trigger_generation=True,
                voice_settings=voice.settings.model_dump() if voice.settings else None,
                generation_config=dict(
                    chunk_length_schedule=[50],
                ),
            )
        )
        EOS = json.dumps(dict(text=""))

        with connect(
            f"wss://api.elevenlabs.io/v1/text-to-speech/{voice.voice_id}/stream-input?model_id={model.model_id}&output_format={output_format}",
            additional_headers={
                "xi-api-key": api_key or os.environ.get("ELEVEN_API_KEY")
            },
        ) as websocket:
            # Send beginning of stream
            websocket.send(BOS)

            # Stream text chunks and receive audio
            for text_chunk in text_chunker(text):
                data = dict(text=text_chunk, try_trigger_generation=True)
                websocket.send(json.dumps(data))
                try:
                    data = json.loads(websocket.recv(1e-4))
                    if data["audio"]:
                        yield base64.b64decode(data["audio"])  # type: ignore
                except TimeoutError:
                    pass

            # Send end of stream
            websocket.send(EOS)

            # Receive remaining audio
            while True:
                try:
                    data = json.loads(websocket.recv())
                    if data["audio"]:
                        yield base64.b64decode(data["audio"])  # type: ignore
                except websockets.exceptions.ConnectionClosed:
                    break
