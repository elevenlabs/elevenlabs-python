import json
import asyncio
from typing import Optional, Dict, Any
import httpx
from livekit.rtc import Room, TrackKind

from .base_connection import BaseConnection


class WebRTCConnection(BaseConnection):
    """WebRTC-based connection for conversations using LiveKit."""

    LIVEKIT_WS_URL = "wss://livekit.rtc.elevenlabs.io"

    def __init__(self, conversation_token: Optional[str] = None, agent_id: Optional[str] = None):
        super().__init__()
        self.conversation_token = conversation_token
        self.agent_id = agent_id
        self._room: Optional[Room] = None
        self._is_connected = False

    async def connect(self) -> None:
        """Establish the WebRTC connection using LiveKit."""
        # Get conversation token if not provided
        if not self.conversation_token:
            if not self.agent_id:
                raise ValueError("Either conversation_token or agent_id is required for WebRTC connection")
            self.conversation_token = await self._fetch_conversation_token()

        # Create room and connect
        self._room = Room()
        self._setup_room_callbacks()

        # Connect to LiveKit room
        await self._room.connect(self.LIVEKIT_WS_URL, self.conversation_token)
        self._is_connected = True

        # Set conversation ID from room name if available
        if self._room.name:
            self.conversation_id = self._room.name
        else:
            self.conversation_id = f"webrtc-{id(self)}"

        # Enable microphone
        await self._room.local_participant.set_microphone_enabled(True)

    async def close(self) -> None:
        """Close the WebRTC connection."""
        if self._room:
            await self._room.disconnect()
            self._room = None
        self._is_connected = False

    async def send_message(self, message: dict) -> None:
        """Send a message through WebRTC data channel."""
        if not self._is_connected or not self._room:
            raise RuntimeError("WebRTC room not connected")

        # In WebRTC mode, audio is sent via published tracks, not data messages
        if "user_audio_chunk" in message:
            return  # Audio is handled separately

        try:
            data = json.dumps(message).encode('utf-8')
            await self._room.local_participant.publish_data(data, reliable=True)
        except Exception as e:
            print(f"Failed to send message via WebRTC: {e}")
            raise

    async def send_audio(self, audio_data: bytes) -> None:
        """Send audio data through WebRTC (handled by published tracks)."""
        # In WebRTC mode, audio is sent through the microphone track
        # This method can be used for custom audio streaming if needed
        pass

    async def _fetch_conversation_token(self) -> str:
        """Fetch conversation token from ElevenLabs API."""
        if not self.agent_id:
            raise ValueError("Agent ID is required to fetch conversation token")

        url = f"https://api.elevenlabs.io/v1/convai/conversation/token?agent_id={self.agent_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if not response.is_success:
                raise Exception(f"Failed to fetch conversation token for agent {self.agent_id}: {response.status_code} {response.text}")

            data = response.json()
            token = data.get("token")

            if not token:
                raise Exception("No conversation token received from API")

            return token

    def _setup_room_callbacks(self) -> None:
        """Setup LiveKit room event callbacks."""
        if not self._room:
            return

        @self._room.on("connected")
        def on_connected() -> None:
            print("WebRTC room connected")

        @self._room.on("disconnected")
        def on_disconnected(reason: Optional[str] = None) -> None:
            self._is_connected = False
            print(f"WebRTC room disconnected: {reason}")

        @self._room.on("data_received")
        def on_data_received(data: bytes, participant) -> None:
            try:
                message = json.loads(data.decode('utf-8'))

                # Filter out audio messages for WebRTC - they're handled via audio tracks
                if message.get("type") == "audio":
                    return

                self._handle_message(message)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"Failed to parse incoming data message: {e}")

        @self._room.on("track_subscribed")
        def on_track_subscribed(track, publication, participant) -> None:
            if track.kind == TrackKind.KIND_AUDIO and "agent" in participant.identity:
                # Handle incoming agent audio
                print("Subscribed to agent audio track")

    def get_room(self) -> Optional[Room]:
        """Get the LiveKit room instance for advanced usage."""
        return self._room