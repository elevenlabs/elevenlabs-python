"""Support for the ``websocket-realtime`` connection type.

The Realtime endpoint (``/v1/convai/realtime``) speaks an OpenAI-compatible protocol and does not load a
saved agent. This module translates that protocol to and from the native conversation event stream, so the
conversation classes handle both connection types with the same callbacks and audio interfaces.

BETA: This API is subject to change without regard to backwards compatibility.
"""

import array
import json
import logging
import math
import sys
import threading
import time
import typing
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Literal, Optional, Sequence, Set, Union

logger = logging.getLogger(__name__)

# Marks an option as not provided, so `None` can carry its own meaning.
OMIT = typing.cast(typing.Any, ...)

RealtimeAudioFormat = Literal["pcm_24000", "ulaw_8000"]

REALTIME_SUBPROTOCOL = "realtime"
CLIENT_SECRET_SUBPROTOCOL_PREFIX = "openai-insecure-api-key."
REALTIME_DISABLED_CLOSE_CODE = 4003

# The sample rate of the audio exchanged with `AudioInterface` and `AsyncAudioInterface`.
AUDIO_INTERFACE_SAMPLE_RATE = 16000

_SUPPORTED_AUDIO_FORMATS = ("pcm_24000", "ulaw_8000")
_SPEECH_STARTED_VAD_SCORE = 1
_SPEECH_STOPPED_VAD_SCORE = 0


@dataclass
class RealtimeFunctionTool:
    """A client tool the model may call. Register a handler with the same name in ``ClientTools``.

    Args:
        name: The tool name the model calls.
        description: What the tool does and when to call it.
        parameters: JSON Schema for the tool's arguments.
    """

    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class RealtimeTurnDetection:
    """Server-side turn detection.

    Args:
        type: The turn detection mode. Only ``"semantic_vad"`` is supported.
        eagerness: How eagerly the model ends the user's turn.
        create_response: Whether the server responds automatically when the user's turn ends.
        interrupt_response: Whether user speech interrupts the agent. Defaults to ``True``.
    """

    type: Literal["semantic_vad"] = "semantic_vad"
    eagerness: Optional[Literal["low", "medium", "high", "auto"]] = None
    create_response: Optional[bool] = None
    interrupt_response: Optional[bool] = None


@dataclass
class RealtimeSessionOptions:
    """Session configuration sent to the Realtime endpoint in ``session.update``.

    The audio formats only select what is sent over the wire. Audio interfaces always exchange
    16-bit PCM mono at 16kHz, whichever format is chosen.

    Args:
        instructions: The system instructions for the model.
        voice: The voice the model speaks with.
        input_audio_format: The wire format of user audio.
        output_audio_format: The wire format of agent audio.
        turn_detection: Server-side turn detection. Omit for the server default, or pass ``None``
            to disable it for manual turn-taking.
        tools: Client tools the model may call.
        temperature: The sampling temperature.
        max_output_tokens: The maximum number of tokens per response, or ``"inf"``.
    """

    instructions: Optional[str] = None
    voice: Optional[str] = None
    input_audio_format: RealtimeAudioFormat = "pcm_24000"
    output_audio_format: RealtimeAudioFormat = "pcm_24000"
    turn_detection: Optional[RealtimeTurnDetection] = OMIT
    tools: List[RealtimeFunctionTool] = field(default_factory=list)
    temperature: Optional[float] = None
    max_output_tokens: Optional[Union[int, Literal["inf"]]] = None


class RealtimeUnsupportedFeatureError(RuntimeError):
    """Raised for conversation features that have no equivalent on the Realtime endpoint."""

    def __init__(self, feature: str):
        super().__init__(f"{feature} is not supported by websocket-realtime connections.")
        self.feature = feature


class RealtimeConnectionError(ConnectionError):
    """Raised when the Realtime session cannot be established."""

    def __init__(self, message: str, close_code: Optional[int] = None, close_reason: Optional[str] = None):
        super().__init__(message)
        self.close_code = close_code
        self.close_reason = close_reason


def validate_realtime_options(options: RealtimeSessionOptions) -> None:
    """Rejects options the Realtime endpoint would otherwise reject or silently ignore."""
    turn_detection = options.turn_detection
    if turn_detection is not OMIT and turn_detection is not None and turn_detection.type != "semantic_vad":
        raise ValueError(
            f'Unsupported realtime turn_detection type "{turn_detection.type}". '
            'Use "semantic_vad", or None for manual turn-taking.'
        )

    for audio_format in (options.input_audio_format, options.output_audio_format):
        if audio_format not in _SUPPORTED_AUDIO_FORMATS:
            raise ValueError(
                f'Unsupported realtime audio format "{audio_format}". '
                f"Use one of: {', '.join(_SUPPORTED_AUDIO_FORMATS)}."
            )

    tool_names: Set[str] = set()
    for tool in options.tools:
        if not tool.name:
            raise ValueError("Every realtime tool requires a name.")
        if tool.name in tool_names:
            raise ValueError(f'Duplicate realtime tool name "{tool.name}".')
        tool_names.add(tool.name)


def realtime_subprotocols(client_secret: str) -> List[str]:
    return [REALTIME_SUBPROTOCOL, f"{CLIENT_SECRET_SUBPROTOCOL_PREFIX}{client_secret}"]


def build_session_update(options: RealtimeSessionOptions, text_only: bool) -> Dict[str, Any]:
    audio_input: Dict[str, Any] = {"format": _to_wire_audio_format(options.input_audio_format)}
    turn_detection = options.turn_detection
    if turn_detection is None:
        audio_input["turn_detection"] = None
    elif turn_detection is not OMIT:
        audio_input["turn_detection"] = _omit_none(
            {
                "type": turn_detection.type,
                "eagerness": turn_detection.eagerness,
                "create_response": turn_detection.create_response,
                "interrupt_response": turn_detection.interrupt_response,
            }
        )

    audio_output = _omit_none(
        {"format": _to_wire_audio_format(options.output_audio_format), "voice": options.voice}
    )

    session = _omit_none(
        {
            "type": "realtime",
            "output_modalities": ["text" if text_only else "audio"],
            "instructions": options.instructions,
            "audio": {"input": audio_input, "output": audio_output},
            "tools": [
                _omit_none(
                    {
                        "type": "function",
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    }
                )
                for tool in options.tools
            ]
            or None,
            "temperature": options.temperature,
            "max_output_tokens": options.max_output_tokens,
        }
    )
    return {"type": "session.update", "session": session}


@dataclass(frozen=True)
class RealtimeWireFormat:
    """An audio format in effect on the wire."""

    encoding: Literal["pcm", "ulaw"]
    sample_rate: int

    @property
    def native_name(self) -> str:
        return f"{self.encoding}_{self.sample_rate}"


@dataclass(frozen=True)
class RealtimeEffectiveSession:
    """The session configuration in effect, as reported by ``session.updated``."""

    id: str
    input_format: RealtimeWireFormat
    output_format: RealtimeWireFormat
    interrupt_on_speech: bool


class RealtimeHandshake:
    """Configures the session: waits for ``session.created``, sends ``session.update`` and
    resolves with the effective session once ``session.updated`` arrives.

    Performs no I/O, so the sync and async conversations share it.
    """

    def __init__(self, options: RealtimeSessionOptions, text_only: bool):
        self._options = options
        self._session_update = build_session_update(options, text_only)
        self._session_id: Optional[str] = None
        self.session: Optional[RealtimeEffectiveSession] = None

    def handle_message(self, raw: Union[str, bytes]) -> Optional[Dict[str, Any]]:
        """Returns an event to send, if any. Sets ``session`` once the handshake completes.

        Raises:
            RealtimeConnectionError: If the server rejects the session.
        """
        message = parse_server_event(raw)
        if message is None:
            return None

        if message["type"] == "session.created":
            self._session_id = (message.get("session") or {}).get("id")
            return self._session_update

        if message["type"] == "session.updated":
            session = message.get("session") or {}
            session_id = self._session_id or session.get("id")
            if not session_id:
                raise RealtimeConnectionError("The Realtime endpoint did not report a session id.")
            audio = session.get("audio") or {}
            audio_input = audio.get("input") or {}
            audio_output = audio.get("output") or {}
            turn_detection = audio_input.get("turn_detection") or {}
            requested_turn_detection = self._options.turn_detection
            requested_interrupt = (
                requested_turn_detection.interrupt_response
                if requested_turn_detection is not OMIT and requested_turn_detection is not None
                else None
            )
            interrupt_on_speech = turn_detection.get("interrupt_response")
            if interrupt_on_speech is None:
                interrupt_on_speech = True if requested_interrupt is None else requested_interrupt
            self.session = RealtimeEffectiveSession(
                id=session_id,
                input_format=_from_wire_audio_format(audio_input.get("format"), self._options.input_audio_format),
                output_format=_from_wire_audio_format(audio_output.get("format"), self._options.output_audio_format),
                interrupt_on_speech=bool(interrupt_on_speech),
            )
            return None

        if message["type"] == "error":
            error = message.get("error") or {}
            raise RealtimeConnectionError(error.get("message") or "The Realtime endpoint rejected the session.")

        return None


def handshake_close_error(code: Optional[int], reason: Optional[str]) -> RealtimeConnectionError:
    if reason or code == REALTIME_DISABLED_CLOSE_CODE:
        message = describe_close(code, reason)
    elif code == 1000:
        message = "Connection closed normally before session could be established."
    else:
        message = "Connection closed unexpectedly before session could be established."
    return RealtimeConnectionError(message, close_code=code, close_reason=reason or None)


def describe_close(code: Optional[int], reason: Optional[str]) -> str:
    if reason:
        return reason
    if code == REALTIME_DISABLED_CLOSE_CODE:
        return "The Realtime API is not enabled for this workspace."
    return "The connection was closed by the server."


def parse_server_event(raw: Union[str, bytes]) -> Optional[Dict[str, Any]]:
    try:
        parsed = json.loads(raw)
    except (TypeError, ValueError):
        return None
    if isinstance(parsed, dict) and isinstance(parsed.get("type"), str):
        return parsed
    return None


def initiation_metadata_event(session: RealtimeEffectiveSession) -> Dict[str, Any]:
    """Synthesized, since the Realtime endpoint never sends initiation metadata."""
    return {
        "type": "conversation_initiation_metadata",
        "conversation_initiation_metadata_event": {
            "conversation_id": session.id,
            "agent_output_audio_format": session.output_format.native_name,
            "user_input_audio_format": session.input_format.native_name,
        },
    }


@dataclass
class RealtimeTranslation:
    """The result of translating one event.

    Attributes:
        events: Native events to handle, as if the server had sent them.
        sends: Realtime events to send to the server, in order.
    """

    events: List[Dict[str, Any]] = field(default_factory=list)
    sends: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class _ResponseState:
    id: str
    event_id: int
    text: str = ""
    agent_response: Optional[str] = None
    streaming: bool = False
    done: bool = False
    interrupted: bool = False
    audio_item_id: Optional[str] = None
    audio_content_index: int = 0
    audio_received_ms: float = 0
    playback_start_at: Optional[float] = None
    truncate_at_ms: Optional[int] = None


class RealtimeProtocolTranslator:
    """Translates between the Realtime wire protocol and the native conversation event stream.

    Thread-safe. Returns its effects instead of performing them, so callers can send and dispatch
    them outside the lock, synchronously or asynchronously.
    """

    def __init__(
        self,
        output_format: RealtimeWireFormat,
        interrupt_on_speech: bool,
        now: Optional[Callable[[], float]] = None,
    ):
        self._output_format = output_format
        self._interrupt_on_speech = interrupt_on_speech
        self._now = now or (lambda: time.monotonic() * 1000)
        self._lock = threading.Lock()
        self._out = RealtimeTranslation()

        self._last_event_id = 0
        self._internal_event_count = 0
        self._internal_event_ids: Set[str] = set()
        self._responses: Dict[str, _ResponseState] = {}
        self._active_response_id: Optional[str] = None
        self._last_audio_response: Optional[_ResponseState] = None
        self._playback_ends_at: float = 0
        self._pending_tool_calls: Set[str] = set()
        self._pending_corrections: Dict[str, _ResponseState] = {}

    def handle_server_event(self, event: Dict[str, Any]) -> RealtimeTranslation:
        with self._lock:
            self._out = RealtimeTranslation()
            self._dispatch_server_event(event)
            return self._out

    def handle_outgoing_event(self, message: Dict[str, Any]) -> RealtimeTranslation:
        """Translates a native client event.

        Raises:
            RealtimeUnsupportedFeatureError: For native events with no Realtime equivalent.
        """
        with self._lock:
            self._out = RealtimeTranslation()
            self._dispatch_outgoing_event(message)
            return self._out

    def _dispatch_server_event(self, event: Dict[str, Any]) -> None:
        event_type = event.get("type")
        if event_type == "response.created":
            response_id = (event.get("response") or {}).get("id")
            if isinstance(response_id, str):
                self._ensure_response(response_id)
                self._active_response_id = response_id
        elif event_type == "response.output_audio.delta":
            self._handle_audio_delta(event)
        elif event_type in ("response.output_audio_transcript.delta", "response.output_text.delta"):
            self._handle_text_delta(event)
        elif event_type == "response.done":
            self._handle_response_done(event)
        elif event_type == "input_audio_buffer.speech_started":
            self._emit_vad_score(_SPEECH_STARTED_VAD_SCORE)
            if self._interrupt_on_speech:
                self._interrupt()
        elif event_type == "input_audio_buffer.speech_stopped":
            self._emit_vad_score(_SPEECH_STOPPED_VAD_SCORE)
        elif event_type == "conversation.item.input_audio_transcription.completed":
            self._emit(
                {
                    "type": "user_transcript",
                    "user_transcription_event": {
                        "user_transcript": event.get("transcript") or "",
                        "event_id": self._next_event_id(),
                    },
                }
            )
        elif event_type == "conversation.item.truncated":
            if event.get("item_id") in self._pending_corrections:
                self._send_internal({"type": "conversation.item.retrieve", "item_id": event["item_id"]})
        elif event_type == "conversation.item.retrieved":
            self._handle_item_retrieved(event)
        elif event_type == "error":
            self._handle_error(event)
        else:
            logger.debug("Unhandled realtime event: %s", event_type)

    def _dispatch_outgoing_event(self, message: Dict[str, Any]) -> None:
        if "type" not in message:
            self._send({"type": "input_audio_buffer.append", "audio": message["user_audio_chunk"]})
            return

        message_type = message["type"]
        if message_type == "user_message":
            self._interrupt()
            if self._active_response_id:
                self._send_internal({"type": "response.cancel"})
            self._send(
                {
                    "type": "conversation.item.create",
                    "item": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": message.get("text") or ""}],
                    },
                }
            )
            self._send({"type": "response.create"})
        elif message_type == "client_tool_result":
            call_id = message.get("tool_call_id")
            self._send(
                {
                    "type": "conversation.item.create",
                    "item": {
                        "type": "function_call_output",
                        "call_id": call_id,
                        "output": _tool_output(message.get("result")),
                    },
                }
            )
            # The model only continues once every call from the response has an output.
            if call_id in self._pending_tool_calls:
                self._pending_tool_calls.discard(call_id)
                if not self._pending_tool_calls:
                    self._send({"type": "response.create"})
        elif message_type in ("pong", "user_activity"):
            return
        else:
            raise RealtimeUnsupportedFeatureError(str(getattr(message_type, "value", message_type)))

    # Interruption ids must sit between response ids for stale audio to be dropped.
    def _next_event_id(self) -> int:
        self._last_event_id += 1
        return self._last_event_id

    def _ensure_response(self, response_id: str) -> _ResponseState:
        state = self._responses.get(response_id)
        if state is None:
            state = _ResponseState(id=response_id, event_id=self._next_event_id())
            self._responses[response_id] = state
        return state

    def _release_response(self, state: _ResponseState) -> None:
        if (
            state.done
            and state is not self._last_audio_response
            and not (state.audio_item_id and state.audio_item_id in self._pending_corrections)
        ):
            self._responses.pop(state.id, None)

    def _handle_audio_delta(self, event: Dict[str, Any]) -> None:
        response_id = event.get("response_id")
        delta = event.get("delta")
        if not isinstance(response_id, str) or not delta:
            return
        state = self._ensure_response(response_id)
        if state.interrupted:
            return

        # The server never reports playback position, so assume back-to-back playback on receipt.
        now = self._now()
        duration_ms = self._audio_duration_ms(delta)
        start_at = max(now, self._playback_ends_at)
        if state.playback_start_at is None:
            state.playback_start_at = start_at
        state.audio_received_ms += duration_ms
        state.audio_item_id = event.get("item_id")
        state.audio_content_index = event.get("content_index") or 0
        self._playback_ends_at = start_at + duration_ms

        previous = self._last_audio_response
        self._last_audio_response = state
        if previous is not None and previous is not state:
            self._release_response(previous)

        self._emit({"type": "audio", "audio_event": {"audio_base_64": delta, "event_id": state.event_id}})

    def _handle_text_delta(self, event: Dict[str, Any]) -> None:
        response_id = event.get("response_id")
        if not isinstance(response_id, str):
            return
        state = self._ensure_response(response_id)
        if state.interrupted or state.done:
            return

        if not state.streaming:
            state.streaming = True
            self._emit_text_part(state, "start", "")
        delta = event.get("delta") or ""
        state.text += delta
        self._emit_text_part(state, "delta", delta)

    def _handle_response_done(self, event: Dict[str, Any]) -> None:
        response = event.get("response") or {}
        response_id = response.get("id")
        if not isinstance(response_id, str):
            return
        state = self._ensure_response(response_id)
        state.done = True
        if self._active_response_id == response_id:
            self._active_response_id = None

        output = response.get("output")
        output = output if isinstance(output, list) else []
        text = _extract_assistant_text(output) or state.text
        reached_client = state.audio_received_ms > 0 or state.text != ""
        if text and (response.get("status") != "cancelled" or reached_client):
            state.agent_response = text
            self._emit(
                {
                    "type": "agent_response",
                    "agent_response_event": {
                        "agent_response": text,
                        "event_id": state.event_id,
                        "response_id": state.id,
                    },
                }
            )
        if state.streaming:
            state.streaming = False
            self._emit_text_part(state, "stop", "")

        if response.get("status") == "failed":
            error = (response.get("status_details") or {}).get("error") or {}
            self._emit_error(error.get("message") or error.get("code") or "The response failed.", error)

        if response.get("status") == "completed":
            for item in output:
                if not isinstance(item, dict) or item.get("type") != "function_call" or not item.get("call_id"):
                    continue
                self._pending_tool_calls.add(item["call_id"])
                self._emit(
                    {
                        "type": "client_tool_call",
                        "client_tool_call": {
                            "tool_name": item.get("name"),
                            "tool_call_id": item["call_id"],
                            "parameters": _parse_tool_arguments(item.get("arguments")),
                            "event_id": state.event_id,
                        },
                    }
                )

        self._send_pending_truncate(state)
        self._release_response(state)

    def _interrupt(self) -> None:
        """Stops playback of the latest response and truncates its server-side item to what was heard."""
        now = self._now()

        # Drop what a not-yet-audible response sends before the server-side cancellation lands.
        if self._active_response_id:
            active = self._responses.get(self._active_response_id)
            if active is not None and active.audio_received_ms == 0:
                active.interrupted = True

        state = self._last_audio_response
        if state is None or state.interrupted:
            return
        is_playing = self._active_response_id == state.id or now < self._playback_ends_at
        if not is_playing:
            return

        state.interrupted = True
        self._playback_ends_at = now
        self._emit({"type": "interruption", "interruption_event": {"event_id": self._next_event_id()}})

        start_at = state.playback_start_at if state.playback_start_at is not None else now
        played_ms = math.floor(min(max(now - start_at, 0), state.audio_received_ms))
        if state.audio_item_id and played_ms < math.floor(state.audio_received_ms):
            state.truncate_at_ms = played_ms
            if state.done:
                self._send_pending_truncate(state)

    def _send_pending_truncate(self, state: _ResponseState) -> None:
        if state.truncate_at_ms is None or not state.audio_item_id:
            return
        audio_end_ms = state.truncate_at_ms
        state.truncate_at_ms = None
        self._pending_corrections[state.audio_item_id] = state
        self._send_internal(
            {
                "type": "conversation.item.truncate",
                "item_id": state.audio_item_id,
                "content_index": state.audio_content_index,
                "audio_end_ms": audio_end_ms,
            }
        )

    def _handle_item_retrieved(self, event: Dict[str, Any]) -> None:
        item = event.get("item") or {}
        state = self._pending_corrections.pop(str(item.get("id")), None)
        if state is None:
            return

        corrected = _extract_assistant_text([item])
        original = state.agent_response
        if original is not None and corrected != original:
            self._emit(
                {
                    "type": "agent_response_correction",
                    "agent_response_correction_event": {
                        "original_agent_response": original,
                        "corrected_agent_response": corrected,
                        "event_id": state.event_id,
                        "response_id": state.id,
                    },
                }
            )
        self._release_response(state)

    def _handle_error(self, event: Dict[str, Any]) -> None:
        error = event.get("error") or {}
        if error.get("event_id") in self._internal_event_ids:
            # Errors from SDK-initiated requests don't affect the conversation.
            logger.debug("Realtime request sent by the SDK failed: %s", error)
            return
        self._emit_error(error.get("message") or "Unknown error", error)

    def _emit_error(self, message: str, error: Dict[str, Any]) -> None:
        self._emit(
            {
                "type": "error",
                "error_event": {
                    "code": 1008 if error.get("type") == "invalid_request_error" else 1011,
                    "message": message,
                    "error_type": "unknown",
                    "details": {
                        "type": error.get("type"),
                        "code": error.get("code"),
                        "param": error.get("param"),
                        "event_id": error.get("event_id"),
                    },
                },
            }
        )

    def _emit_vad_score(self, vad_score: int) -> None:
        self._emit({"type": "vad_score", "vad_score_event": {"vad_score": vad_score}})

    def _emit_text_part(self, state: _ResponseState, part_type: str, text: str) -> None:
        self._emit(
            {
                "type": "agent_chat_response_part",
                "text_response_part": {
                    "text": text,
                    "type": part_type,
                    "event_id": state.event_id,
                    "response_id": state.id,
                },
            }
        )

    def _emit(self, event: Dict[str, Any]) -> None:
        self._out.events.append(event)

    def _send(self, event: Dict[str, Any]) -> None:
        self._out.sends.append(event)

    def _send_internal(self, event: Dict[str, Any]) -> None:
        self._internal_event_count += 1
        event_id = f"sdk_{self._internal_event_count}"
        self._internal_event_ids.add(event_id)
        self._send({**event, "event_id": event_id})

    def _audio_duration_ms(self, delta: str) -> float:
        padding = 2 if delta.endswith("==") else 1 if delta.endswith("=") else 0
        num_bytes = (len(delta) * 3) // 4 - padding
        bytes_per_sample = 1 if self._output_format.encoding == "ulaw" else 2
        return num_bytes / bytes_per_sample / self._output_format.sample_rate * 1000


class RealtimeAudioConverter:
    """Converts between the audio interface format (16-bit PCM mono at 16kHz) and the session's wire formats."""

    def __init__(self, input_format: RealtimeWireFormat, output_format: RealtimeWireFormat):
        self._input_format = input_format
        self._output_format = output_format
        self._input_stream = _Pcm16Stream()
        self._output_stream = _Pcm16Stream()
        self._input_resampler = _LinearResampler(AUDIO_INTERFACE_SAMPLE_RATE, input_format.sample_rate)
        self._output_resampler = _LinearResampler(output_format.sample_rate, AUDIO_INTERFACE_SAMPLE_RATE)

    def encode_input(self, audio: bytes) -> bytes:
        samples = self._input_resampler.process(self._input_stream.samples(audio))
        if self._input_format.encoding == "ulaw":
            return bytes(_ulaw_encode(sample) for sample in samples)
        return _pack_pcm16(samples)

    def decode_output(self, audio: bytes) -> bytes:
        if self._output_format.encoding == "ulaw":
            samples: Sequence[int] = [_ULAW_DECODE_TABLE[byte] for byte in audio]
        else:
            samples = self._output_stream.samples(audio)
        return _pack_pcm16(self._output_resampler.process(samples))


class _Pcm16Stream:
    """Splits a byte stream into little-endian 16-bit samples, carrying odd bytes into the next chunk."""

    def __init__(self) -> None:
        self._remainder = b""

    def samples(self, data: bytes) -> "array.array[int]":
        data = self._remainder + data
        usable = len(data) - len(data) % 2
        self._remainder = data[usable:]
        samples = array.array("h")
        samples.frombytes(data[:usable])
        if sys.byteorder == "big":
            samples.byteswap()
        return samples


def _pack_pcm16(samples: Sequence[int]) -> bytes:
    packed = array.array("h", samples)
    if sys.byteorder == "big":
        packed.byteswap()
    return packed.tobytes()


class _LinearResampler:
    """Streaming linear-interpolation resampler for 16-bit samples.

    Downsampling applies a [1, 2, 1] low-pass first to limit aliasing.
    """

    def __init__(self, source_rate: int, target_rate: int):
        divisor = math.gcd(source_rate, target_rate)
        self._source_step = source_rate // divisor
        self._target_step = target_rate // divisor
        self._low_pass = target_rate < source_rate
        self._history = [0, 0]
        self._previous: Optional[int] = None
        # Position of the next output sample in source samples, scaled by `_target_step`,
        # relative to `_previous`.
        self._position = 0

    def process(self, samples: Sequence[int]) -> List[int]:
        if self._source_step == self._target_step:
            return list(samples)
        if self._low_pass:
            samples = self._filter(samples)

        buffer = list(samples) if self._previous is None else [self._previous, *samples]
        if not buffer:
            return []
        source_step, target_step = self._source_step, self._target_step
        end = (len(buffer) - 1) * target_step
        position = self._position
        result = []
        while position < end:
            index, fraction = divmod(position, target_step)
            result.append((buffer[index] * (target_step - fraction) + buffer[index + 1] * fraction) // target_step)
            position += source_step
        self._position = position - end
        self._previous = buffer[-1]
        return result

    def _filter(self, samples: Sequence[int]) -> List[int]:
        before, last = self._history
        filtered = []
        for sample in samples:
            filtered.append((before + 2 * last + sample) >> 2)
            before, last = last, sample
        self._history = [before, last]
        return filtered


_ULAW_BIAS = 0x84
_ULAW_CLIP = 32635


def _ulaw_encode(sample: int) -> int:
    sign = 0x80 if sample < 0 else 0
    magnitude = min(-sample if sign else sample, _ULAW_CLIP) + _ULAW_BIAS
    exponent = max((magnitude >> 7).bit_length() - 1, 0)
    mantissa = (magnitude >> (exponent + 3)) & 0x0F
    return ~(sign | (exponent << 4) | mantissa) & 0xFF


def _ulaw_decode(byte: int) -> int:
    byte = ~byte & 0xFF
    exponent = (byte >> 4) & 0x07
    magnitude = ((((byte & 0x0F) << 3) + _ULAW_BIAS) << exponent) - _ULAW_BIAS
    return -magnitude if byte & 0x80 else magnitude


_ULAW_DECODE_TABLE = [_ulaw_decode(byte) for byte in range(256)]


def _to_wire_audio_format(audio_format: RealtimeAudioFormat) -> Dict[str, Any]:
    if audio_format == "ulaw_8000":
        return {"type": "audio/pcmu"}
    return {"type": "audio/pcm", "rate": 24000}


def _from_wire_audio_format(wire_format: Optional[Dict[str, Any]], fallback: RealtimeAudioFormat) -> RealtimeWireFormat:
    if not wire_format:
        return RealtimeWireFormat("ulaw", 8000) if fallback == "ulaw_8000" else RealtimeWireFormat("pcm", 24000)
    if wire_format.get("type") == "audio/pcm":
        return RealtimeWireFormat("pcm", int(wire_format.get("rate") or 24000))
    if wire_format.get("type") == "audio/pcmu":
        return RealtimeWireFormat("ulaw", 8000)
    raise RealtimeConnectionError(
        f"The Realtime endpoint selected an unsupported audio format: {wire_format.get('type')}"
    )


def _omit_none(value: Dict[str, Any]) -> Dict[str, Any]:
    return {key: entry for key, entry in value.items() if entry is not None}


def _tool_output(result: Any) -> str:
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    try:
        return json.dumps(result)
    except (TypeError, ValueError):
        return str(result)


def _extract_assistant_text(items: List[Any]) -> str:
    text = ""
    for item in items:
        if not isinstance(item, dict) or item.get("type") != "message" or item.get("role") != "assistant":
            continue
        content = item.get("content")
        for part in content if isinstance(content, list) else []:
            if isinstance(part, dict):
                text += part.get("transcript") or part.get("text") or ""
    return text


def _parse_tool_arguments(arguments: Any) -> Dict[str, Any]:
    if not isinstance(arguments, str) or arguments == "":
        return {}
    try:
        parsed = json.loads(arguments)
    except ValueError:
        return {}
    return parsed if isinstance(parsed, dict) else {}
