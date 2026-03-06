import json

import pytest

from elevenlabs.music_custom import MusicClient, _find_audio_start

SAMPLE_JSON = {"compositionPlan": {"sections": []}, "songMetadata": {"title": "Test"}}
SAMPLE_AUDIO = bytes(range(256)) * 4


def _build_multipart(line_ending: bytes) -> bytes:
    """Build a realistic multipart response with the given line ending."""
    boundary = b"--boundary123"
    nl = line_ending

    parts = []
    parts.append(boundary + nl)
    parts.append(b"Content-Type: application/json" + nl)
    parts.append(nl)
    parts.append(json.dumps(SAMPLE_JSON).encode("utf-8") + nl)
    parts.append(boundary + nl)
    parts.append(b"Content-Type: audio/mpeg" + nl)
    parts.append(b'Content-Disposition: attachment; filename="test_song.mp3"' + nl)
    parts.append(nl)
    parts.append(SAMPLE_AUDIO)
    parts.append(nl + boundary + b"--" + nl)

    return b"".join(parts)


class TestFindAudioStart:
    def test_crlf(self):
        data = b"Header: value\r\n\r\naudio data here"
        assert _find_audio_start(data, 0) == data.index(b"audio")

    def test_lf(self):
        data = b"Header: value\n\naudio data here"
        assert _find_audio_start(data, 0) == data.index(b"audio")

    def test_crlf_preferred_over_lf(self):
        data = b"Header: value\r\n\r\naudio data here"
        pos = _find_audio_start(data, 0)
        assert data[pos : pos + 5] == b"audio"

    def test_raises_when_no_separator(self):
        with pytest.raises(ValueError, match="header/body separator"):
            _find_audio_start(b"no blank line here", 0)

    def test_start_offset_respected(self):
        data = b"skip\n\nHeader: value\r\n\r\naudio"
        pos = _find_audio_start(data, 6)
        assert data[pos : pos + 5] == b"audio"


class TestParseMultipart:
    @staticmethod
    def _parse(data: bytes):
        return MusicClient._parse_multipart(None, iter([data]))  # type: ignore[arg-type]

    def test_crlf_line_endings(self):
        data = _build_multipart(b"\r\n")
        result = self._parse(data)
        assert result.audio.startswith(SAMPLE_AUDIO)
        assert result.json == SAMPLE_JSON
        assert result.filename == "test_song.mp3"

    def test_lf_line_endings(self):
        data = _build_multipart(b"\n")
        result = self._parse(data)
        assert result.audio.startswith(SAMPLE_AUDIO)
        assert result.json == SAMPLE_JSON
        assert result.filename == "test_song.mp3"

    def test_audio_bytes_not_corrupted(self):
        for nl in [b"\r\n", b"\n"]:
            data = _build_multipart(nl)
            result = self._parse(data)
            assert result.audio[:4] == SAMPLE_AUDIO[:4], (
                f"First 4 bytes mismatch with {nl!r} line endings — possible byte offset error"
            )
            assert result.audio[: len(SAMPLE_AUDIO)] == SAMPLE_AUDIO
