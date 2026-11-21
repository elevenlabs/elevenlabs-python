import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface


@pytest.mark.parametrize("failure_on", [1, 2])
def test_startup_failure_releases_acquired_audio_resources(monkeypatch, failure_on):
    device = MagicMock()
    input_stream = MagicMock()
    failure = OSError("audio device unavailable")
    device.open.side_effect = [failure] if failure_on == 1 else [input_stream, failure]
    monkeypatch.setitem(sys.modules, "pyaudio", SimpleNamespace(PyAudio=lambda: device, paInt16=8, paContinue=0))
    interface = DefaultAudioInterface()

    with pytest.raises(OSError, match="audio device unavailable") as caught:
        interface.start(lambda _: None)

    assert caught.value is failure
    device.terminate.assert_called_once_with()
    if failure_on == 2:
        input_stream.close.assert_called_once_with()


def test_successful_start_keeps_audio_resources_until_stop(monkeypatch):
    device = MagicMock()
    input_stream = MagicMock()
    output_stream = MagicMock()
    device.open.side_effect = [input_stream, output_stream]
    monkeypatch.setitem(sys.modules, "pyaudio", SimpleNamespace(PyAudio=lambda: device, paInt16=8, paContinue=0))
    interface = DefaultAudioInterface()
    interface.start(lambda _: None)
    try:
        device.terminate.assert_not_called()
        input_stream.close.assert_not_called()
        output_stream.close.assert_not_called()
    finally:
        interface.stop()
    input_stream.close.assert_called_once_with()
    output_stream.close.assert_called_once_with()
    device.terminate.assert_called_once_with()
