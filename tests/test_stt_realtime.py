"""Tests for realtime speech-to-text (Scribe) functionality.

These tests cover URL building, validation, and event handling behavior
that don't require an actual WebSocket connection.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import parse_qsl, urlparse

import pytest

from elevenlabs.realtime.connection import RealtimeConnection, RealtimeEvents
from elevenlabs.realtime.scribe import (
    AudioFormat,
    CommitStrategy,
    ScribeRealtime,
)


def query_params(url):
    """Every query parameter on the URL, preserving repeats and their order."""
    return parse_qsl(urlparse(url).query, keep_blank_values=True)


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

    def test_includes_keyterms_as_repeated_query_params(self):
        """Test that keyterms are included as repeated query params"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual",
            keyterms=["ElevenLabs", "Scribe"],
        )

        assert "keyterms=ElevenLabs" in url
        assert "keyterms=Scribe" in url

    def test_includes_no_verbatim_true(self):
        """Test that no_verbatim=true is included when set to True"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual",
            no_verbatim=True,
        )

        assert "no_verbatim=true" in url

    def test_includes_no_verbatim_false(self):
        """Test that no_verbatim=false is included when set to False"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual",
            no_verbatim=False,
        )

        assert "no_verbatim=false" in url

    def test_omits_keyterms_and_no_verbatim_when_not_specified(self):
        """Test that keyterms and no_verbatim are omitted when not specified"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual",
        )

        assert "keyterms" not in url
        assert "no_verbatim" not in url

    def test_serializes_every_supported_option_to_its_parameter_name(self):
        """Exhaustive check: a renamed, dropped or duplicated param fails here"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="vad",
            vad_silence_threshold_secs=1.5,
            vad_threshold=0.4,
            min_speech_duration_ms=100,
            min_silence_duration_ms=200,
            language_code="en",
            secondary_languages=["nl", "de"],
            include_timestamps=False,
            include_language_detection=True,
            keyterms=["ElevenLabs", "Scribe"],
            no_verbatim=True,
            entity_detection=["pii", "email_address"],
            filter_background_audio=True,
            enable_logging=False,
            token="sutkn_1234567890",
        )

        assert sorted(query_params(url)) == sorted([
            ("model_id", "scribe_v2_realtime"),
            ("audio_format", "pcm_16000"),
            ("commit_strategy", "vad"),
            ("vad_silence_threshold_secs", "1.5"),
            ("vad_threshold", "0.4"),
            ("min_speech_duration_ms", "100"),
            ("min_silence_duration_ms", "200"),
            ("language_code", "en"),
            ("secondary_languages", "nl"),
            ("secondary_languages", "de"),
            ("include_timestamps", "false"),
            ("include_language_detection", "true"),
            ("keyterms", "ElevenLabs"),
            ("keyterms", "Scribe"),
            ("no_verbatim", "true"),
            ("entity_detection", "pii"),
            ("entity_detection", "email_address"),
            ("filter_background_audio", "true"),
            ("enable_logging", "false"),
            ("token", "sutkn_1234567890"),
        ])

    def test_sends_nothing_beyond_the_required_parameters(self):
        """Exhaustive check that unset options do not leak into the URL"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual",
        )

        assert sorted(query_params(url)) == sorted([
            ("model_id", "scribe_v2_realtime"),
            ("audio_format", "pcm_16000"),
            ("commit_strategy", "manual"),
        ])

    def test_transmits_booleans_that_are_explicitly_false(self):
        """False is meaningful: dropping it silently reverts to a server default"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual",
            include_timestamps=False,
            include_language_detection=False,
            no_verbatim=False,
            filter_background_audio=False,
            enable_logging=False,
        )

        params = dict(query_params(url))
        assert params["include_timestamps"] == "false"
        assert params["include_language_detection"] == "false"
        assert params["no_verbatim"] == "false"
        assert params["filter_background_audio"] == "false"
        assert params["enable_logging"] == "false"

    def test_accepts_a_bare_string_for_entity_detection(self):
        """A single entity_detection string is sent as one value, not exploded"""
        url = self.scribe._build_websocket_url(
            model_id="scribe_v2_realtime",
            audio_format="pcm_16000",
            commit_strategy="manual",
            entity_detection="all",
        )

        assert [v for k, v in query_params(url) if k == "entity_detection"] == ["all"]


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

    @pytest.mark.asyncio
    @patch("elevenlabs.realtime.scribe.websocket_connect", new_callable=AsyncMock)
    async def test_connect_threads_every_option_into_url(self, mock_ws_connect):
        """Exhaustive check of the option key to query parameter mapping.

        The URL builder is tested directly elsewhere, so this is the only cover
        for _shared_url_kwargs: a typo there would drop an option silently.
        """
        mock_websocket = MagicMock()
        mock_ws_connect.return_value = mock_websocket
        mock_websocket.__aiter__ = MagicMock(return_value=iter([]))

        await self.scribe.connect({
            "model_id": "scribe_v2_realtime",
            "audio_format": AudioFormat.PCM_16000,
            "sample_rate": 16000,
            "commit_strategy": CommitStrategy.VAD,
            "vad_silence_threshold_secs": 1.5,
            "vad_threshold": 0.4,
            "min_speech_duration_ms": 100,
            "min_silence_duration_ms": 200,
            "language_code": "en",
            "secondary_languages": ["en", "nl"],
            "include_timestamps": False,
            "include_language_detection": True,
            "keyterms": ["ElevenLabs"],
            "no_verbatim": True,
            "entity_detection": ["pii", "email_address"],
            "filter_background_audio": True,
            "enable_logging": False,
            "token": "sutkn_1234567890",
        })

        url = mock_ws_connect.call_args[0][0]
        assert sorted(query_params(url)) == sorted([
            ("model_id", "scribe_v2_realtime"),
            ("audio_format", "pcm_16000"),
            ("commit_strategy", "vad"),
            ("vad_silence_threshold_secs", "1.5"),
            ("vad_threshold", "0.4"),
            ("min_speech_duration_ms", "100"),
            ("min_silence_duration_ms", "200"),
            ("language_code", "en"),
            ("secondary_languages", "en"),
            ("secondary_languages", "nl"),
            ("include_timestamps", "false"),
            ("include_language_detection", "true"),
            ("keyterms", "ElevenLabs"),
            ("no_verbatim", "true"),
            ("entity_detection", "pii"),
            ("entity_detection", "email_address"),
            ("filter_background_audio", "true"),
            ("enable_logging", "false"),
            ("token", "sutkn_1234567890"),
        ])


class TestConnectAuthentication:
    """Tests for API key vs single-use token authentication"""

    @pytest.mark.asyncio
    @patch("elevenlabs.realtime.scribe.websocket_connect", new_callable=AsyncMock)
    async def test_api_key_sent_as_header(self, mock_ws_connect):
        """Test that a configured api_key is sent in the xi-api-key header"""
        mock_websocket = MagicMock()
        mock_ws_connect.return_value = mock_websocket
        mock_websocket.__aiter__ = MagicMock(return_value=iter([]))

        scribe = ScribeRealtime(api_key="test-api-key")
        await scribe.connect({
            "model_id": "scribe_v2_realtime",
            "audio_format": AudioFormat.PCM_16000,
            "sample_rate": 16000,
        })

        headers = mock_ws_connect.call_args.kwargs["additional_headers"]
        assert headers == {"xi-api-key": "test-api-key"}

    @pytest.mark.asyncio
    @patch("elevenlabs.realtime.scribe.websocket_connect", new_callable=AsyncMock)
    async def test_token_only_omits_api_key_header(self, mock_ws_connect):
        """Test that a token authenticates without sending an empty api key header"""
        mock_websocket = MagicMock()
        mock_ws_connect.return_value = mock_websocket
        mock_websocket.__aiter__ = MagicMock(return_value=iter([]))

        scribe = ScribeRealtime(api_key="")
        await scribe.connect({
            "model_id": "scribe_v2_realtime",
            "audio_format": AudioFormat.PCM_16000,
            "sample_rate": 16000,
            "token": "sutkn_1234567890",
        })

        headers = mock_ws_connect.call_args.kwargs["additional_headers"]
        assert headers == {}
        assert "token=sutkn_1234567890" in mock_ws_connect.call_args[0][0]

    @pytest.mark.asyncio
    @patch("elevenlabs.realtime.scribe.websocket_connect", new_callable=AsyncMock)
    async def test_token_takes_precedence_over_configured_api_key(self, mock_ws_connect):
        """The server authenticates the token and never falls back to the key, so
        sending it would transmit a long-lived credential that cannot be used."""
        mock_websocket = MagicMock()
        mock_ws_connect.return_value = mock_websocket
        mock_websocket.__aiter__ = MagicMock(return_value=iter([]))

        scribe = ScribeRealtime(api_key="test-api-key")
        await scribe.connect({
            "model_id": "scribe_v2_realtime",
            "audio_format": AudioFormat.PCM_16000,
            "sample_rate": 16000,
            "token": "sutkn_1234567890",
        })

        headers = mock_ws_connect.call_args.kwargs["additional_headers"]
        assert headers == {}
        assert "token=sutkn_1234567890" in mock_ws_connect.call_args[0][0]

    @pytest.mark.asyncio
    async def test_requires_api_key_or_token(self):
        """Test that connecting without either credential raises"""
        scribe = ScribeRealtime(api_key="")
        with pytest.raises(ValueError, match="api_key or a single-use token is required"):
            await scribe.connect({
                "model_id": "scribe_v2_realtime",
                "audio_format": AudioFormat.PCM_16000,
                "sample_rate": 16000,
            })


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


class _FakeWebsocket:
    """Minimal async-iterable stand-in for a websocket connection."""

    def __init__(self, messages):
        self._messages = list(messages)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._messages:
            raise StopAsyncIteration
        return self._messages.pop(0)


class TestMessageDispatch:
    """Tests that server message types are routed to the matching events"""

    async def _dispatch(self, *messages):
        """Feed raw JSON messages through the connection's message handler"""
        self.connection = RealtimeConnection(
            websocket=_FakeWebsocket([json.dumps(m) for m in messages]),
            current_sample_rate=16000,
            ffmpeg_process=None,
        )
        for event, sink in self._subscriptions:
            self.connection.on(event, sink)
        await self.connection._start_message_handler()

    def setup_method(self):
        """Set up test fixtures"""
        self._subscriptions = []

    def subscribe(self, event):
        """Register a sink for an event, returning the list it collects into"""
        received = []
        self._subscriptions.append((event, received.append))
        return received

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message_type",
        [
            "final_transcript",
            "final_transcript_with_timestamps",
            "committed_transcript_entities",
        ],
    )
    async def test_dispatches_transcript_events(self, message_type):
        """Test that transcript message types reach their handlers"""
        received = self.subscribe(message_type)

        await self._dispatch({"message_type": message_type, "text": "hello"})

        assert received == [{"message_type": message_type, "text": "hello"}]

    @pytest.mark.asyncio
    async def test_invalid_request_emits_specific_and_generic_error(self):
        """Parameter rejections arrive as a message before the socket closes;
        dropping it leaves the caller with a closed connection and no reason why."""
        specific = self.subscribe(RealtimeEvents.INVALID_REQUEST)
        generic = self.subscribe(RealtimeEvents.ERROR)

        payload = {
            "message_type": "invalid_request",
            "error": "Number of keyterms cannot exceed 50. You provided 51 keyterms.",
        }
        await self._dispatch(payload)

        assert specific == [payload]
        assert generic == [payload]

    @pytest.mark.asyncio
    async def test_unaccepted_terms_emits_both_event_names(self):
        """Test that the server's unaccepted_terms also fires the older event name"""
        new_name = self.subscribe(RealtimeEvents.UNACCEPTED_TERMS)
        old_name = self.subscribe(RealtimeEvents.UNACCEPTED_TERMS_ERROR)
        generic_error = self.subscribe(RealtimeEvents.ERROR)

        payload = {"message_type": "unaccepted_terms", "error": "terms not accepted"}
        await self._dispatch(payload)

        assert new_name == [payload]
        assert old_name == [payload]
        assert generic_error == [payload]
