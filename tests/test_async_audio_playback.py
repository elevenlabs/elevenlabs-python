import asyncio
import sys
import threading
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from elevenlabs.conversational_ai.default_audio_interface import AsyncDefaultAudioInterface


@pytest.mark.asyncio
async def test_event_loop_can_progress_while_audio_device_is_writing(monkeypatch):
    device = MagicMock()
    input_stream = MagicMock()
    output_stream = MagicMock()
    device.open.side_effect = [input_stream, output_stream]
    monkeypatch.setitem(sys.modules, "pyaudio", SimpleNamespace(PyAudio=lambda: device, paInt16=8, paContinue=0))
    interface = AsyncDefaultAudioInterface()
    started = threading.Event()
    release = threading.Event()
    finished = threading.Event()
    loop_progress = threading.Event()
    progress_during_write = []

    def write(_audio):
        started.set()
        try:
            release.wait(timeout=2)
            progress_during_write.append(loop_progress.is_set())
        finally:
            finished.set()

    output_stream.write.side_effect = write
    await interface.start(lambda _: None)
    try:
        await interface.output(b"audio")
        assert await asyncio.get_running_loop().run_in_executor(None, started.wait, 3)
        loop_progress.set()
        release.set()
        assert await asyncio.get_running_loop().run_in_executor(None, finished.wait, 3)
        assert progress_during_write == [True]
        output_stream.write.assert_called_once_with(b"audio")
    finally:
        release.set()
        await interface.stop()
