from typing import Optional, Callable, Awaitable, Union

from ..base_client import BaseElevenLabs
from .conversation import (
    Conversation,
    AsyncConversation,
    AudioInterface,
    AsyncAudioInterface,
    ConversationInitiationData,
    ClientTools
)
from .webrtc_conversation import WebRTCConversation
from .base_connection import ConnectionType


def create_conversation(
    client: BaseElevenLabs,
    agent_id: str,
    user_id: Optional[str] = None,
    *,
    connection_type: ConnectionType = ConnectionType.WEBSOCKET,
    conversation_token: Optional[str] = None,
    requires_auth: bool = True,
    audio_interface: Optional[Union[AudioInterface, AsyncAudioInterface]] = None,
    config: Optional[ConversationInitiationData] = None,
    client_tools: Optional[ClientTools] = None,
    # Sync callbacks (for websocket conversations)
    callback_agent_response: Optional[Callable[[str], None]] = None,
    callback_agent_response_correction: Optional[Callable[[str, str], None]] = None,
    callback_user_transcript: Optional[Callable[[str], None]] = None,
    callback_latency_measurement: Optional[Callable[[int], None]] = None,
    callback_end_session: Optional[Callable] = None,
    # Async callbacks (for WebRTC and async websocket conversations)
    async_callback_agent_response: Optional[Callable[[str], Awaitable[None]]] = None,
    async_callback_agent_response_correction: Optional[Callable[[str, str], Awaitable[None]]] = None,
    async_callback_user_transcript: Optional[Callable[[str], Awaitable[None]]] = None,
    async_callback_latency_measurement: Optional[Callable[[int], Awaitable[None]]] = None,
    async_callback_end_session: Optional[Callable[[], Awaitable[None]]] = None,
) -> Union[Conversation, AsyncConversation, WebRTCConversation]:
    """Create a conversation with the specified connection type.

    Args:
        client: ElevenLabs client instance
        agent_id: ID of the agent to connect to
        user_id: Optional user ID
        connection_type: Type of connection (websocket or webrtc)
        conversation_token: Token for WebRTC authentication
        requires_auth: Whether authentication is required
        audio_interface: Audio interface for the conversation
        config: Conversation configuration
        client_tools: Client tools for handling agent calls
        callback_*: Synchronous callbacks for websocket conversations
        async_callback_*: Asynchronous callbacks for WebRTC and async conversations

    Returns:
        A conversation instance of the appropriate type

    Examples:
        # WebSocket conversation (default)
        conversation = create_conversation(
            client=client,
            agent_id="your-agent-id",
            audio_interface=your_audio_interface
        )

        # WebRTC conversation
        conversation = create_conversation(
            client=client,
            agent_id="your-agent-id",
            connection_type=ConnectionType.WEBRTC,
            conversation_token="your-token",  # Optional, will fetch if not provided
            audio_interface=your_async_audio_interface,
            async_callback_agent_response=your_response_handler
        )

        # Public agent (no auth required)
        conversation = create_conversation(
            client=client,
            agent_id="public-agent-id",
            connection_type=ConnectionType.WEBRTC,
            requires_auth=False,
            audio_interface=your_async_audio_interface
        )
    """

    # Set up configuration
    if config is None:
        config = ConversationInitiationData()

    config.connection_type = connection_type
    if conversation_token:
        config.conversation_token = conversation_token

    if connection_type == ConnectionType.WEBRTC:
        # Create WebRTC conversation
        if not isinstance(audio_interface, AsyncAudioInterface) and audio_interface is not None:
            raise ValueError("WebRTC conversations require an AsyncAudioInterface")

        return WebRTCConversation(
            client=client,
            agent_id=agent_id,
            user_id=user_id,
            conversation_token=conversation_token,
            audio_interface=audio_interface,
            config=config,
            client_tools=client_tools,
            callback_agent_response=async_callback_agent_response,
            callback_agent_response_correction=async_callback_agent_response_correction,
            callback_user_transcript=async_callback_user_transcript,
            callback_latency_measurement=async_callback_latency_measurement,
            callback_end_session=async_callback_end_session,
        )

    elif connection_type == ConnectionType.WEBSOCKET:
        # Determine if we should use sync or async conversation
        has_async_callbacks = any([
            async_callback_agent_response,
            async_callback_agent_response_correction,
            async_callback_user_transcript,
            async_callback_latency_measurement,
            async_callback_end_session,
        ])

        if has_async_callbacks or isinstance(audio_interface, AsyncAudioInterface):
            # Use async conversation
            return AsyncConversation(
                client=client,
                agent_id=agent_id,
                user_id=user_id,
                requires_auth=requires_auth,
                audio_interface=audio_interface,  # type: ignore
                config=config,
                client_tools=client_tools,
                callback_agent_response=async_callback_agent_response,
                callback_agent_response_correction=async_callback_agent_response_correction,
                callback_user_transcript=async_callback_user_transcript,
                callback_latency_measurement=async_callback_latency_measurement,
                callback_end_session=async_callback_end_session,
            )
        else:
            # Use sync conversation
            if not isinstance(audio_interface, AudioInterface) and audio_interface is not None:
                raise ValueError("Synchronous WebSocket conversations require an AudioInterface")

            return Conversation(
                client=client,
                agent_id=agent_id,
                user_id=user_id,
                requires_auth=requires_auth,
                audio_interface=audio_interface,  # type: ignore
                config=config,
                client_tools=client_tools,
                callback_agent_response=callback_agent_response,
                callback_agent_response_correction=callback_agent_response_correction,
                callback_user_transcript=callback_user_transcript,
                callback_latency_measurement=callback_latency_measurement,
                callback_end_session=callback_end_session,
            )

    else:
        raise ValueError(f"Unsupported connection type: {connection_type}")


# Convenience functions for specific connection types

def create_webrtc_conversation(
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
) -> WebRTCConversation:
    """Create a WebRTC conversation.

    Convenience function for creating WebRTC conversations with type safety.
    """
    return WebRTCConversation(
        client=client,
        agent_id=agent_id,
        user_id=user_id,
        conversation_token=conversation_token,
        livekit_url=livekit_url,
        api_origin=api_origin,
        webrtc_overrides=webrtc_overrides,
        on_debug=on_debug,
        audio_interface=audio_interface,
        config=config,
        client_tools=client_tools,
        callback_agent_response=callback_agent_response,
        callback_agent_response_correction=callback_agent_response_correction,
        callback_user_transcript=callback_user_transcript,
        callback_latency_measurement=callback_latency_measurement,
        callback_end_session=callback_end_session,
    )


def create_websocket_conversation(
    client: BaseElevenLabs,
    agent_id: str,
    user_id: Optional[str] = None,
    *,
    requires_auth: bool = True,
    audio_interface: Optional[AudioInterface] = None,
    config: Optional[ConversationInitiationData] = None,
    client_tools: Optional[ClientTools] = None,
    callback_agent_response: Optional[Callable[[str], None]] = None,
    callback_agent_response_correction: Optional[Callable[[str, str], None]] = None,
    callback_user_transcript: Optional[Callable[[str], None]] = None,
    callback_latency_measurement: Optional[Callable[[int], None]] = None,
    callback_end_session: Optional[Callable] = None,
) -> Union[Conversation, AsyncConversation]:
    """Create a WebSocket conversation.

    Convenience function for creating WebSocket conversations with type safety.
    """
    result = create_conversation(
        client=client,
        agent_id=agent_id,
        user_id=user_id,
        connection_type=ConnectionType.WEBSOCKET,
        requires_auth=requires_auth,
        audio_interface=audio_interface,
        config=config,
        client_tools=client_tools,
        callback_agent_response=callback_agent_response,
        callback_agent_response_correction=callback_agent_response_correction,
        callback_user_transcript=callback_user_transcript,
        callback_latency_measurement=callback_latency_measurement,
        callback_end_session=callback_end_session,
    )
    return result