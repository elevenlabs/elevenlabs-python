from abc import ABC, abstractmethod
import base64
import json
import threading
from typing import Callable, Optional, Awaitable, Union, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

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


class ClientTools:
    """Handles registration and execution of client-side tools that can be called by the agent.

    Supports both synchronous and asynchronous tools running in a dedicated event loop,
    ensuring non-blocking operation of the main conversation thread.
    """

    def __init__(self):
        self.tools: dict[str, tuple[Union[Callable[[dict], Any], Callable[[dict], Awaitable[Any]]], bool]] = {}
        self.lock = threading.Lock()
        self._loop = None
        self._thread = None
        self._running = threading.Event()
        self.thread_pool = ThreadPoolExecutor()

    def start(self):
        """Start the event loop in a separate thread for handling async operations."""
        if self._running.is_set():
            return

        def run_event_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._running.set()
            try:
                self._loop.run_forever()
            finally:
                self._running.clear()
                self._loop.close()
                self._loop = None

        self._thread = threading.Thread(target=run_event_loop, daemon=True, name="ClientTools-EventLoop")
        self._thread.start()
        # Wait for loop to be ready
        self._running.wait()

    def stop(self):
        """Gracefully stop the event loop and clean up resources."""
        if self._loop and self._running.is_set():
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join()
            self.thread_pool.shutdown(wait=False)

    def register(
        self,
        tool_name: str,
        handler: Union[Callable[[dict], Any], Callable[[dict], Awaitable[Any]]],
        is_async: bool = False,
    ) -> None:
        """Register a new tool that can be called by the AI agent.

        Args:
            tool_name: Unique identifier for the tool
            handler: Function that implements the tool's logic
            is_async: Whether the handler is an async function
        """
        with self.lock:
            if not callable(handler):
                raise ValueError("Handler must be callable")
            if tool_name in self.tools:
                raise ValueError(f"Tool '{tool_name}' is already registered")
            self.tools[tool_name] = (handler, is_async)

    async def handle(self, tool_name: str, parameters: dict) -> Any:
        """Execute a registered tool with the given parameters.

        Returns the result of the tool execution.
        """
        with self.lock:
            if tool_name not in self.tools:
                raise ValueError(f"Tool '{tool_name}' is not registered")
            handler, is_async = self.tools[tool_name]

        if is_async:
            return await handler(parameters)
        else:
            return await asyncio.get_event_loop().run_in_executor(self.thread_pool, handler, parameters)

    def execute_tool(self, tool_name: str, parameters: dict, callback: Callable[[dict], None]):
        """Execute a tool and send its result via the provided callback.

        This method is non-blocking and handles both sync and async tools.
        """
        if not self._running.is_set():
            raise RuntimeError("ClientTools event loop is not running")

        async def _execute_and_callback():
            try:
                result = await self.handle(tool_name, parameters)
                response = {
                    "type": "client_tool_result",
                    "tool_call_id": parameters.get("tool_call_id"),
                    "result": result or f"Client tool: {tool_name} called successfully.",
                    "is_error": False,
                }
            except Exception as e:
                response = {
                    "type": "client_tool_result",
                    "tool_call_id": parameters.get("tool_call_id"),
                    "result": str(e),
                    "is_error": True,
                }
            callback(response)

        asyncio.run_coroutine_threadsafe(_execute_and_callback(), self._loop)


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
    client_tools: Optional[ClientTools]
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
        client_tools: Optional[ClientTools] = None,
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
            client_tools: The client tools to use for the conversation.
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
        self.client_tools = client_tools or ClientTools()
        self.callback_agent_response_correction = callback_agent_response_correction
        self.callback_user_transcript = callback_user_transcript
        self.callback_latency_measurement = callback_latency_measurement

        self.client_tools.start()

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
        """Ends the conversation session and cleans up resources."""
        self.audio_interface.stop()
        self.client_tools.stop()
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
            self._last_interrupt_id = int(event["event_id"])
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
        elif message["type"] == "client_tool_call":
            tool_call = message.get("client_tool_call", {})
            tool_name = tool_call.get("tool_name")
            parameters = {"tool_call_id": tool_call["tool_call_id"], **tool_call.get("parameters", {})}

            def send_response(response):
                if not self._should_stop.is_set():
                    ws.send(json.dumps(response))

            self.client_tools.execute_tool(tool_name, parameters, send_response)
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
