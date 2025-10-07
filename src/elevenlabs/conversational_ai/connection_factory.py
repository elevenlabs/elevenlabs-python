from typing import Optional, Dict, Any, Callable

from .base_connection import BaseConnection, ConnectionType
from .websocket_connection import WebSocketConnection
from .webrtc_connection import WebRTCConnection, WebRTCConnectionConfig


def create_connection(
    connection_type: ConnectionType,
    *,
    ws_url: Optional[str] = None,
    conversation_token: Optional[str] = None,
    agent_id: Optional[str] = None,
    livekit_url: Optional[str] = None,
    api_origin: Optional[str] = None,
    overrides: Optional[Dict[str, Any]] = None,
    on_debug: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> BaseConnection:
    """Factory function to create connections based on type."""

    if connection_type == ConnectionType.WEBSOCKET:
        if not ws_url:
            raise ValueError("ws_url is required for WebSocket connections")
        return WebSocketConnection(ws_url)

    elif connection_type == ConnectionType.WEBRTC:
        return WebRTCConnection(
            conversation_token=conversation_token,
            agent_id=agent_id,
            livekit_url=livekit_url,
            api_origin=api_origin,
            overrides=overrides,
            on_debug=on_debug,
        )

    else:
        raise ValueError(f"Unknown connection type: {connection_type}")


def determine_connection_type(
    connection_type: Optional[ConnectionType] = None,
    conversation_token: Optional[str] = None,
    **kwargs
) -> ConnectionType:
    """Determine the appropriate connection type based on parameters."""

    # If connection_type is explicitly specified, use it
    if connection_type:
        return connection_type

    # If conversation_token is provided, use WebRTC
    if conversation_token:
        return ConnectionType.WEBRTC

    # Default to WebSocket for backward compatibility
    return ConnectionType.WEBSOCKET