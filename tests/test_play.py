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


def test_play_joins_a_list_of_chunks(monkeypatch):
    received = _fake_ffplay(monkeypatch, exit_code=0)

    play_module.play([b"audio ", b"bytes"])

    assert received["args"][0] == "ffplay"


def test_save_joins_a_list_of_chunks(tmp_path):
    target = tmp_path / "out.mp3"

    play_module.save([b"audio ", b"bytes"], str(target))

    assert target.read_bytes() == b"audio bytes"


def test_save_writes_bytes_unchanged(tmp_path):
    target = tmp_path / "out.mp3"

    play_module.save(b"audio bytes", str(target))

    assert target.read_bytes() == b"audio bytes"


@pytest.mark.parametrize("error", [RuntimeError("audio source failed"), KeyboardInterrupt()])
def test_stream_reaps_player_when_audio_source_raises(monkeypatch, error):
    processes = []
    real_popen = subprocess.Popen

    def player(args, **kwargs):
        process = real_popen(
            [sys.executable, "-c", "import sys; sys.stdin.buffer.read()"], **kwargs
        )
        processes.append(process)
        return process

    monkeypatch.setattr(play_module, "is_installed", lambda name: True)
    monkeypatch.setattr(play_module.subprocess, "Popen", player)

    def audio():
        yield b"audio"
        raise error

    try:
        with pytest.raises(type(error)) as caught:
            play_module.stream(audio())
        assert caught.value is error
        assert processes[0].poll() is not None
        assert processes[0].stdin.closed
    finally:
        for process in processes:
            process.kill()
            process.communicate()


@pytest.mark.parametrize("chunks", [[], [b"first", None, b"second"]])
def test_stream_finishes_player_after_success(monkeypatch, tmp_path, chunks):
    target = tmp_path / "played.raw"
    processes = []
    real_popen = subprocess.Popen

    def player(args, **kwargs):
        script = "import pathlib, sys; pathlib.Path(sys.argv[1]).write_bytes(sys.stdin.buffer.read())"
        process = real_popen([sys.executable, "-c", script, str(target)], **kwargs)
        processes.append(process)
        return process

    monkeypatch.setattr(play_module, "is_installed", lambda name: True)
    monkeypatch.setattr(play_module.subprocess, "Popen", player)
    expected = b"".join(chunk for chunk in chunks if chunk is not None)

    assert play_module.stream(iter(chunks)) == expected
    assert target.read_bytes() == expected
    assert processes[0].returncode == 0


def test_stream_closes_pipe_when_player_exits_before_audio(monkeypatch):
    processes = []
    real_popen = subprocess.Popen

    def player(args, **kwargs):
        process = real_popen([sys.executable, "-c", "pass"], **kwargs)
        processes.append(process)
        return process

    monkeypatch.setattr(play_module, "is_installed", lambda name: True)
    monkeypatch.setattr(play_module.subprocess, "Popen", player)

    def audio():
        processes[0].wait(timeout=5)
        yield b"audio"

    try:
        with pytest.raises(BrokenPipeError):
            play_module.stream(audio())
        assert processes[0].stdin.closed
    finally:
        for process in processes:
            process.kill()
            process.communicate()
