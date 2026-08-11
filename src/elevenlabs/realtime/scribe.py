import asyncio
import base64
import subprocess
import typing
from enum import Enum
from typing import overload

from typing_extensions import Required

try:
    from websockets.asyncio.client import connect as websocket_connect
except ImportError:
    raise ImportError(
        "The websockets package is required for realtime speech-to-text. "
        "Install it with: pip install websockets"
    )

from ..url_utils import build_ws_url
from .connection import RealtimeConnection


class AudioFormat(str, Enum):
    """Audio format options for realtime transcription"""
    PCM_8000 = "pcm_8000"
    PCM_16000 = "pcm_16000"
    PCM_22050 = "pcm_22050"
    PCM_24000 = "pcm_24000"
    PCM_44100 = "pcm_44100"
    PCM_48000 = "pcm_48000"
    ULAW_8000 = "ulaw_8000"


class CommitStrategy(str, Enum):
    """
    Strategy for committing transcription results.

    VAD: Voice Activity Detection - automatically commits when speech ends
    MANUAL: Manual commit - requires calling commit() to commit the segment
    """
    VAD = "vad"
    MANUAL = "manual"


RealtimeEntityDetection = typing.Union[str, typing.List[str]]
"""
Entities to detect on committed transcripts.

Accepts ``"all"``, a single category (``"pii"``, ``"phi"``, ``"pci"``, ``"other"``,
``"offensive_language"``), a specific entity type such as ``"email_address"``, or a
list of categories/types.
"""


class _RealtimeSharedOptions(typing.TypedDict, total=False):
    """
    Options accepted by both realtime connection modes.

    Attributes:
        model_id: The model ID to use for transcription (required)
        commit_strategy: Strategy for committing transcriptions (optional, defaults to MANUAL)
        vad_silence_threshold_secs: Silence threshold in seconds for VAD (must be between 0.3 and 3.0)
        vad_threshold: Threshold for voice activity detection (must be between 0.1 and 0.9)
        min_speech_duration_ms: Minimum speech duration in milliseconds (must be between 50 and 2000)
        min_silence_duration_ms: Minimum silence duration in milliseconds (must be between 50 and 2000)
        language_code: An ISO-639-1 or ISO-639-3 language_code corresponding to the language of the audio file. Can sometimes improve transcription performance if known beforehand.
        secondary_languages: Additional ISO-639-1 or ISO-639-3 language codes that may be present in the audio. Providing them makes language identification more reliable by only focusing on a certain set of languages.
        include_timestamps: Whether to receive the committed_transcript_with_timestamps event after committing the segment (optional, defaults to False)
        include_language_detection: Whether to receive a delayed final transcript carrying the detected language_code after each commit (optional, defaults to False)
        keyterms: Keyterms to bias the model towards (maximum 50, each at most 20 characters)
        no_verbatim: If True, removes filler words, false starts and disfluencies from the transcript
        entity_detection: Entities to detect on committed transcripts, delivered in a separate committed_transcript_entities event
        filter_background_audio: Reduce false activations from nearby conversations and ambient noise. Cannot be combined with include_timestamps.
        enable_logging: When False, zero retention mode is used for the request. Only available to enterprise customers.
        token: A single-use token used to authenticate the session instead of an API key. Useful when connecting from a client where an API key should not be exposed. Takes precedence over any configured api_key, which is not sent when a token is supplied.
    """
    model_id: Required[str]
    commit_strategy: CommitStrategy
    vad_silence_threshold_secs: float
    vad_threshold: float
    min_speech_duration_ms: int
    min_silence_duration_ms: int
    language_code: str
    secondary_languages: typing.List[str]
    include_timestamps: bool
    include_language_detection: bool
    keyterms: typing.List[str]
    no_verbatim: bool
    entity_detection: RealtimeEntityDetection
    filter_background_audio: bool
    enable_logging: bool
    token: str


class RealtimeAudioOptions(_RealtimeSharedOptions, total=False):
    """
    Options for providing audio chunks manually.

    Accepts every key in :class:`_RealtimeSharedOptions`, plus:

    Attributes:
        audio_format: The audio format (required)
        sample_rate: The sample rate in Hz (required)
    """
    audio_format: Required[AudioFormat]
    sample_rate: Required[int]


class RealtimeUrlOptions(_RealtimeSharedOptions, total=False):
    """
    Options for streaming audio from a URL.

    Accepts every key in :class:`_RealtimeSharedOptions`, plus:

    Attributes:
        url: The URL of the audio stream (required)
    """
    url: Required[str]


class ScribeRealtime:
    """
    Helper class for creating realtime speech-to-text connections.

    Supports two modes:
    1. URL-based: Stream audio from a URL (uses ffmpeg for conversion)
    2. Manual: Send audio chunks yourself

    Example (URL-based):
        ```python
        connection = await elevenlabs.speech_to_text.realtime.connect({
            "model_id": "scribe_v2_realtime",
            "url": "https://stream.example.com/audio.mp3"
        })
        ```

    Example (Manual chunks):
        ```python
        connection = await elevenlabs.speech_to_text.realtime.connect({
            "model_id": "scribe_v2_realtime",
            "audio_format": AudioFormat.PCM_16000,
            "sample_rate": 16000
        })

        # Send audio chunks
        await connection.send({"audio_base_64": chunk})
        ```
    """

    def __init__(self, api_key: str, base_url: str = "wss://api.elevenlabs.io"):
        self.api_key = api_key
        self.base_url = base_url

    @overload
    async def connect(
        self,
        options: RealtimeAudioOptions
    ) -> RealtimeConnection: ...

    @overload
    async def connect(
        self,
        options: RealtimeUrlOptions
    ) -> RealtimeConnection: ...

    async def connect(
        self,
        options: typing.Union[RealtimeAudioOptions, RealtimeUrlOptions]
    ) -> RealtimeConnection:
        """
        Create a realtime transcription connection.

        Args:
            options: Either RealtimeAudioOptions for manual chunk sending or RealtimeUrlOptions for URL streaming

        Returns:
            RealtimeConnection instance ready to send/receive data

        Raises:
            ValueError: If invalid options are provided
            RuntimeError: If ffmpeg is not available (for URL-based streaming)

        Example:
            ```python
            # URL-based streaming
            connection = await elevenlabs.speech_to_text.realtime.connect({
                "model_id": "scribe_v2_realtime",
                "url": "https://stream.example.com/audio.mp3",
            })

            # Manual chunks
            connection = await elevenlabs.speech_to_text.realtime.connect({
                "model_id": "scribe_v2_realtime",
                "audio_format": AudioFormat.PCM_16000,
                "sample_rate": 16000,
                "commit_strategy": CommitStrategy.MANUAL
            })
            ```
        """
        # Determine if this is URL-based or manual mode
        is_url_mode = "url" in options

        if "model_id" not in options:
            raise ValueError("model_id is required for realtime transcription")

        if is_url_mode:
            return await self._connect_url(typing.cast(RealtimeUrlOptions, options))
        else:
            return await self._connect_audio(typing.cast(RealtimeAudioOptions, options))

    @staticmethod
    def _shared_url_kwargs(
        options: typing.Union[RealtimeAudioOptions, RealtimeUrlOptions]
    ) -> typing.Dict[str, typing.Any]:
        """Collect the query parameters both connection modes share."""
        return {
            "vad_silence_threshold_secs": options.get("vad_silence_threshold_secs"),
            "vad_threshold": options.get("vad_threshold"),
            "min_speech_duration_ms": options.get("min_speech_duration_ms"),
            "min_silence_duration_ms": options.get("min_silence_duration_ms"),
            "language_code": options.get("language_code"),
            "secondary_languages": options.get("secondary_languages"),
            "include_timestamps": options.get("include_timestamps", False),
            "include_language_detection": options.get("include_language_detection"),
            "keyterms": options.get("keyterms"),
            "no_verbatim": options.get("no_verbatim"),
            "entity_detection": options.get("entity_detection"),
            "filter_background_audio": options.get("filter_background_audio"),
            "enable_logging": options.get("enable_logging"),
            "token": options.get("token"),
        }

    def _connection_headers(
        self, options: typing.Union[RealtimeAudioOptions, RealtimeUrlOptions]
    ) -> typing.Dict[str, str]:
        """
        Build the handshake headers.

        A single-use token authenticates the session on its own and takes
        precedence server-side, so the api key is not sent alongside one.
        """
        if options.get("token"):
            return {}
        if not self.api_key:
            raise ValueError(
                "An api_key or a single-use token is required for realtime transcription"
            )
        return {"xi-api-key": self.api_key}

    async def _connect_audio(self, options: RealtimeAudioOptions) -> RealtimeConnection:
        """Connect with manual audio chunk sending"""
        model_id = options["model_id"]
        audio_format = options.get("audio_format")
        sample_rate = options.get("sample_rate")
        commit_strategy = options.get("commit_strategy", CommitStrategy.MANUAL)

        if not audio_format or not sample_rate:
            raise ValueError("audio_format and sample_rate are required for manual audio mode")

        headers = self._connection_headers(options)

        # Build WebSocket URL with query parameters
        ws_url = self._build_websocket_url(
            model_id=model_id,
            audio_format=audio_format.value,
            commit_strategy=commit_strategy.value,
            **self._shared_url_kwargs(options),
        )

        # Connect to WebSocket
        websocket = await websocket_connect(ws_url, additional_headers=headers)

        # Create connection object
        connection = RealtimeConnection(
            websocket=websocket,
            current_sample_rate=sample_rate,
            ffmpeg_process=None
        )

        # Start message handler
        connection._message_task = asyncio.create_task(connection._start_message_handler())
        connection._emit("open")

        return connection

    async def _connect_url(self, options: RealtimeUrlOptions) -> RealtimeConnection:
        """Connect with URL-based audio streaming using ffmpeg"""
        model_id = options["model_id"]
        url = options.get("url")
        commit_strategy = options.get("commit_strategy", CommitStrategy.MANUAL)

        if not url:
            raise ValueError("url is required for URL mode")

        # Default to 16kHz for URL streaming
        sample_rate = 16000
        audio_format = AudioFormat.PCM_16000

        headers = self._connection_headers(options)

        # Build WebSocket URL
        ws_url = self._build_websocket_url(
            model_id=model_id,
            audio_format=audio_format.value,
            commit_strategy=commit_strategy.value,
            **self._shared_url_kwargs(options),
        )

        # Connect to WebSocket
        websocket = await websocket_connect(ws_url, additional_headers=headers)

        # Start ffmpeg process to convert stream to PCM
        try:
            ffmpeg_process = subprocess.Popen(
                [
                    "ffmpeg",
                    "-i", url,
                    "-f", "s16le",
                    "-ar", str(sample_rate),
                    "-ac", "1",
                    "-"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                bufsize=0
            )
        except FileNotFoundError:
            await websocket.close(1011, "ffmpeg not found")
            raise RuntimeError(
                "ffmpeg is required for URL-based audio streaming. "
                "Please install ffmpeg: https://ffmpeg.org/download.html"
            )

        # Create connection object
        connection = RealtimeConnection(
            websocket=websocket,
            current_sample_rate=sample_rate,
            ffmpeg_process=ffmpeg_process
        )

        # Start message handler
        connection._message_task = asyncio.create_task(connection._start_message_handler())
        connection._emit("open")

        # Start streaming audio from ffmpeg to websocket
        asyncio.create_task(self._stream_ffmpeg_to_websocket(connection))

        return connection

    async def _stream_ffmpeg_to_websocket(self, connection: RealtimeConnection) -> None:
        """Stream audio from ffmpeg process to WebSocket"""
        if not connection.ffmpeg_process or not connection.ffmpeg_process.stdout:
            return

        try:
            # Read chunks from ffmpeg and send to websocket
            chunk_size = 8192  # 8KB chunks

            loop = asyncio.get_event_loop()

            while True:
                # Read from ffmpeg stdout in a non-blocking way
                chunk = await loop.run_in_executor(
                    None,
                    connection.ffmpeg_process.stdout.read,
                    chunk_size
                )

                if not chunk:
                    # Stream ended
                    break

                # Convert to base64 and send
                chunk_base64 = base64.b64encode(chunk).decode('utf-8')

                try:
                    await connection.send({"audio_base_64": chunk_base64})
                except Exception as e:
                    connection._emit("error", {"error": f"Failed to send audio: {e}"})
                    break

                # Small delay to prevent overwhelming the connection
                await asyncio.sleep(0.01)

        except Exception as e:
            connection._emit("error", {"error": f"FFmpeg streaming error: {e}"})
        finally:
            # Clean up ffmpeg process
            if connection.ffmpeg_process:
                connection.ffmpeg_process.kill()
                try:
                    connection.ffmpeg_process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    connection.ffmpeg_process.kill()

    def _build_websocket_url(
        self,
        model_id: str,
        audio_format: str,
        commit_strategy: str,
        vad_silence_threshold_secs: typing.Optional[float] = None,
        vad_threshold: typing.Optional[float] = None,
        min_speech_duration_ms: typing.Optional[int] = None,
        min_silence_duration_ms: typing.Optional[int] = None,
        language_code: typing.Optional[str] = None,
        secondary_languages: typing.Optional[typing.List[str]] = None,
        include_timestamps: typing.Optional[bool] = None,
        include_language_detection: typing.Optional[bool] = None,
        keyterms: typing.Optional[typing.List[str]] = None,
        no_verbatim: typing.Optional[bool] = None,
        entity_detection: typing.Optional[RealtimeEntityDetection] = None,
        filter_background_audio: typing.Optional[bool] = None,
        enable_logging: typing.Optional[bool] = None,
        token: typing.Optional[str] = None,
    ) -> str:
        """Build the WebSocket URL with query parameters"""
        params = [
            ("model_id", model_id),
            ("audio_format", audio_format),
            ("commit_strategy", commit_strategy),
        ]
        for key, value in [
            ("vad_silence_threshold_secs", vad_silence_threshold_secs),
            ("vad_threshold", vad_threshold),
            ("min_speech_duration_ms", min_speech_duration_ms),
            ("min_silence_duration_ms", min_silence_duration_ms),
            ("language_code", language_code),
        ]:
            if value is not None:
                params.append((key, str(value)))
        if secondary_languages is not None:
            for language in secondary_languages:
                params.append(("secondary_languages", language))
        if include_timestamps is not None:
            params.append(("include_timestamps", str(include_timestamps).lower()))
        if include_language_detection is not None:
            params.append(
                ("include_language_detection", str(include_language_detection).lower())
            )
        if keyterms is not None:
            for term in keyterms:
                params.append(("keyterms", term))
        if no_verbatim is not None:
            params.append(("no_verbatim", str(no_verbatim).lower()))
        if entity_detection is not None:
            entities = (
                [entity_detection]
                if isinstance(entity_detection, str)
                else entity_detection
            )
            for entity in entities:
                params.append(("entity_detection", entity))
        if filter_background_audio is not None:
            params.append(
                ("filter_background_audio", str(filter_background_audio).lower())
            )
        if enable_logging is not None:
            params.append(("enable_logging", str(enable_logging).lower()))
        if token is not None:
            params.append(("token", token))

        return build_ws_url(self.base_url, ["v1", "speech-to-text", "realtime"], params)

