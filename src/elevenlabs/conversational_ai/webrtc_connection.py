import json
import asyncio
from typing import Optional, Dict, Any, Callable, Union, Awaitable
import httpx

try:
    from livekit.rtc import Room, TrackKind
except ImportError:
    raise ImportError(
        "livekit package is required for WebRTC support. "
        "Install with: pip install livekit"
    )

from .base_connection import BaseConnection


class WebRTCConnectionConfig:
    """Configuration for WebRTC connection."""
    def __init__(
        self,
        conversation_token: Optional[str] = None,
        agent_id: Optional[str] = None,
        livekit_url: Optional[str] = None,
        api_origin: Optional[str] = None,
        overrides: Optional[Dict[str, Any]] = None,
        on_debug: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        self.conversation_token = conversation_token
        self.agent_id = agent_id
        self.livekit_url = livekit_url
        self.api_origin = api_origin
        self.overrides = overrides or {}
        self.on_debug = on_debug


class WebRTCConnection(BaseConnection):
    """WebRTC-based connection for conversations using LiveKit."""

    DEFAULT_LIVEKIT_WS_URL = "wss://livekit.rtc.elevenlabs.io"
    DEFAULT_API_ORIGIN = "https://api.elevenlabs.io"

    def __init__(
        self,
        conversation_token: Optional[str] = None,
        agent_id: Optional[str] = None,
        livekit_url: Optional[str] = None,
        api_origin: Optional[str] = None,
        overrides: Optional[Dict[str, Any]] = None,
        on_debug: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        super().__init__()
        self.conversation_token = conversation_token
        self.agent_id = agent_id
        self.livekit_url = livekit_url or self.DEFAULT_LIVEKIT_WS_URL
        self.api_origin = api_origin or self.DEFAULT_API_ORIGIN
        self.overrides = overrides or {}
        self.on_debug = on_debug
        self._room: Optional[Room] = None
        self._is_connected: bool = False

    @classmethod
    async def create(cls, config: WebRTCConnectionConfig) -> "WebRTCConnection":
        """Create and connect a WebRTC connection."""
        connection = cls(
            conversation_token=config.conversation_token,
            agent_id=config.agent_id,
            livekit_url=config.livekit_url,
            api_origin=config.api_origin,
            overrides=config.overrides,
            on_debug=config.on_debug,
        )

        await connection.connect()
        return connection

    async def connect(self) -> None:
        """Establish the WebRTC connection using LiveKit."""
        try:
            # Get conversation token if not provided
            if not self.conversation_token:
                if not self.agent_id:
                    raise ValueError("Either conversation_token or agent_id is required for WebRTC connection")
                self.conversation_token = await self._fetch_conversation_token()

            # Create room and connect
            self._room = Room()
            self._setup_room_callbacks()

            # Connect to LiveKit room using configurable URL
            try:
                await self._room.connect(self.livekit_url, self.conversation_token)
                self._is_connected = True
            except Exception as e:
                self._is_connected = False
                raise ConnectionError(f"Failed to connect to LiveKit room: {e}") from e

            # Set conversation ID from room name if available
            if self._room.name:
                # Extract conversation ID from room name if it contains one
                import re
                match = re.search(r'(conv_[a-zA-Z0-9]+)', self._room.name)
                self.conversation_id = match.group(0) if match else self._room.name
            else:
                self.conversation_id = f"webrtc-{id(self)}"

            # Enable microphone
            try:
                await self._room.local_participant.set_microphone_enabled(True)
            except Exception as e:
                self.debug({
                    "type": "microphone_enable_error",
                    "error": str(e)
                })
                # Don't fail the connection for microphone issues

            # Send overrides if any
            if self.overrides:
                try:
                    await self.send_message(self._construct_overrides())
                except Exception as e:
                    self.debug({
                        "type": "overrides_send_error",
                        "error": str(e)
                    })

            self.debug({
                "type": "conversation_initiation_client_data",
                "message": self._construct_overrides()
            })

        except Exception as e:
            # Ensure cleanup on connection failure
            if self._room:
                try:
                    await self._room.disconnect()
                except:
                    pass
                self._room = None
            self._is_connected = False
            raise

    async def close(self) -> None:
        """Close the WebRTC connection."""
        if self._room:
            try:
                await self._room.disconnect()
            except Exception as e:
                self.debug({
                    "type": "disconnect_error",
                    "error": str(e)
                })
            finally:
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

    async def receive_messages(self) -> None:
        """Receive and handle messages - handled by LiveKit event callbacks."""
        # In WebRTC mode, messages are handled via LiveKit event callbacks
        # This method exists for compatibility with the BaseConnection interface
        if not self._is_connected:
            return

        # Keep the connection alive while connected
        while self._is_connected:
            await asyncio.sleep(0.1)

    async def _fetch_conversation_token(self) -> str:
        """Fetch conversation token from ElevenLabs API."""
        if not self.agent_id:
            raise ValueError("Agent ID is required to fetch conversation token")

        try:
            # Get version and source from overrides or use defaults
            version = self.overrides.get("client", {}).get("version", "2.15.0")  # From pyproject.toml
            source = self.overrides.get("client", {}).get("source", "python_sdk")

            # Convert WSS origin to HTTPS for API calls
            api_origin = self._convert_wss_to_https(self.api_origin)

            url = f"{api_origin}/v1/convai/conversation/token?agent_id={self.agent_id}&source={source}&version={version}"

            async with httpx.AsyncClient(timeout=30.0) as client:
                try:
                    response = await client.get(url)
                except httpx.TimeoutException:
                    raise ConnectionError(f"Timeout when fetching conversation token for agent {self.agent_id}")
                except httpx.NetworkError as e:
                    raise ConnectionError(f"Network error when fetching conversation token: {e}")

                if not response.is_success:
                    error_msg = f"ElevenLabs API returned {response.status_code} {response.reason_phrase}"
                    if response.status_code == 401:
                        error_msg = "Your agent has authentication enabled, but no signed URL or conversation token was provided."
                    elif response.status_code == 404:
                        error_msg = f"Agent with ID {self.agent_id} not found"
                    elif response.status_code == 429:
                        error_msg = "Rate limit exceeded. Please try again later."

                    raise Exception(f"Failed to fetch conversation token for agent {self.agent_id}: {error_msg}")

                try:
                    data = response.json()
                except Exception as e:
                    raise Exception(f"Invalid JSON response from API: {e}")

                token = data.get("token")

                if not token:
                    raise Exception("No conversation token received from API")

                return token

        except Exception as e:
            self.debug({
                "type": "token_fetch_error",
                "agent_id": self.agent_id,
                "error": str(e)
            })
            raise

    def _convert_wss_to_https(self, origin: str) -> str:
        """Convert WSS origin to HTTPS for API calls."""
        return origin.replace("wss://", "https://")

    def _construct_overrides(self) -> Dict[str, Any]:
        """Construct overrides message for conversation initiation."""
        return {
            "type": "conversation_initiation_client_data",
            "overrides": self.overrides
        }

    def debug(self, info: Dict[str, Any]) -> None:
        """Log debug information."""
        if self.on_debug:
            self.on_debug(info)

    def _setup_room_callbacks(self) -> None:
        """Setup LiveKit room event callbacks."""
        if not self._room:
            return

        @self._room.on("connected")
        def on_connected() -> None:
            self._is_connected = True
            self.debug({"type": "webrtc_connected", "message": "WebRTC room connected"})

        @self._room.on("disconnected")
        def on_disconnected(reason: Optional[str] = None) -> None:
            self._is_connected = False
            self.debug({"type": "webrtc_disconnected", "message": f"WebRTC room disconnected: {reason}"})

        @self._room.on("connection_state_changed")
        def on_connection_state_changed(state) -> None:
            self.debug({"type": "connection_state_changed", "state": str(state)})
            # Handle disconnected state
            if hasattr(state, 'name') and state.name == 'DISCONNECTED':
                self._is_connected = False

        @self._room.on("data_received")
        def on_data_received(data: bytes, participant) -> None:
            try:
                message = json.loads(data.decode('utf-8'))

                # Filter out audio messages for WebRTC - they're handled via audio tracks
                if message.get("type") == "audio":
                    return

                self._handle_message(message)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                self.debug({
                    "type": "data_parse_error",
                    "error": str(e),
                    "raw_data": data.decode('utf-8', errors='replace')
                })

        @self._room.on("track_subscribed")
        def on_track_subscribed(track, publication, participant) -> None:
            if track.kind == TrackKind.KIND_AUDIO and "agent" in participant.identity:
                self.debug({
                    "type": "agent_audio_track_subscribed",
                    "participant": participant.identity
                })

        @self._room.on("active_speakers_changed")
        def on_active_speakers_changed(speakers) -> None:
            # Update mode based on active speakers
            if speakers and len(speakers) > 0:
                is_agent_speaking = any("agent" in speaker.identity for speaker in speakers)
                mode = "speaking" if is_agent_speaking else "listening"
            else:
                mode = "listening"

            self.debug({"type": "mode_changed", "mode": mode})

    async def set_microphone_enabled(self, enabled: bool) -> None:
        """Enable or disable the microphone."""
        if not self._room or not self._room.local_participant:
            raise RuntimeError("Room not connected")

        await self._room.local_participant.set_microphone_enabled(enabled)

    async def set_microphone_device(self, device_id: str) -> None:
        """Set the microphone input device."""
        if not self._room or not self._room.local_participant:
            raise RuntimeError("Room not connected")

        # This would require additional LiveKit functionality for device switching
        # For now, we log the request
        self.debug({
            "type": "microphone_device_change_requested",
            "device_id": device_id
        })

    def get_room(self) -> Optional[Room]:
        """Get the LiveKit room instance for advanced usage."""
        return self._room