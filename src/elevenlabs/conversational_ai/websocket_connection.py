import json
import base64
from typing import Optional
import websockets
from websockets.exceptions import ConnectionClosedOK

from .base_connection import BaseConnection


class WebSocketConnection(BaseConnection):
    """WebSocket-based connection for conversations."""

    def __init__(self, ws_url: str):
        super().__init__()
        self.ws_url = ws_url
        self._ws: Optional[websockets.WebSocketClientProtocol] = None

    async def connect(self) -> None:
        """Establish the WebSocket connection."""
        self._ws = await websockets.connect(self.ws_url, max_size=16 * 1024 * 1024)

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def send_message(self, message: dict) -> None:
        """Send a message through the WebSocket."""
        if not self._ws:
            raise RuntimeError("WebSocket not connected")
        await self._ws.send(json.dumps(message))

    async def send_audio(self, audio_data: bytes) -> None:
        """Send audio data through the WebSocket."""
        if not self._ws:
            raise RuntimeError("WebSocket not connected")

        message = {
            "user_audio_chunk": base64.b64encode(audio_data).decode()
        }
        await self._ws.send(json.dumps(message))

    async def receive_messages(self) -> None:
        """Receive and handle messages from the WebSocket."""
        if not self._ws:
            return

        try:
            async for message_str in self._ws:
                try:
                    message = json.loads(message_str)
                    self._handle_message(message)
                except json.JSONDecodeError:
                    continue
        except ConnectionClosedOK:
            pass