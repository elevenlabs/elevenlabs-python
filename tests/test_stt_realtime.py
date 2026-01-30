"""Tests for realtime speech-to-text (Scribe) functionality.

These tests cover URL building, validation, and event handling behavior
that don't require an actual WebSocket connection.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from elevenlabs.realtime.connection import RealtimeConnection, RealtimeEvents
from elevenlabs.realtime.scribe import (
    AudioFormat,
    CommitStrategy,
    ScribeRealtime,
)


class TestBuildWebsocketUrl:
    """Tests for _build_websocket_url helper method"""

    def setup_method(self):
        """Set up test fixtures"""
        self.scribe = ScribeRealtime(api_key="test-api-key")

    def test_builds_url_with_all_parameters(self):
        """Test URL construction with required and optional parameters"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="vad",
            vad_silence_threshold_secs=0.5,
            vad_threshold=0.3,
            min_speech_duration_ms=100,
            min_silence_duration_ms=200,
            language_code="es",
            include_timestamps=True
        )

        # Base URL structure
        assert url.startswith("wss://api.elevenlabs.io/v1/speech-to-text/realtime?")
        
        # Required parameters
        assert "model_id=scribe_v2_realtime" in url
        assert "audio_format=pcm_16000" in url
        assert "commit_strategy=vad" in url
        
        # Optional parameters
        assert "vad_silence_threshold_secs=0.5" in url
        assert "vad_threshold=0.3" in url
        assert "min_speech_duration_ms=100" in url
        assert "min_silence_duration_ms=200" in url
        assert "language_code=es" in url
        assert "include_timestamps=true" in url

    def test_optional_parameters_omitted_when_none(self):
        """Test that None parameters are not included in URL"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual",
            vad_silence_threshold_secs=None,
            language_code=None
        )

        assert "vad_silence_threshold_secs" not in url
        assert "language_code" not in url

    def test_url_converts_https_to_wss(self):
        """Test that https base URLs are converted to wss"""
        scribe = ScribeRealtime(
            api_key="test-api-key",
            base_url="https://api.elevenlabs.io"
        )
        url = scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual"
        )

        assert url.startswith("wss://")
        assert not url.startswith("wss://wss://")

    def test_url_converts_http_to_ws(self):
        """Test that http base URLs are converted to ws"""
        scribe = ScribeRealtime(
            api_key="test-api-key",
            base_url="http://localhost:8080"
        )
        url = scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual"
        )

        assert url.startswith("ws://localhost:8080")


class TestConnectValidation:
    """Tests for connect method validation"""

    def setup_method(self):
        """Set up test fixtures"""
        self.scribe = ScribeRealtime(api_key="test-api-key")

    @pytest.mark.asyncio
    async def test_connect_requires_model_id(self):
        """Test that connect raises error without model_id"""
        with pytest.raises(ValueError, match="model_id is required"):
            await self.scribe.connect({})  # type: ignore

    @pytest.mark.asyncio
    async def test_connect_audio_mode_requires_format_and_sample_rate(self):
        """Test that audio mode requires both audio_format and sample_rate"""
        with pytest.raises(ValueError, match="audio_format and sample_rate are required"):
            await self.scribe.connect({
                "model_id": "scribe_v2_realtime"
            })  # type: ignore

        with pytest.raises(ValueError, match="audio_format and sample_rate are required"):
            await self.scribe.connect({
                "model_id": "scribe_v2_realtime",
                "audio_format": AudioFormat.PCM_16000
                # missing sample_rate
            })  # type: ignore

        with pytest.raises(ValueError, match="audio_format and sample_rate are required"):
            await self.scribe.connect({
                "model_id": "scribe_v2_realtime",
                "sample_rate": 16000
                # missing audio_format
            })  # type: ignore

    @pytest.mark.asyncio
    @patch("elevenlabs.realtime.scribe.websocket_connect")
    async def test_connect_url_mode_requires_url(self, mock_ws_connect):
        """Test that URL mode requires non-empty url parameter"""
        with pytest.raises(ValueError, match="url is required"):
            await self.scribe.connect({
                "model_id": "scribe_v2_realtime",
                "url": ""
            })  # type: ignore


class TestConnectEnumHandling:
    """Tests for correct enum value extraction when building WebSocket URLs.
    
    Regression tests to ensure AudioFormat and CommitStrategy enums are
    converted to their string values (e.g., 'pcm_16000') rather than being
    passed as enum objects (which would result in 'AudioFormat.PCM_16000').
    """

    def setup_method(self):
        """Set up test fixtures"""
        self.scribe = ScribeRealtime(api_key="test-api-key")

    @pytest.mark.asyncio
    @patch("elevenlabs.realtime.scribe.websocket_connect", new_callable=AsyncMock)
    async def test_connect_audio_uses_enum_values_in_url(self, mock_ws_connect):
        """Test that AudioFormat and CommitStrategy enum values are correctly extracted.
        
        This is a regression test: previously, if .value was not called on enums,
        the URL would contain 'AudioFormat.PCM_16000' instead of 'pcm_16000'.
        """
        mock_websocket = MagicMock()
        mock_ws_connect.return_value = mock_websocket
        # Mock the async iterator for the websocket (needed for message handler)
        mock_websocket.__aiter__ = MagicMock(return_value=iter([]))

        await self.scribe.connect({
            "model_id": "scribe_v2_realtime",
            "audio_format": AudioFormat.PCM_16000,
            "sample_rate": 16000,
            "commit_strategy": CommitStrategy.VAD
        })

        # Verify websocket_connect was called
        mock_ws_connect.assert_awaited_once()
        
        # Extract the URL that was passed to websocket_connect
        call_args = mock_ws_connect.call_args
        url = call_args[0][0]  # First positional argument

        # Verify the URL contains the string values, not enum representations
        assert "audio_format=pcm_16000" in url, \
            f"URL should contain 'audio_format=pcm_16000', not enum repr. Got: {url}"
        assert "AudioFormat" not in url, \
            f"URL should not contain 'AudioFormat' enum name. Got: {url}"
        
        assert "commit_strategy=vad" in url, \
            f"URL should contain 'commit_strategy=vad', not enum repr. Got: {url}"
        assert "CommitStrategy" not in url, \
            f"URL should not contain 'CommitStrategy' enum name. Got: {url}"

    @pytest.mark.asyncio
    @patch("elevenlabs.realtime.scribe.websocket_connect", new_callable=AsyncMock)
    async def test_connect_audio_default_commit_strategy_is_manual(self, mock_ws_connect):
        """Test that the default commit strategy is MANUAL when not specified."""
        mock_websocket = MagicMock()
        mock_ws_connect.return_value = mock_websocket
        mock_websocket.__aiter__ = MagicMock(return_value=iter([]))

        await self.scribe.connect({
            "model_id": "scribe_v2_realtime",
            "audio_format": AudioFormat.PCM_16000,
            "sample_rate": 16000
            # commit_strategy not specified
        })

        url = mock_ws_connect.call_args[0][0]
        assert "commit_strategy=manual" in url


class TestRealtimeConnectionEventHandling:
    """Tests for RealtimeConnection event handling behavior"""

    def setup_method(self):
        """Set up test fixtures"""
        self.mock_websocket = MagicMock()
        self.connection = RealtimeConnection(
            websocket=self.mock_websocket,
            current_sample_rate=16000,
            ffmpeg_process=None
        )

    def test_emit_calls_all_registered_handlers(self):
        """Test that emitting an event calls all registered handlers in order"""
        call_order = []
        
        def handler1(data):
            call_order.append(("handler1", data))
        
        def handler2(data):
            call_order.append(("handler2", data))

        self.connection.on("test_event", handler1)
        self.connection.on("test_event", handler2)
        self.connection._emit("test_event", {"value": 42})

        assert call_order == [
            ("handler1", {"value": 42}),
            ("handler2", {"value": 42})
        ]

    def test_emit_isolates_handler_exceptions(self, capsys):
        """Test that an exception in one handler doesn't prevent others from running"""
        results = []

        def bad_handler(data):
            raise ValueError("Handler error")

        def good_handler(data):
            results.append(data)

        self.connection.on("test_event", bad_handler)
        self.connection.on("test_event", good_handler)
        
        # Should not raise, and good_handler should still be called
        self.connection._emit("test_event", {"value": "test"})

        assert results == [{"value": "test"}]
        captured = capsys.readouterr()
        assert "Error in event handler" in captured.out

    def test_emit_with_no_handlers_does_not_raise(self):
        """Test that emitting to an event with no handlers is a no-op"""
        # Should not raise
        self.connection._emit("nonexistent_event", {"data": "test"})

    def test_handlers_receive_correct_arguments(self):
        """Test that handlers receive all emitted arguments"""
        received_args = []

        def handler(*args):
            received_args.extend(args)

        self.connection.on(RealtimeEvents.PARTIAL_TRANSCRIPT, handler)
        self.connection._emit(RealtimeEvents.PARTIAL_TRANSCRIPT, "arg1", "arg2", {"key": "value"})

        assert received_args == ["arg1", "arg2", {"key": "value"}]
