import asyncio
import json
import base64
from typing import Callable, Optional, Any
import websockets
from websockets.exceptions import ConnectionClosed

# Reuse existing types from the sync module
from .conversation import ClientTools, ConversationInitiationData

class AsyncConversation:
    """
    Asynchronous version of the Conversation.

    This class is intended for use with an async ElevenLabs client (such as AsyncElevenLabs).
    Other parameters (agent_id, audio_interface, callbacks, etc.) remain the same.
    """
    def __init__(
        self,
        client: Any,
        agent_id: str,
        *,
        requires_auth: bool,
        audio_interface: Any,
        config: Optional[ConversationInitiationData] = None,
        client_tools: Optional[ClientTools] = None,
        callback_agent_response: Optional[Callable[[str], None]] = None,
        callback_agent_response_correction: Optional[Callable[[str, str], None]] = None,
        callback_user_transcript: Optional[Callable[[str], None]] = None,
        callback_latency_measurement: Optional[Callable[[int], None]] = None,
    ):
        """
        Initializes the async conversation. The parameters are the same as the synchronous version.
        """
        self.client = client
        self.agent_id = agent_id
        self.requires_auth = requires_auth
        self.audio_interface = audio_interface
        self.config = config or ConversationInitiationData()
        self.client_tools = client_tools or ClientTools()
        self.callback_agent_response = callback_agent_response
        self.callback_agent_response_correction = callback_agent_response_correction
        self.callback_user_transcript = callback_user_transcript
        self.callback_latency_measurement = callback_latency_measurement

        # Start the client tools event loop (if needed)
        self.client_tools.start()

        self._conversation_id: Optional[str] = None
        self._last_interrupt_id: int = 0
        self._should_stop: asyncio.Event = asyncio.Event()
        self._task: Optional[asyncio.Task] = None

    async def start_session(self) -> None:
        """
        Starts the asynchronous conversation session.

        If authentication is required, this awaits the async get_signed_url call.
        Then, it creates a background task to run the conversation.
        """
        ws_url = await self._get_signed_url() if self.requires_auth else await self._get_wss_url()
        self._task = asyncio.create_task(self._run(ws_url))

    async def end_session(self) -> None:
        """
        Ends the conversation session and cleans up resources.
        """
        self.audio_interface.stop()
        self.client_tools.stop()
        self._should_stop.set()
        if self._task:
            await self._task

    async def wait_for_session_end(self) -> Optional[str]:
        """
        Awaits the end of the conversation session and returns the conversation ID, if available.
        """
        if not self._task:
            raise RuntimeError("Session not started.")
        await self._task
        return self._conversation_id

    async def _get_signed_url(self) -> str:
        """
        Awaits the async get_signed_url method from the client.
        """
        response = await self.client.conversational_ai.get_signed_url(agent_id=self.agent_id)
        return response.signed_url

    async def _get_wss_url(self) -> str:
        """
        Constructs the websocket URL for non-authenticated sessions.
        """
        base_url = self.client._client_wrapper._base_url
        base_ws_url = base_url.replace("http", "ws", 1)  # Replace only first occurrence.
        return f"{base_ws_url}/v1/convai/conversation?agent_id={self.agent_id}"

    async def _run(self, ws_url: str) -> None:
        """
        Main async loop: connects to the websocket and listens for messages.
        """
        try:
            async with websockets.connect(ws_url) as ws:
                # Send the conversation initiation data.
                await ws.send(json.dumps({
                    "type": "conversation_initiation_client_data",
                    "custom_llm_extra_body": self.config.extra_body,
                    "conversation_config_override": self.config.conversation_config_override,
                    "dynamic_variables": self.config.dynamic_variables,
                }))

                # Define a callback for handling audio input.
                def input_callback(audio: bytes):
                    async def send_audio():
                        try:
                            await ws.send(json.dumps({
                                "user_audio_chunk": base64.b64encode(audio).decode(),
                            }))
                        except ConnectionClosed:
                            await self.end_session()
                        except Exception as e:
                            print(f"Error sending user audio chunk: {e}")
                            await self.end_session()
                    asyncio.create_task(send_audio())

                # Start the audio interface.
                self.audio_interface.start(input_callback)

                while not self._should_stop.is_set():
                    try:
                        raw_message = await asyncio.wait_for(ws.recv(), timeout=0.5)
                        message = json.loads(raw_message)
                        await self._handle_message(message, ws)
                    except asyncio.TimeoutError:
                        continue
                    except ConnectionClosed:
                        await self.end_session()
                    except Exception as e:
                        print(f"Error receiving message: {e}")
                        await self.end_session()
        except Exception as e:
            print(f"Error in connection: {e}")
            await self.end_session()

    async def _handle_message(self, message: dict, ws: websockets.WebSocketClientProtocol) -> None:
        """
        Handles incoming messages from the websocket.
        """
        msg_type = message.get("type")
        if msg_type == "conversation_initiation_metadata":
            event = message["conversation_initiation_metadata_event"]
            if self._conversation_id is None:
                self._conversation_id = event["conversation_id"]

        elif msg_type == "audio":
            event = message["audio_event"]
            if int(event["event_id"]) <= self._last_interrupt_id:
                return
            audio = base64.b64decode(event["audio_base_64"])
            self.audio_interface.output(audio)

        elif msg_type == "agent_response":
            if self.callback_agent_response:
                event = message["agent_response_event"]
                self.callback_agent_response(event["agent_response"].strip())

        elif msg_type == "agent_response_correction":
            if self.callback_agent_response_correction:
                event = message["agent_response_correction_event"]
                self.callback_agent_response_correction(
                    event["original_agent_response"].strip(), event["corrected_agent_response"].strip()
                )

        elif msg_type == "user_transcript":
            if self.callback_user_transcript:
                event = message["user_transcription_event"]
                self.callback_user_transcript(event["user_transcript"].strip())

        elif msg_type == "interruption":
            event = message["interruption_event"]
            self._last_interrupt_id = int(event["event_id"])
            self.audio_interface.interrupt()

        elif msg_type == "ping":
            event = message["ping_event"]
            await ws.send(json.dumps({
                "type": "pong",
                "event_id": event["event_id"],
            }))
            if self.callback_latency_measurement and event.get("ping_ms"):
                self.callback_latency_measurement(int(event["ping_ms"]))

        elif msg_type == "client_tool_call":
            tool_call = message.get("client_tool_call", {})
            tool_name = tool_call.get("tool_name")
            parameters = {"tool_call_id": tool_call.get("tool_call_id"), **tool_call.get("parameters", {})}
            try:
                result = await self.client_tools.handle(tool_name, parameters)
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
            await ws.send(json.dumps(response))

        else:
            pass  # Ignore any other message types.