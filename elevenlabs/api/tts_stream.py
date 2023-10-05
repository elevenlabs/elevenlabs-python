"""
https://docs.elevenlabs.io/api-reference/text-to-speech-websockets
"""
import asyncio
import base64
import json
import os
from typing import Optional, AsyncGenerator, Callable, Coroutine, Any

import websockets


class TTSStream:
    DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # "Rachel"

    def __init__(self, *,
                 voice_id: Optional[str] = None,
                 model: str = 'eleven_monolingual_v1',
                 output_format: str = 'mp3_44100',
                 optimize_streaming_latency: int = 0,
                 output_audio_stream_callback: Optional[
                     Callable[[AsyncGenerator[bytes, Any], ..., ], Coroutine]] = None,
                 output_stream_callback: Optional[
                     Callable[[AsyncGenerator[dict, Any], ...], Coroutine]] = None,
                 other_callback_arguments: Optional[dict] = None,
                 eleven_api_key: Optional[str] = None,

                 ):
        """
        :param voice_id: https://api.elevenlabs.io/v1/voices
        :param model: 'eleven_monolingual_v1' (only EN), 'eleven_monolingual_v2'
         https://elevenlabs.io/blog/multilingualv2/'
        :param output_format: 'mp3_44100', 'pcm_16000', 'pcm_22050', 'pcm_24000'
        :param optimize_streaming_latency: numbers from 0 (no latency optimizations)
         to 4 (max latency optimizations)
        :param output_audio_stream_callback: tts stream returned bytes audio chunks
        :param output_stream_callback: tts stream returned AudioStreamData
        :param other_callback_arguments: dict with args for callback
        :param eleven_api_key: https://docs.elevenlabs.io/api-reference/quick-start/authentication
        """
        self._model = model
        self._output_format = output_format
        self._optimize_streaming_latency = str(optimize_streaming_latency)
        self._eleven_api_key = eleven_api_key if eleven_api_key else os.getenv('ELEVEN_API_KEY')
        voice_id = voice_id if voice_id else TTSStream.DEFAULT_VOICE_ID
        self._voice_id = voice_id

        if not self._eleven_api_key:
            raise ValueError(
                'eleven_api_key must be set explicitly or via the "ELEVEN_API_KEY" '
                'environment variable!')

        if not (output_stream_callback or output_audio_stream_callback):
            raise NotImplementedError(
                'One of handlers output_stream_callback or output_audio_stream_callback '
                'must be defined!')

        if output_stream_callback and output_audio_stream_callback:
            raise ValueError(
                'Only one of handlers output_stream_callback or output_audio_stream_callback '
                'must be defined!')

        self._output_audio_stream_callback = output_audio_stream_callback
        self._output_stream_callback = output_stream_callback
        self._other_callback_args = other_callback_arguments if other_callback_arguments else {}

        self._text_buffer = ''

    async def __aenter__(self):
        ws_url = (f'wss://api.elevenlabs.io/v1/text-to-speech/{self._voice_id}/stream-input?'
                  f'model_id={self._model}&optimize_streaming_latency='
                  f'{self._optimize_streaming_latency}&output_format={self._output_format}')

        self._ws = await websockets.connect(ws_url)

        # Begin of stream
        await self._ws.send(json.dumps({
            "text": " ",
            "voice_settings": {"stability": 0.5, "similarity_boost": True},
            "xi_api_key": self._eleven_api_key,
        }))

        await self._listen()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._text_buffer:
            await self._ws.send(
                json.dumps(
                    {"text": self._text_buffer + " ", "try_trigger_generation": True}))

        await self._ws.send(json.dumps({"text": ""}))
        await self._listen_task
        await self._ws.close()

    async def send_text(self, text: str):
        splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]", "}", " ")

        if self._text_buffer.endswith(splitters):
            await self._ws.send(
                json.dumps({"text": self._text_buffer + " ", "try_trigger_generation": True}))
            self._text_buffer = text
        elif text.startswith(splitters):
            await self._ws.send(
                json.dumps(
                    {"text": self._text_buffer + text[0] + " ", "try_trigger_generation": True}))
            self._text_buffer = text[1:]
        else:
            self._text_buffer += text

    async def _listen(self):
        if self._output_audio_stream_callback:
            self._listen_task = asyncio.create_task(
                self._output_audio_stream_callback(self._listen_audio_stream(),
                                                   **self._other_callback_args))
        else:
            self._listen_task = asyncio.create_task(
                self._output_stream_callback(self._listen_stream(),
                                             **self._other_callback_args))

    async def _listen_audio_stream(self) -> AsyncGenerator[bytes, Any]:
        while True:
            try:
                message = await self._ws.recv()
                data = json.loads(message)
                if data.get("audio"):
                    yield base64.b64decode(data["audio"])
                elif data.get('isFinal'):
                    break
            except websockets.ConnectionClosed:
                print("Connection closed")
                break

    async def _listen_stream(self) -> AsyncGenerator[dict, Any]:
        """tts stream dict {'audio': str, 'isFinal': optional[bool], 'normalizedAlignment':
         dict {'chars': List[str], charStartTimesMs': List[int], 'charDurationsMs': List[int]}}"""
        while True:
            try:
                message = await self._ws.recv()
                data = json.loads(message)
                if data.get("audio"):
                    yield data
                elif data.get('isFinal'):
                    break
            except websockets.ConnectionClosed:
                print("Connection closed")
                break
