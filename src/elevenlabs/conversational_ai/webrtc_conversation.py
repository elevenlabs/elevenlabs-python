import asyncio
import json
import base64
from typing import Optional, Callable, Awaitable

from ..base_client import BaseElevenLabs
from .conversation import (
    BaseConversation,
    ConversationInitiationData,
    AsyncAudioInterface,
    ClientTools
)
from .base_connection import ConnectionType
from .webrtc_connection import WebRTCConnection, WebRTCConnectionConfig


class WebRTCConversation(BaseConversation):
    """WebRTC-based conversational AI session using LiveKit.

    This class provides WebRTC connectivity for real-time audio conversations
    with ElevenLabs agents, offering lower latency compared to WebSocket connections.
    """

    def __init__(
        self,
        client: BaseElevenLabs,
        agent_id: str,
        user_id: Optional[str] = None,
        *,
        conversation_token: Optional[str] = None,
        livekit_url: Optional[str] = None,
        api_origin: Optional[str] = None,
        webrtc_overrides: Optional[dict] = None,
        on_debug: Optional[Callable[[dict], None]] = None,
        audio_interface: Optional[AsyncAudioInterface] = None,
        config: Optional[ConversationInitiationData] = None,
        client_tools: Optional[ClientTools] = None,
        callback_agent_response: Optional[Callable[[str], Awaitable[None]]] = None,
        callback_agent_response_correction: Optional[Callable[[str, str], Awaitable[None]]] = None,
        callback_user_transcript: Optional[Callable[[str], Awaitable[None]]] = None,
        callback_latency_measurement: Optional[Callable[[int], Awaitable[None]]] = None,
        callback_end_session: Optional[Callable[[], Awaitable[None]]] = None,
    ):
        """Initialize a WebRTC conversation.

        Args:
            client: The ElevenLabs client to use for the conversation.
            agent_id: The ID of the agent to converse with.
            user_id: The ID of the user conversing with the agent.
            conversation_token: Token for WebRTC authentication. If not provided,
                               will be fetched using the agent_id.
            livekit_url: Custom LiveKit WebSocket URL. If not provided, uses default.
            api_origin: Custom API origin for token fetching. If not provided, uses default.
            webrtc_overrides: Additional overrides specific to WebRTC connection.
            on_debug: Debug callback function for WebRTC connection events.
            audio_interface: The async audio interface to use for input and output.
            config: Configuration for the conversation.
            client_tools: Client tools for handling agent tool calls.
            callback_agent_response: Async callback for agent responses.
            callback_agent_response_correction: Async callback for response corrections.
            callback_user_transcript: Async callback for user transcripts.
            callback_latency_measurement: Async callback for latency measurements.
            callback_end_session: Async callback for when session ends.
        """

        # Set up configuration with WebRTC specifics
        if config is None:
            config = ConversationInitiationData()
        config.connection_type = ConnectionType.WEBRTC
        config.conversation_token = conversation_token
        config.livekit_url = livekit_url
        config.api_origin = api_origin
        config.webrtc_overrides = webrtc_overrides or {}
        config.on_debug = on_debug

        super().__init__(
            client=client,
            agent_id=agent_id,
            user_id=user_id,
            requires_auth=True,  # WebRTC requires authentication
            config=config,
            client_tools=client_tools,
        )

        self.audio_interface = audio_interface
        self.callback_agent_response = callback_agent_response
        self.callback_agent_response_correction = callback_agent_response_correction
        self.callback_user_transcript = callback_user_transcript
        self.callback_latency_measurement = callback_latency_measurement
        self.callback_end_session = callback_end_session

        self._connection: Optional[WebRTCConnection] = None
        self._should_stop = asyncio.Event()
        self._session_task: Optional[asyncio.Task] = None

    async def start_session(self):
        """Start the WebRTC conversation session."""
        try:
            # Use the enhanced connection creation from BaseConversation
            self._connection = self._create_connection()

            # Set up message handler
            self._connection.on_message(self._handle_message)

            # Connect
            await self._connection.connect()

            # Update conversation ID
            self._conversation_id = self._connection.conversation_id

            # Start audio interface if provided
            if self.audio_interface:
                await self.audio_interface.start(self._audio_input_callback)

            if self.config.on_debug:
                self.config.on_debug({
                    "type": "webrtc_conversation_started",
                    "conversation_id": self._conversation_id
                })

        except Exception as e:
            if self.config.on_debug:
                self.config.on_debug({
                    "type": "webrtc_session_start_error",
                    "error": str(e)
                })
            raise

    async def end_session(self):
        """End the WebRTC conversation session."""
        self._should_stop.set()

        if self.audio_interface:
            await self.audio_interface.stop()

        if self._connection:
            await self._connection.close()
            self._connection = None

        self.client_tools.stop()

        if self.callback_end_session:
            await self.callback_end_session()

    async def send_user_message(self, text: str):
        """Send a text message from the user to the agent."""
        if not self._connection:
            raise RuntimeError("Session not started")

        message = {
            "type": "user_message",
            "text": text
        }
        await self._connection.send_message(message)

    async def send_contextual_update(self, text: str):
        """Send a contextual update to the conversation."""
        if not self._connection:
            raise RuntimeError("Session not started")

        message = {
            "type": "contextual_update",
            "text": text
        }
        await self._connection.send_message(message)

    async def register_user_activity(self):
        """Register user activity to prevent session timeout."""
        if not self._connection:
            raise RuntimeError("Session not started")

        message = {
            "type": "user_activity"
        }
        await self._connection.send_message(message)

    async def _audio_input_callback(self, audio_data: bytes):
        """Handle audio input from the audio interface."""
        if self._connection and not self._should_stop.is_set():
            # For WebRTC, audio is sent through the room's microphone track
            # This callback can be used for custom processing if needed
            pass

    async def _handle_message(self, message: dict):
        """Handle incoming messages from the WebRTC connection."""
        try:
            message_type = message.get("type")

            if message_type == "conversation_initiation_metadata":
                event = message["conversation_initiation_metadata_event"]
                if not self._conversation_id:
                    self._conversation_id = event["conversation_id"]

            elif message_type == "audio":
                # Audio is handled through WebRTC audio tracks, not data messages
                pass

            elif message_type == "agent_response":
                if self.callback_agent_response:
                    event = message["agent_response_event"]
                    await self.callback_agent_response(event["agent_response"].strip())

            elif message_type == "agent_response_correction":
                if self.callback_agent_response_correction:
                    event = message["agent_response_correction_event"]
                    await self.callback_agent_response_correction(
                        event["original_agent_response"].strip(),
                        event["corrected_agent_response"].strip()
                    )

            elif message_type == "user_transcript":
                if self.callback_user_transcript:
                    event = message["user_transcription_event"]
                    await self.callback_user_transcript(event["user_transcript"].strip())

            elif message_type == "interruption":
                if self.audio_interface:
                    await self.audio_interface.interrupt()

            elif message_type == "ping":
                event = message["ping_event"]
                # Send pong response
                pong_message = {
                    "type": "pong",
                    "event_id": event["event_id"]
                }
                await self._connection.send_message(pong_message)

                if self.callback_latency_measurement and event.get("ping_ms"):
                    await self.callback_latency_measurement(int(event["ping_ms"]))

            elif message_type == "client_tool_call":
                tool_call = message.get("client_tool_call", {})
                tool_name = tool_call.get("tool_name")
                parameters = {
                    "tool_call_id": tool_call["tool_call_id"],
                    **tool_call.get("parameters", {})
                }

                # Execute tool asynchronously
                async def send_response(response):
                    if not self._should_stop.is_set():
                        await self._connection.send_message(response)

                self.client_tools.execute_tool(tool_name, parameters, send_response)

        except Exception as e:
            print(f"Error handling message: {e}")

    def get_webrtc_room(self):
        """Get the underlying LiveKit room for advanced WebRTC operations."""
        if self._connection:
            return self._connection.get_room()
        return None