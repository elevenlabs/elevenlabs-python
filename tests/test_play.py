import subprocess
import sys

import pytest

from elevenlabs import play as play_module


def _fake_ffplay(monkeypatch, exit_code, stderr=""):
    """Run a real subprocess in place of ffplay: it reads the audio from stdin,
    writes ``stderr`` and exits with ``exit_code``."""
    received = {}
    real_popen = subprocess.Popen

    def fake_popen(args, **kwargs):
        received["args"] = args
        script = (
            "import sys; data = sys.stdin.buffer.read(); "
            f"sys.stderr.write({stderr!r}); "
            f"sys.exit({exit_code})"
        )
        return real_popen([sys.executable, "-c", script], **kwargs)

    monkeypatch.setattr(play_module, "is_installed", lambda name: True)
    monkeypatch.setattr(play_module.subprocess, "Popen", fake_popen)
    return received


def test_play_returns_when_ffplay_succeeds(monkeypatch):
    received = _fake_ffplay(monkeypatch, exit_code=0)

    play_module.play(b"audio bytes")

    assert received["args"][0] == "ffplay"


def test_play_raises_when_ffplay_fails(monkeypatch):
    _fake_ffplay(monkeypatch, exit_code=1, stderr="error while loading shared libraries: libavdevice.so.61")

    with pytest.raises(ValueError, match="ffplay exited with status 1") as excinfo:
        play_module.play(b"audio bytes")

    assert "libavdevice.so.61" in str(excinfo.value)


def test_play_raises_without_error_output(monkeypatch):
    _fake_ffplay(monkeypatch, exit_code=2)

    with pytest.raises(ValueError, match=r"ffplay exited with status 2 and did not play the audio\.$"):
        play_module.play(b"audio bytes")


def test_play_joins_an_iterator_before_piping_it(monkeypatch):
    _fake_ffplay(monkeypatch, exit_code=0)

    play_module.play(iter([b"audio ", b"bytes"]))
