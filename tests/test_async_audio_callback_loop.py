import asyncio
import sys
import threading
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from elevenlabs.conversational_ai.default_audio_interface import AsyncDefaultAudioInterface


@pytest.mark.asyncio
async def test_microphone_callback_runs_on_starting_event_loop(monkeypatch):
    audio = MagicMock()
    monkeypatch.setitem(
        sys.modules,
        "pyaudio",
        SimpleNamespace(
            PyAudio=lambda: audio,
            paInt16=8,
            paContinue=0,
        ),
    )
    interface = AsyncDefaultAudioInterface()
    received = asyncio.Event()
    callback_loops = []
    chunks = []

    async def on_input(chunk):
        callback_loops.append(asyncio.get_running_loop())
        chunks.append(chunk)
        received.set()

    await interface.start(on_input)
    try:
        callback = audio.open.call_args_list[0].kwargs["stream_callback"]
        thread = threading.Thread(target=callback, args=(b"microphone audio", 8, None, 0))
        thread.start()
        await asyncio.get_running_loop().run_in_executor(None, thread.join)
        await asyncio.wait_for(received.wait(), timeout=1)
        assert chunks == [b"microphone audio"]
        assert callback_loops == [asyncio.get_running_loop()]
    finally:
        await interface.stop()
