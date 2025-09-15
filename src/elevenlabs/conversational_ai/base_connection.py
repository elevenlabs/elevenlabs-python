from abc import ABC, abstractmethod
import asyncio
import json
from typing import Callable, Optional, Awaitable, Union, Any, Literal, Dict
from enum import Enum


class ConnectionType(str, Enum):
    """Connection types available for conversations."""
    WEBSOCKET = "websocket"
    WEBRTC = "webrtc"


class BaseConnection(ABC):
    """Base class for conversation connections."""

    def __init__(self):
        self.conversation_id: Optional[str] = None
        self._message_queue = []
        self._on_message_callback: Optional[Callable[[dict], Union[None, Awaitable[None]]]] = None

    @abstractmethod
    async def connect(self) -> None:
        """Establish the connection."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the connection."""
        pass

    @abstractmethod
    async def send_message(self, message: dict) -> None:
        """Send a message through the connection."""
        pass

    @abstractmethod
    async def send_audio(self, audio_data: bytes) -> None:
        """Send audio data through the connection."""
        pass

    def on_message(self, callback: Callable[[dict], Union[None, Awaitable[None]]]) -> None:
        """Set the message callback."""
        self._on_message_callback = callback
        # Process any queued messages
        if self._message_queue:
            for message in self._message_queue:
                self._handle_message(message)
            self._message_queue.clear()

    def _handle_message(self, message: dict) -> None:
        """Handle incoming messages."""
        if self._on_message_callback:
            if asyncio.iscoroutinefunction(self._on_message_callback):
                asyncio.create_task(self._on_message_callback(message))
            else:
                self._on_message_callback(message)
        else:
            self._message_queue.append(message)