from abc import ABC, abstractmethod
import base64
import json
import threading
from typing import Callable, Optional

from websockets.sync.client import connect

from ..base_client import BaseElevenLabs


class AudioInterface(ABC):
    """AudioInterface provides an abstraction for handling audio input and output."""

    @abstractmethod
    def start(self, input_callback: Callable[[bytes], None]):
        """Starts the audio interface.

        Called one time before the conversation starts.
        The `input_callback` should be called regularly with input audio chunks from
        the user. The audio should be in 16-bit PCM mono format at 16kHz. Recommended
        chunk size is 4000 samples (250 milliseconds).
        """
        pass

    @abstractmethod
    def stop(self):
        """Stops the audio interface.

        Called one time after the conversation ends. Should clean up any resources
        used by the audio interface and stop any audio streams. Do not call the
        `input_callback` from `start` after this method is called.
        """
        pass

    @abstractmethod
    def output(self, audio: bytes):
        """Output audio to the user.

        The `audio` input is in 16-bit PCM mono format at 16kHz. Implementations can
        choose to do additional buffering. This method should return quickly and not
        block the calling thread.
        """
        pass

    @abstractmethod
    def interrupt(self):
        """Interruption signal to stop any audio output.

        User has interrupted the agent and all previosly buffered audio output should
        be stopped.
        """
        pass

class ConversationConfig:
    """Configuration options for the Conversation."""
    def __init__(
        self,
        extra_body: Optional[dict] = None,
        conversation_config_override: Optional[dict] = None,
    ):
        self.extra_body = extra_body or {}
        self.conversation_config_override = conversation_config_override or {}
        
class Conversation:
    client: BaseElevenLabs
    agent_id: str
    requires_auth: bool
    config: ConversationConfig
    audio_interface: AudioInterface
    callback_agent_response: Optional[Callable[[str], None]]
    callback_agent_response_correction: Optional[Callable[[str, str], None]]
    callback_user_transcript: Optional[Callable[[str], None]]
    callback_latency_measurement: Optional[Callable[[int], None]]

    _thread: Optional[threading.Thread]
    _should_stop: threading.Event
    _conversation_id: Optional[str]
    _last_interrupt_id: int

    def __init__(
        self,
        client: BaseElevenLabs,
        agent_id: str,
        *,
        requires_auth: bool,
        audio_interface: AudioInterface,
        config: Optional[ConversationConfig] = None,
        
        callback_agent_response: Optional[Callable[[str], None]] = None,
        callback_agent_response_correction: Optional[Callable[[str, str], None]] = None,
        callback_user_transcript: Optional[Callable[[str], None]] = None,
        callback_latency_measurement: Optional[Callable[[int], None]] = None,
    ):
        """Conversational AI session.

        BETA: This API is subject to change without regard to backwards compatibility.

        Args:
            client: The ElevenLabs client to use for the conversation.
            agent_id: The ID of the agent to converse with.
            requires_auth: Whether the agent requires authentication.
            audio_interface: The audio interface to use for input and output.
            callback_agent_response: Callback for agent responses.
            callback_agent_response_correction: Callback for agent response corrections.
                First argument is the original response (previously given to
                callback_agent_response), second argument is the corrected response.
            callback_user_transcript: Callback for user transcripts.
            callback_latency_measurement: Callback for latency measurements (in milliseconds).
        """

        self.client = client
        self.agent_id = agent_id
        self.requires_auth = requires_auth

        self.audio_interface = audio_interface
        self.callback_agent_response = callback_agent_response
        self.config = config or ConversationConfig()
        self.callback_agent_response_correction = callback_agent_response_correction
        self.callback_user_transcript = callback_user_transcript
        self.callback_latency_measurement = callback_latency_measurement

        self._thread = None
        self._should_stop = threading.Event()
        self._conversation_id = None
        self._last_interrupt_id = 0

    def start_session(self):
        """Starts the conversation session.

        Will run in background thread until `end_session` is called.
        """
        ws_url = self._get_signed_url() if self.requires_auth else self._get_wss_url()
        self._thread = threading.Thread(target=self._run, args=(ws_url,))
        self._thread.start()

    def end_session(self):
        """Ends the conversation session."""
        self.audio_interface.stop()
        self._should_stop.set()

    def wait_for_session_end(self) -> Optional[str]:
        """Waits for the conversation session to end.

        You must call `end_session` before calling this method, otherwise it will block.

        Returns the conversation ID, if available.
        """
        if not self._thread:
            raise RuntimeError("Session not started.")
        self._thread.join()
        return self._conversation_id

    def _run(self, ws_url: str):
        with connect(ws_url) as ws:
            ws.send(
                json.dumps(
                {
                    "type": "conversation_initiation_client_data",
                    "custom_llm_extra_body": self.config.extra_body,
                    "conversation_config_override": self.config.conversation_config_override,
                    }
                )
            )

            def input_callback(audio):
                ws.send(
                    json.dumps(
                        {
                            "user_audio_chunk": base64.b64encode(audio).decode(),
                        }
                    )
                )

            self.audio_interface.start(input_callback)
            while not self._should_stop.is_set():
                try:
                    message = json.loads(ws.recv(timeout=0.5))
                    if self._should_stop.is_set():
                        return
                    self._handle_message(message, ws)
                except TimeoutError:
                    pass

    def _handle_message(self, message, ws):
        if message["type"] == "conversation_initiation_metadata":
            event = message["conversation_initiation_metadata_event"]
            assert self._conversation_id is None
            self._conversation_id = event["conversation_id"]

        elif message["type"] == "audio":
            event = message["audio_event"]
            if int(event["event_id"]) <= self._last_interrupt_id:
                return
            audio = base64.b64decode(event["audio_base_64"])
            self.audio_interface.output(audio)
        elif message["type"] == "agent_response":
            if self.callback_agent_response:
                event = message["agent_response_event"]
                self.callback_agent_response(event["agent_response"].strip())
        elif message["type"] == "agent_response_correction":
            if self.callback_agent_response_correction:
                event = message["agent_response_correction_event"]
                self.callback_agent_response_correction(
                    event["original_agent_response"].strip(), event["corrected_agent_response"].strip()
                )
        elif message["type"] == "user_transcript":
            if self.callback_user_transcript:
                event = message["user_transcription_event"]
                self.callback_user_transcript(event["user_transcript"].strip())
        elif message["type"] == "interruption":
            event = message["interruption_event"]
            self.last_interrupt_id = int(event["event_id"])
            self.audio_interface.interrupt()
        elif message["type"] == "ping":
            event = message["ping_event"]
            ws.send(
                json.dumps(
                    {
                        "type": "pong",
                        "event_id": event["event_id"],
                    }
                )
            )
            if self.callback_latency_measurement and event["ping_ms"]:
                self.callback_latency_measurement(int(event["ping_ms"]))
        else:
            pass  # Ignore all other message types.

    def _get_wss_url(self):
        base_url = self.client._client_wrapper._base_url
        # Replace http(s) with ws(s).
        base_ws_url = base_url.replace("http", "ws", 1)  # First occurrence only.
        return f"{base_ws_url}/v1/convai/conversation?agent_id={self.agent_id}"

    def _get_signed_url(self):
        response = self.client.conversational_ai.get_signed_url(agent_id=self.agent_id)
        return response.signed_url
