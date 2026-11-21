import sys
import types
import pytest

from elevenlabs.conversational_ai.default_audio_interface import (
    AsyncDefaultAudioInterface,
    DefaultAudioInterface,
)


def _install_fake_pyaudio(monkeypatch):
    opened = []

    class FakeStream:
        def stop_stream(self):
            pass

        def close(self):
            pass

        def write(self, data):
            pass

    class FakePyAudio:
        def open(self, **kwargs):
            opened.append(kwargs)
            return FakeStream()

        def terminate(self):
            pass

    fake_mod = types.SimpleNamespace(PyAudio=FakePyAudio, paInt16=8, paContinue=0)
    monkeypatch.setitem(sys.modules, "pyaudio", fake_mod)
    return opened


def test_default_audio_interface_configurable_chunk_duration(monkeypatch):
    opened = _install_fake_pyaudio(monkeypatch)
    iface = DefaultAudioInterface(input_chunk_duration_ms=50)
    iface.start(lambda _data: None)
    iface.stop()
    in_stream = next(c for c in opened if c.get("input"))
    assert in_stream["frames_per_buffer"] == 800


@pytest.mark.asyncio
async def test_async_default_audio_interface_configurable_chunk_duration(monkeypatch):
    opened = _install_fake_pyaudio(monkeypatch)
    iface = AsyncDefaultAudioInterface(input_chunk_duration_ms=50)

    async def _cb(_data: bytes) -> None:
        pass

    await iface.start(_cb)
    await iface.stop()
    in_stream = next(c for c in opened if c.get("input"))
    assert in_stream["frames_per_buffer"] == 800


def test_default_audio_interface_preserves_subclass_override_and_validates(monkeypatch):
    opened = _install_fake_pyaudio(monkeypatch)

    class CustomDefaultAudioInterface(DefaultAudioInterface):
        INPUT_FRAMES_PER_BUFFER = 1600

    iface = CustomDefaultAudioInterface()
    iface.start(lambda _data: None)
    iface.stop()
    in_stream = next(c for c in opened if c.get("input"))
    assert in_stream["frames_per_buffer"] == 1600

    for bad in (0, -50, False):
        with pytest.raises(ValueError):
            DefaultAudioInterface(input_chunk_duration_ms=bad)
        with pytest.raises(ValueError):
            AsyncDefaultAudioInterface(input_chunk_duration_ms=bad)
