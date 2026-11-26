"""URL streaming releases the socket when its audio process cannot start."""

from unittest.mock import AsyncMock, patch

import pytest

from elevenlabs.realtime.scribe import ScribeRealtime


@pytest.mark.asyncio
@pytest.mark.parametrize("error", [PermissionError("permission denied"), OSError("process limit")])
async def test_url_connect_closes_websocket_when_ffmpeg_cannot_start(error):
    websocket = AsyncMock()
    with patch("elevenlabs.realtime.scribe.websocket_connect", new_callable=AsyncMock, return_value=websocket), patch(
        "elevenlabs.realtime.scribe.subprocess.Popen", side_effect=error
    ):
        with pytest.raises(OSError) as caught:
            await ScribeRealtime(api_key="test").connect(
                {"model_id": "scribe_v2_realtime", "url": "https://example.org/audio.mp3"}
            )
    assert caught.value is error
    websocket.close.assert_awaited_once_with(1011, "ffmpeg failed to start")


@pytest.mark.asyncio
async def test_missing_ffmpeg_keeps_installation_error_and_closes_socket():
    websocket = AsyncMock()
    with patch("elevenlabs.realtime.scribe.websocket_connect", new_callable=AsyncMock, return_value=websocket), patch(
        "elevenlabs.realtime.scribe.subprocess.Popen", side_effect=FileNotFoundError()
    ):
        with pytest.raises(RuntimeError, match="ffmpeg is required"):
            await ScribeRealtime(api_key="test").connect(
                {"model_id": "scribe_v2_realtime", "url": "https://example.org/audio.mp3"}
            )
    websocket.close.assert_awaited_once_with(1011, "ffmpeg not found")
