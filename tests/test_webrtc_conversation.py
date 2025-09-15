import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

from elevenlabs.conversational_ai.base_connection import ConnectionType
from elevenlabs.conversational_ai.conversation_factory import (
    create_conversation,
    create_webrtc_conversation,
    create_websocket_conversation
)
from elevenlabs.conversational_ai.webrtc_conversation import WebRTCConversation
from elevenlabs.conversational_ai.conversation import Conversation, AsyncConversation
from elevenlabs.conversational_ai.webrtc_connection import WebRTCConnection


class TestWebRTCConversation:
    """Test WebRTC conversation functionality."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock ElevenLabs client."""
        return Mock()

    @pytest.fixture
    def mock_audio_interface(self):
        """Create a mock async audio interface."""
        from elevenlabs.conversational_ai.conversation import AsyncAudioInterface
        interface = Mock(spec=AsyncAudioInterface)
        interface.start = AsyncMock()
        interface.stop = AsyncMock()
        interface.output = AsyncMock()
        interface.interrupt = AsyncMock()
        return interface

    def test_connection_type_determination(self):
        """Test that connection types are determined correctly."""
        from elevenlabs.conversational_ai.connection_factory import determine_connection_type

        # Default should be websocket
        assert determine_connection_type() == ConnectionType.WEBSOCKET

        # Explicit connection type should be respected
        assert determine_connection_type(ConnectionType.WEBRTC) == ConnectionType.WEBRTC

        # Conversation token should imply WebRTC
        assert determine_connection_type(conversation_token="token") == ConnectionType.WEBRTC

        # Explicit type should override token inference
        assert determine_connection_type(
            ConnectionType.WEBSOCKET,
            conversation_token="token"
        ) == ConnectionType.WEBSOCKET

    def test_factory_creates_correct_conversation_types(self, mock_client):
        """Test that the factory creates the correct conversation types."""
        # WebRTC conversation
        webrtc_conv = create_conversation(
            client=mock_client,
            agent_id="test-agent",
            connection_type=ConnectionType.WEBRTC
        )
        assert isinstance(webrtc_conv, WebRTCConversation)

        # WebSocket conversation (sync)
        ws_conv = create_conversation(
            client=mock_client,
            agent_id="test-agent",
            connection_type=ConnectionType.WEBSOCKET
        )
        assert isinstance(ws_conv, (Conversation, AsyncConversation))

    def test_convenience_functions(self, mock_client, mock_audio_interface):
        """Test convenience functions for creating conversations."""
        # WebRTC convenience function with conversation token to avoid HTTP calls
        with patch('elevenlabs.conversational_ai.webrtc_connection.Room') as mock_room_class:
            mock_room = Mock()
            mock_room.connect = AsyncMock()
            mock_room.disconnect = AsyncMock()
            mock_room.local_participant = Mock()
            mock_room.local_participant.set_microphone_enabled = AsyncMock()
            mock_room.name = "test-room"
            mock_room_class.return_value = mock_room

            webrtc_conv = create_webrtc_conversation(
                client=mock_client,
                agent_id="test-agent",
                conversation_token="test-token",
                audio_interface=mock_audio_interface
            )
            assert isinstance(webrtc_conv, WebRTCConversation)

        # WebSocket convenience function
        ws_conv = create_websocket_conversation(
            client=mock_client,
            agent_id="test-agent"
        )
        assert isinstance(ws_conv, Conversation)

    @pytest.mark.asyncio
    async def test_webrtc_conversation_lifecycle(self, mock_client, mock_audio_interface):
        """Test WebRTC conversation lifecycle."""
        with patch('elevenlabs.conversational_ai.webrtc_connection.Room') as mock_room_class:
            # Mock room instance
            mock_room = Mock()
            mock_room.connect = AsyncMock()
            mock_room.disconnect = AsyncMock()
            mock_room.local_participant = Mock()
            mock_room.local_participant.set_microphone_enabled = AsyncMock()
            mock_room.local_participant.publish_data = AsyncMock()
            mock_room.name = "test-room"
            mock_room_class.return_value = mock_room

            # Create conversation with a conversation token to avoid HTTP calls
            conversation = WebRTCConversation(
                client=mock_client,
                agent_id="test-agent",
                conversation_token="test-token",  # Provide token to avoid fetching
                audio_interface=mock_audio_interface
            )

            # Test start session
            await conversation.start_session()
            mock_room.connect.assert_called_once()
            mock_audio_interface.start.assert_called_once()

            # Test end session
            await conversation.end_session()
            mock_room.disconnect.assert_called_once()
            mock_audio_interface.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_webrtc_conversation_messaging(self, mock_client):
        """Test WebRTC conversation messaging functionality."""
        with patch('elevenlabs.conversational_ai.webrtc_connection.Room') as mock_room_class:
            # Mock room instance
            mock_room = Mock()
            mock_room.connect = AsyncMock()
            mock_room.disconnect = AsyncMock()
            mock_room.local_participant = Mock()
            mock_room.local_participant.set_microphone_enabled = AsyncMock()
            mock_room.local_participant.publish_data = AsyncMock()
            mock_room.name = "test-room"
            mock_room_class.return_value = mock_room

            # Create conversation with a conversation token to avoid HTTP calls
            conversation = WebRTCConversation(
                client=mock_client,
                agent_id="test-agent",
                conversation_token="test-token"  # Provide token to avoid fetching
            )

            # Start session
            await conversation.start_session()

            # Test sending user message
            await conversation.send_user_message("Hello, agent!")
            # WebRTC messages are sent via publish_data
            assert mock_room.local_participant.publish_data.called

            # Test sending contextual update
            await conversation.send_contextual_update("Context update")
            assert mock_room.local_participant.publish_data.called

            # Test registering user activity
            await conversation.register_user_activity()
            assert mock_room.local_participant.publish_data.called

    def test_webrtc_connection_creation(self):
        """Test WebRTC connection creation and configuration."""
        # Test with conversation token
        connection = WebRTCConnection(conversation_token="test-token")
        assert connection.conversation_token == "test-token"

        # Test with agent ID
        connection = WebRTCConnection(agent_id="test-agent")
        assert connection.agent_id == "test-agent"

    @pytest.mark.asyncio
    async def test_webrtc_connection_token_fetch(self):
        """Test fetching conversation token from API."""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_response = Mock()
            mock_response.is_success = True
            mock_response.json.return_value = {"token": "fetched-token"}
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__aenter__.return_value = mock_client

            connection = WebRTCConnection(agent_id="test-agent")
            token = await connection._fetch_conversation_token()

            assert token == "fetched-token"
            mock_client.get.assert_called_once_with(
                "https://api.elevenlabs.io/v1/convai/conversation/token?agent_id=test-agent"
            )

    @pytest.mark.asyncio
    async def test_webrtc_connection_token_fetch_error(self):
        """Test error handling when fetching conversation token."""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_response = Mock()
            mock_response.is_success = False
            mock_response.status_code = 404
            mock_response.text = "Not Found"
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__aenter__.return_value = mock_client

            connection = WebRTCConnection(agent_id="test-agent")

            with pytest.raises(Exception, match="Failed to fetch conversation token"):
                await connection._fetch_conversation_token()

    def test_factory_validation(self, mock_client):
        """Test validation in factory functions."""
        from elevenlabs.conversational_ai.conversation import AudioInterface

        # Should raise error for wrong audio interface type with WebRTC
        sync_audio = Mock(spec=AudioInterface)
        with pytest.raises(ValueError, match="WebRTC conversations require an AsyncAudioInterface"):
            create_conversation(
                client=mock_client,
                agent_id="test-agent",
                connection_type=ConnectionType.WEBRTC,
                audio_interface=sync_audio
            )