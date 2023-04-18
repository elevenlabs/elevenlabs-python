import os
import shutil
import subprocess
import wave
from collections.abc import Iterator
from pathlib import Path

from IPython.display import Audio, display


def play(audio: bytes, autoplay: bool = True) -> None:
    display(Audio(audio, rate=44100, autoplay=autoplay))


def save(audio: bytes, filename: str) -> None:
    with wave.open(filename, "w") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(44100)
        f.writeframes(audio)


def is_mpv_installed() -> bool:
    mpv = shutil.which("mpv")
    if mpv is None:
        return False
    global_path = Path(mpv)
    # else check if path is valid and has the correct access rights
    return global_path.exists() and os.access(global_path, os.X_OK)


def stream(audio_stream: Iterator[bytes]) -> None:
    if not is_mpv_installed():
        raise ValueError("mpv not found, necessary to stream audio.")

    mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
    mpv_process = subprocess.Popen(mpv_command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for chunk in audio_stream:
        if chunk is not None:
            mpv_process.stdin.write(chunk)  # type: ignore
            mpv_process.stdin.flush()  # type: ignore

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()
