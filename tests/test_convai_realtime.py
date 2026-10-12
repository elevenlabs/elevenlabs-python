import asyncio
import base64
import json
import math
import threading
import time
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from websockets.exceptions import ConnectionClosedError
from websockets.frames import Close

from elevenlabs.conversational_ai.conversation import (
    AsyncAudioInterface,
    AsyncConversation,
    AudioInterface,
    ClientTools,
    Conversation,
    ConversationInitiationData,
    RealtimeConnectionError,
    RealtimeFunctionTool,
    RealtimeSessionOptions,
    RealtimeTurnDetection,
    RealtimeUnsupportedFeatureError,
)
from elevenlabs.conversational_ai.realtime_protocol import (
    RealtimeAudioConverter,
    RealtimeProtocolTranslator,
    RealtimeWireFormat,
    build_session_update,
)

PCM_24K = RealtimeWireFormat("pcm", 24000)
ULAW_8K = RealtimeWireFormat("ulaw", 8000)
PCM_24K_BYTES_PER_MS = 48

EFFECTIVE_SESSION = {
    "type": "realtime",
    "id": "sess_123",
    "audio": {
        "input": {
            "format": {"type": "audio/pcm", "rate": 24000},
            "turn_detection": {"type": "semantic_vad", "interrupt_response": True},
        },
        "output": {"format": {"type": "audio/pcm", "rate": 24000}, "voice": "marin"},
    },
}


def pcm_chunk(duration_ms: int) -> str:
    return base64.b64encode(bytes(duration_ms * PCM_24K_BYTES_PER_MS)).decode()


def assistant_message(item_id: str, transcript: str) -> Dict[str, Any]:
    return {
        "id": item_id,
        "type": "message",
        "role": "assistant",
        "content": [{"type": "output_audio", "transcript": transcript}],
    }


class TranslatorHarness:
    def __init__(self, interrupt_on_speech: bool = True):
        self.now = 10_000.0
        self.emitted: List[Dict[str, Any]] = []
        self.sent: List[Dict[str, Any]] = []
        self.translator = RealtimeProtocolTranslator(
            output_format=PCM_24K, interrupt_on_speech=interrupt_on_speech, now=lambda: self.now
        )

    def server(self, event: Dict[str, Any]) -> None:
        translation = self.translator.handle_server_event(event)
        self.emitted.extend(translation.events)
        self.sent.extend(translation.sends)

    def outgoing(self, message: Dict[str, Any]) -> None:
        translation = self.translator.handle_outgoing_event(message)
        self.emitted.extend(translation.events)
        self.sent.extend(translation.sends)

    def start_response(self, response_id: str) -> None:
        self.server({"type": "response.created", "response": {"id": response_id, "status": "in_progress"}})

    def audio_delta(self, response_id: str, item_id: str, duration_ms: int) -> None:
        self.server(
            {
                "type": "response.output_audio.delta",
                "response_id": response_id,
                "item_id": item_id,
                "content_index": 0,
                "delta": pcm_chunk(duration_ms),
            }
        )

    def finish_response(self, response_id: str, status: str, output=None) -> None:
        self.server({"type": "response.done", "response": {"id": response_id, "status": status, "output": output or []}})

    def speech_started(self) -> None:
        self.server({"type": "input_audio_buffer.speech_started", "audio_start_ms": 0, "item_id": "user_1"})

    def types(self) -> List[str]:
        return [event["type"] for event in self.emitted]


class TestTranslatorAgentTurns:
    def test_streams_text_audio_and_final_response_in_native_order(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.server({"type": "response.output_audio_transcript.delta", "response_id": "resp_1", "delta": "Hello"})
        h.audio_delta("resp_1", "item_1", 100)
        h.server({"type": "response.output_audio_transcript.delta", "response_id": "resp_1", "delta": " there"})
        h.finish_response("resp_1", "completed", [assistant_message("item_1", "Hello there")])

        assert h.types() == [
            "agent_chat_response_part",
            "agent_chat_response_part",
            "audio",
            "agent_chat_response_part",
            "agent_response",
            "agent_chat_response_part",
        ]
        assert h.emitted[0]["text_response_part"] == {
            "text": "",
            "type": "start",
            "event_id": 1,
            "response_id": "resp_1",
        }
        assert h.emitted[2] == {"type": "audio", "audio_event": {"audio_base_64": pcm_chunk(100), "event_id": 1}}
        assert h.emitted[4]["agent_response_event"] == {
            "agent_response": "Hello there",
            "event_id": 1,
            "response_id": "resp_1",
        }
        assert h.emitted[5]["text_response_part"]["type"] == "stop"

    def test_reports_failed_responses_as_errors(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.server(
            {
                "type": "response.done",
                "response": {
                    "id": "resp_1",
                    "status": "failed",
                    "status_details": {"error": {"type": "server_error", "message": "Model overloaded"}},
                },
            }
        )
        assert h.emitted[-1]["type"] == "error"
        assert h.emitted[-1]["error_event"]["message"] == "Model overloaded"
        assert h.emitted[-1]["error_event"]["code"] == 1011

    def test_maps_speech_start_and_stop_to_vad_scores(self):
        h = TranslatorHarness()
        h.speech_started()
        h.server({"type": "input_audio_buffer.speech_stopped"})
        assert [e["vad_score_event"]["vad_score"] for e in h.emitted] == [1, 0]

    def test_user_transcripts(self):
        h = TranslatorHarness()
        h.server({"type": "conversation.item.input_audio_transcription.completed", "transcript": "Hi there"})
        assert h.emitted == [
            {"type": "user_transcript", "user_transcription_event": {"user_transcript": "Hi there", "event_id": 1}}
        ]


class TestTranslatorInterruptions:
    def test_interrupts_playback_and_truncates_to_the_audio_the_user_heard(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.audio_delta("resp_1", "item_1", 1000)
        h.audio_delta("resp_1", "item_1", 1000)
        h.finish_response("resp_1", "completed", [assistant_message("item_1", "A long answer that keeps going")])

        h.now += 700
        h.speech_started()

        assert {"type": "interruption", "interruption_event": {"event_id": 2}} in h.emitted
        assert h.sent == [
            {
                "type": "conversation.item.truncate",
                "item_id": "item_1",
                "content_index": 0,
                "audio_end_ms": 700,
                "event_id": "sdk_1",
            }
        ]

        h.server({"type": "conversation.item.truncated", "item_id": "item_1", "content_index": 0, "audio_end_ms": 700})
        assert h.sent[1] == {"type": "conversation.item.retrieve", "item_id": "item_1", "event_id": "sdk_2"}

        h.server({"type": "conversation.item.retrieved", "item": assistant_message("item_1", "A long answer")})
        assert h.emitted[-1] == {
            "type": "agent_response_correction",
            "agent_response_correction_event": {
                "original_agent_response": "A long answer that keeps going",
                "corrected_agent_response": "A long answer",
                "event_id": 1,
                "response_id": "resp_1",
            },
        }

    def test_defers_truncation_until_the_interrupted_response_is_done(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.audio_delta("resp_1", "item_1", 1000)
        h.now += 300
        h.speech_started()
        assert "interruption" in h.types()
        assert h.sent == []

        h.audio_delta("resp_1", "item_1", 1000)
        assert h.types().count("audio") == 1

        h.finish_response("resp_1", "cancelled", [assistant_message("item_1", "Partial")])
        assert len(h.sent) == 1
        assert h.sent[0]["type"] == "conversation.item.truncate"
        assert h.sent[0]["audio_end_ms"] == 300

    def test_does_not_interrupt_once_playback_has_finished(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.audio_delta("resp_1", "item_1", 500)
        h.finish_response("resp_1", "completed", [assistant_message("item_1", "Hi")])
        h.now += 600
        h.speech_started()
        assert "interruption" not in h.types()
        assert h.sent == []

    def test_keeps_playing_when_interrupt_response_is_disabled(self):
        h = TranslatorHarness(interrupt_on_speech=False)
        h.start_response("resp_1")
        h.audio_delta("resp_1", "item_1", 1000)
        h.now += 100
        h.speech_started()
        assert "interruption" not in h.types()

    def test_gives_the_next_response_an_event_id_above_the_interruption(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.audio_delta("resp_1", "item_1", 1000)
        h.now += 100
        h.speech_started()
        h.finish_response("resp_1", "cancelled")
        h.start_response("resp_2")
        h.audio_delta("resp_2", "item_2", 100)

        interruption = next(e for e in h.emitted if e["type"] == "interruption")
        audio = [e for e in h.emitted if e["type"] == "audio"][-1]
        assert interruption["interruption_event"]["event_id"] == 2
        assert audio["audio_event"]["event_id"] == 3

    def test_ignores_errors_caused_by_its_own_requests(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.audio_delta("resp_1", "item_1", 1000)
        h.finish_response("resp_1", "completed", [assistant_message("item_1", "Hi")])
        h.now += 100
        h.speech_started()
        h.emitted = []

        h.server(
            {
                "type": "error",
                "error": {"type": "invalid_request_error", "message": "out of range", "event_id": "sdk_1"},
            }
        )
        assert h.emitted == []

    def test_reports_other_errors(self):
        h = TranslatorHarness()
        h.server({"type": "error", "error": {"type": "invalid_request_error", "message": "Bad tool"}})
        assert h.emitted[0]["error_event"]["code"] == 1008
        assert h.emitted[0]["error_event"]["message"] == "Bad tool"


class TestTranslatorClientTools:
    def test_calls_tools_from_completed_responses_and_resumes_once_all_results_are_in(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.finish_response(
            "resp_1",
            "completed",
            [
                {"type": "function_call", "call_id": "call_1", "name": "get_weather", "arguments": '{"city":"Paris"}'},
                {"type": "function_call", "call_id": "call_2", "name": "get_time", "arguments": ""},
            ],
        )
        assert h.emitted == [
            {
                "type": "client_tool_call",
                "client_tool_call": {
                    "tool_name": "get_weather",
                    "tool_call_id": "call_1",
                    "parameters": {"city": "Paris"},
                    "event_id": 1,
                },
            },
            {
                "type": "client_tool_call",
                "client_tool_call": {"tool_name": "get_time", "tool_call_id": "call_2", "parameters": {}, "event_id": 1},
            },
        ]

        h.outgoing({"type": "client_tool_result", "tool_call_id": "call_1", "result": "Sunny", "is_error": False})
        assert h.sent == [
            {
                "type": "conversation.item.create",
                "item": {"type": "function_call_output", "call_id": "call_1", "output": "Sunny"},
            }
        ]

        h.outgoing({"type": "client_tool_result", "tool_call_id": "call_2", "result": {"time": "noon"}})
        assert h.sent[1:] == [
            {
                "type": "conversation.item.create",
                "item": {"type": "function_call_output", "call_id": "call_2", "output": '{"time": "noon"}'},
            },
            {"type": "response.create"},
        ]

    def test_does_not_call_tools_from_responses_that_did_not_complete(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.finish_response(
            "resp_1", "cancelled", [{"type": "function_call", "call_id": "call_1", "name": "x", "arguments": "{}"}]
        )
        assert "client_tool_call" not in h.types()


class TestTranslatorOutgoingEvents:
    def test_appends_user_audio_to_the_input_buffer(self):
        h = TranslatorHarness()
        h.outgoing({"user_audio_chunk": "AAAA"})
        assert h.sent == [{"type": "input_audio_buffer.append", "audio": "AAAA"}]

    def test_sends_user_messages_and_requests_a_response(self):
        h = TranslatorHarness()
        h.outgoing({"type": "user_message", "text": "Hi"})
        assert h.sent == [
            {
                "type": "conversation.item.create",
                "item": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "Hi"}]},
            },
            {"type": "response.create"},
        ]

    def test_cancels_the_active_response_before_sending_a_user_message(self):
        h = TranslatorHarness()
        h.start_response("resp_1")
        h.audio_delta("resp_1", "item_1", 1000)
        h.outgoing({"type": "user_message", "text": "Stop"})
        assert "interruption" in h.types()
        assert [e["type"] for e in h.sent] == ["response.cancel", "conversation.item.create", "response.create"]

    def test_drops_events_that_need_no_wire_equivalent(self):
        h = TranslatorHarness()
        h.outgoing({"type": "pong", "event_id": 1})
        h.outgoing({"type": "user_activity"})
        assert h.sent == []

    @pytest.mark.parametrize(
        "message",
        [
            {"type": "contextual_update", "text": "The user is on the pricing page"},
            {"type": "feedback", "feedback": "like"},
            {"type": "multimodal_message", "text": {"type": "user_message", "text": "x"}},
        ],
    )
    def test_rejects_unsupported_events(self, message):
        h = TranslatorHarness()
        with pytest.raises(RealtimeUnsupportedFeatureError):
            h.outgoing(message)
        assert h.sent == []


class TestSessionUpdate:
    def test_defaults(self):
        assert build_session_update(RealtimeSessionOptions(), text_only=False) == {
            "type": "session.update",
            "session": {
                "type": "realtime",
                "output_modalities": ["audio"],
                "audio": {
                    "input": {"format": {"type": "audio/pcm", "rate": 24000}},
                    "output": {"format": {"type": "audio/pcm", "rate": 24000}},
                },
            },
        }

    def test_full_options(self):
        options = RealtimeSessionOptions(
            instructions="Be brief.",
            voice="marin",
            input_audio_format="ulaw_8000",
            output_audio_format="ulaw_8000",
            turn_detection=RealtimeTurnDetection(eagerness="high", interrupt_response=False),
            tools=[RealtimeFunctionTool(name="get_weather", description="Weather", parameters={"type": "object"})],
            temperature=0.7,
            max_output_tokens="inf",
        )
        session = build_session_update(options, text_only=True)["session"]
        assert session == {
            "type": "realtime",
            "output_modalities": ["text"],
            "instructions": "Be brief.",
            "audio": {
                "input": {
                    "format": {"type": "audio/pcmu"},
                    "turn_detection": {"type": "semantic_vad", "eagerness": "high", "interrupt_response": False},
                },
                "output": {"format": {"type": "audio/pcmu"}, "voice": "marin"},
            },
            "tools": [
                {"type": "function", "name": "get_weather", "description": "Weather", "parameters": {"type": "object"}}
            ],
            "temperature": 0.7,
            "max_output_tokens": "inf",
        }

    def test_none_turn_detection_disables_it(self):
        session = build_session_update(RealtimeSessionOptions(turn_detection=None), text_only=False)["session"]
        assert session["audio"]["input"]["turn_detection"] is None


class TestAudioConverter:
    def test_pcm_round_trip_resamples_between_16k_and_24k(self):
        converter = RealtimeAudioConverter(PCM_24K, PCM_24K)
        one_second_16k = bytes(16000 * 2)
        wire = converter.encode_input(one_second_16k)
        assert abs(len(wire) // 2 - 24000) <= 2

        back = converter.decode_output(bytes(24000 * 2))
        assert abs(len(back) // 2 - 16000) <= 2

    def test_streaming_resampling_matches_one_shot(self):
        samples = [int(10000 * math.sin(2 * math.pi * 440 * n / 16000)) for n in range(1600)]
        pcm = b"".join(s.to_bytes(2, "little", signed=True) for s in samples)

        one_shot = RealtimeAudioConverter(PCM_24K, PCM_24K).encode_input(pcm)
        chunked_converter = RealtimeAudioConverter(PCM_24K, PCM_24K)
        chunked = b"".join(chunked_converter.encode_input(pcm[i : i + 333]) for i in range(0, len(pcm), 333))
        assert chunked == one_shot

    def test_ulaw_round_trip(self):
        samples = [0, 1000, -1000, 8000, -8000, 32000, -32000]
        pcm_8k = b"".join(s.to_bytes(2, "little", signed=True) for s in samples)
        converter = RealtimeAudioConverter(ULAW_8K, ULAW_8K)
        from elevenlabs.conversational_ai.realtime_protocol import _ULAW_DECODE_TABLE, _ulaw_encode

        decoded = [_ULAW_DECODE_TABLE[_ulaw_encode(s)] for s in samples]
        for original, roundtrip in zip(samples, decoded):
            assert abs(original - roundtrip) <= max(abs(original) // 16, 8)
        assert len(converter.encode_input(pcm_8k * 2)) == len(samples)


class TestValidation:
    def make(self, **kwargs):
        defaults: Dict[str, Any] = dict(
            client=MagicMock(), connection_type="websocket-realtime", client_secret="ek_test", client_tools=MagicMock()
        )
        defaults.update(kwargs)
        return Conversation(**defaults)

    def test_requires_client_secret(self):
        with pytest.raises(ValueError, match="client_secret"):
            self.make(client_secret=None)

    def test_rejects_agent_options(self):
        with pytest.raises(ValueError, match="agent_id, user_id, requires_auth, environment, config"):
            self.make(
                agent_id="agent",
                user_id="user",
                requires_auth=True,
                environment="staging",
                config=ConversationInitiationData(dynamic_variables={"a": 1}),
            )

    def test_rejects_unsupported_session_options(self):
        with pytest.raises(ValueError, match="audio format"):
            self.make(realtime=RealtimeSessionOptions(output_audio_format="pcm_16000"))  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="Duplicate"):
            self.make(realtime=RealtimeSessionOptions(tools=[RealtimeFunctionTool("a"), RealtimeFunctionTool("a")]))

    def test_websocket_rejects_realtime_options(self):
        with pytest.raises(ValueError, match="only apply to websocket-realtime"):
            Conversation(client=MagicMock(), agent_id="agent", client_secret="ek_test", client_tools=MagicMock())

    def test_websocket_requires_agent_id(self):
        with pytest.raises(ValueError, match="agent_id is required"):
            Conversation(client=MagicMock(), client_tools=MagicMock())


class RecordingAudioInterface(AudioInterface):
    def __init__(self):
        self.output_chunks: List[bytes] = []
        self.interrupts = 0
        self.input_callback = None

    def start(self, input_callback):
        self.input_callback = input_callback

    def stop(self):
        pass

    def output(self, audio):
        self.output_chunks.append(audio)

    def interrupt(self):
        self.interrupts += 1


class FakeSyncRealtimeSocket:
    """Plays the server side of the Realtime handshake, then a scripted conversation."""

    def __init__(self, script: List[Dict[str, Any]]):
        self.sent: List[Dict[str, Any]] = []
        self.closed = False
        self._incoming: List[str] = [json.dumps({"type": "session.created", "session": {"id": "sess_123"}})]
        self._script = script
        self._lock = threading.Condition()

    def send(self, data: str):
        message = json.loads(data)
        with self._lock:
            self.sent.append(message)
            if message.get("type") == "session.update":
                self._incoming.append(json.dumps({"type": "session.updated", "session": EFFECTIVE_SESSION}))
            elif message.get("type") == "response.create":
                self._incoming.extend(json.dumps(event) for event in self._script)
                self._script = []
            self._lock.notify_all()

    def recv(self, timeout=None):
        with self._lock:
            if not self._incoming:
                self._lock.wait(timeout)
            if not self._incoming:
                raise TimeoutError()
            return self._incoming.pop(0)

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def make_client(base_url="https://api.elevenlabs.io"):
    client = MagicMock()
    client._client_wrapper.get_base_url.return_value = base_url
    return client


def wait_until(predicate, timeout=5.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("Timed out waiting for condition")


AGENT_TURN_SCRIPT = [
    {"type": "response.created", "response": {"id": "resp_1"}},
    {"type": "response.output_audio_transcript.delta", "response_id": "resp_1", "delta": "Hello"},
    {
        "type": "response.output_audio.delta",
        "response_id": "resp_1",
        "item_id": "item_1",
        "content_index": 0,
        "delta": pcm_chunk(100),
    },
    {
        "type": "response.done",
        "response": {"id": "resp_1", "status": "completed", "output": [assistant_message("item_1", "Hello")]},
    },
]


def test_sync_realtime_conversation_end_to_end():
    socket = FakeSyncRealtimeSocket(AGENT_TURN_SCRIPT)
    client = MagicMock()
    client._client_wrapper.get_base_url.return_value = "https://api.eu.residency.elevenlabs.io"
    audio = RecordingAudioInterface()
    agent_responses: List[str] = []
    parts: List[str] = []

    conversation = Conversation(
        client,
        connection_type="websocket-realtime",
        client_secret="ek_test",
        realtime=RealtimeSessionOptions(instructions="Be brief.", voice="marin"),
        audio_interface=audio,
        callback_agent_response=agent_responses.append,
        callback_agent_chat_response_part=lambda text, part: parts.append(part.value),
    )

    with patch("elevenlabs.conversational_ai.conversation.connect", return_value=socket) as mock_connect:
        conversation.start_session()

        url = mock_connect.call_args.args[0]
        assert url.startswith("wss://api.eu.residency.elevenlabs.io/v1/convai/realtime?source=python_sdk&version=")
        assert mock_connect.call_args.kwargs["subprotocols"] == ["realtime", "openai-insecure-api-key.ek_test"]
        assert socket.sent[0]["type"] == "session.update"
        assert socket.sent[0]["session"]["instructions"] == "Be brief."
        assert socket.sent[0]["session"]["output_modalities"] == ["audio"]
        assert conversation._conversation_id == "sess_123"

        audio.input_callback(bytes(16000 * 2 // 10))  # 100 ms at 16 kHz
        conversation.send_user_message("Hi")
        wait_until(lambda: agent_responses == ["Hello"])

        with pytest.raises(RealtimeUnsupportedFeatureError):
            conversation.send_contextual_update("context")

        conversation.end_session()
        assert conversation.wait_for_session_end() == "sess_123"

    sent_types = [message["type"] for message in socket.sent]
    assert sent_types[:2] == ["session.update", "input_audio_buffer.append"]
    assert sent_types[2:] == ["conversation.item.create", "response.create"]
    appended = base64.b64decode(socket.sent[1]["audio"])
    assert abs(len(appended) // 2 - 2400) <= 2  # resampled to 24 kHz

    assert parts == ["start", "delta", "stop"]
    assert len(audio.output_chunks) == 1
    assert abs(len(audio.output_chunks[0]) // 2 - 1600) <= 2  # resampled to 16 kHz
    assert socket.closed


def test_sync_realtime_client_tools_round_trip():
    script = [
        {"type": "response.created", "response": {"id": "resp_1"}},
        {
            "type": "response.done",
            "response": {
                "id": "resp_1",
                "status": "completed",
                "output": [
                    {"type": "function_call", "call_id": "call_1", "name": "get_weather", "arguments": '{"city":"Paris"}'}
                ],
            },
        },
    ]
    socket = FakeSyncRealtimeSocket(script)
    client_tools = ClientTools()
    calls: List[Dict[str, Any]] = []

    def get_weather(parameters):
        calls.append(parameters)
        return "Sunny"

    client_tools.register("get_weather", get_weather)
    conversation = Conversation(
        make_client(),
        connection_type="websocket-realtime",
        client_secret="ek_test",
        realtime=RealtimeSessionOptions(tools=[RealtimeFunctionTool(name="get_weather")]),
        client_tools=client_tools,
    )

    with patch("elevenlabs.conversational_ai.conversation.connect", return_value=socket):
        conversation.start_session()
        assert socket.sent[0]["session"]["output_modalities"] == ["text"]
        conversation.send_user_message("Weather in Paris?")
        wait_until(lambda: [m["type"] for m in socket.sent][-1:] == ["response.create"] and len(socket.sent) == 5)
        conversation.end_session()
        conversation.wait_for_session_end()

    assert calls == [{"tool_call_id": "call_1", "city": "Paris"}]
    assert socket.sent[3] == {
        "type": "conversation.item.create",
        "item": {"type": "function_call_output", "call_id": "call_1", "output": "Sunny"},
    }
    assert socket.sent[4] == {"type": "response.create"}


def test_sync_realtime_handshake_reports_disabled_workspace():
    socket = MagicMock()
    socket.recv.side_effect = ConnectionClosedError(Close(4003, ""), None)
    conversation = Conversation(
        make_client(), connection_type="websocket-realtime", client_secret="ek_test", client_tools=MagicMock()
    )

    with patch("elevenlabs.conversational_ai.conversation.connect", return_value=socket):
        with pytest.raises(RealtimeConnectionError, match="not enabled for this workspace") as error:
            conversation.start_session()

    assert error.value.close_code == 4003
    socket.close.assert_called_once()


def test_sync_realtime_handshake_reports_session_errors():
    socket = MagicMock()
    socket.recv.side_effect = [
        json.dumps({"type": "session.created", "session": {"id": "sess_1"}}),
        json.dumps({"type": "error", "error": {"message": "Unknown voice"}}),
    ]
    conversation = Conversation(
        make_client(), connection_type="websocket-realtime", client_secret="ek_test", client_tools=MagicMock()
    )

    with patch("elevenlabs.conversational_ai.conversation.connect", return_value=socket):
        with pytest.raises(RealtimeConnectionError, match="Unknown voice"):
            conversation.start_session()
    socket.close.assert_called_once()


class RecordingAsyncAudioInterface(AsyncAudioInterface):
    def __init__(self):
        self.output_chunks: List[bytes] = []
        self.input_callback = None

    async def start(self, input_callback):
        self.input_callback = input_callback

    async def stop(self):
        pass

    async def output(self, audio):
        self.output_chunks.append(audio)

    async def interrupt(self):
        pass


class FakeAsyncRealtimeSocket:
    def __init__(self, script: List[Dict[str, Any]]):
        self.sent: List[Dict[str, Any]] = []
        self.closed = False
        self._incoming: asyncio.Queue = asyncio.Queue()
        self._incoming.put_nowait(json.dumps({"type": "session.created", "session": {"id": "sess_123"}}))
        self._script = script

    async def send(self, data: str):
        message = json.loads(data)
        self.sent.append(message)
        if message.get("type") == "session.update":
            self._incoming.put_nowait(json.dumps({"type": "session.updated", "session": EFFECTIVE_SESSION}))
        elif message.get("type") == "response.create":
            for event in self._script:
                self._incoming.put_nowait(json.dumps(event))
            self._script = []

    async def recv(self):
        return await self._incoming.get()

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_async_realtime_conversation_end_to_end():
    socket = FakeAsyncRealtimeSocket(AGENT_TURN_SCRIPT)
    client = MagicMock()
    client._client_wrapper.get_base_url.return_value = "https://api.elevenlabs.io"
    audio = RecordingAsyncAudioInterface()
    agent_response = AsyncMock()

    conversation = AsyncConversation(
        client,
        connection_type="websocket-realtime",
        client_secret="ek_test",
        audio_interface=audio,
        callback_agent_response=agent_response,
    )

    connect = AsyncMock(return_value=socket)
    with patch("elevenlabs.conversational_ai.conversation.websockets.connect", connect):
        await conversation.start_session()
        assert connect.call_args.kwargs["subprotocols"] == ["realtime", "openai-insecure-api-key.ek_test"]
        assert conversation._conversation_id == "sess_123"

        await asyncio.sleep(0)  # The audio interface starts in the session task.
        await audio.input_callback(bytes(3200))
        await conversation.send_user_message("Hi")
        for _ in range(100):
            if agent_response.await_count:
                break
            await asyncio.sleep(0.01)

        with pytest.raises(RealtimeUnsupportedFeatureError):
            await conversation.send_multimodal_message(text="x")

        await conversation.end_session()
        assert await conversation.wait_for_session_end() == "sess_123"

    agent_response.assert_awaited_once_with("Hello")
    assert [m["type"] for m in socket.sent] == [
        "session.update",
        "input_audio_buffer.append",
        "conversation.item.create",
        "response.create",
    ]
    assert len(audio.output_chunks) == 1
    assert socket.closed
