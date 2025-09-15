# WebRTC Support Implementation for ElevenLabs Python SDK

This document summarizes the WebRTC support implementation added to the ElevenLabs Python SDK, following the same architecture as the JavaScript SDK.

## Overview

WebRTC support has been added to enable real-time, low-latency conversations with ElevenLabs agents using the LiveKit WebRTC infrastructure. This provides an alternative to the existing WebSocket-based connections with improved performance for real-time audio applications.

## Files Added

### Core Implementation

1. **`src/elevenlabs/conversational_ai/base_connection.py`**
   - Abstract base class for all connection types
   - Defines the common interface for WebSocket and WebRTC connections
   - Includes `ConnectionType` enum with `WEBSOCKET` and `WEBRTC` options

2. **`src/elevenlabs/conversational_ai/websocket_connection.py`**
   - WebSocket connection implementation extending `BaseConnection`
   - Maintains existing WebSocket functionality in the new architecture

3. **`src/elevenlabs/conversational_ai/webrtc_connection.py`**
   - WebRTC connection implementation using LiveKit Python SDK
   - Handles LiveKit room management, audio tracks, and data channels
   - Supports automatic conversation token fetching from ElevenLabs API

4. **`src/elevenlabs/conversational_ai/connection_factory.py`**
   - Factory functions for creating connections based on type
   - Includes logic for determining connection type based on parameters

5. **`src/elevenlabs/conversational_ai/webrtc_conversation.py`**
   - WebRTC-specific conversation class extending `BaseConversation`
   - Provides async interface for WebRTC conversations
   - Integrates with LiveKit for real-time audio streaming

6. **`src/elevenlabs/conversational_ai/conversation_factory.py`**
   - High-level factory functions for creating different conversation types
   - Includes convenience functions `create_webrtc_conversation()` and `create_websocket_conversation()`
   - Provides unified `create_conversation()` function with connection type selection

### Testing

7. **`tests/test_webrtc_conversation.py`**
   - Comprehensive test suite for WebRTC functionality
   - Tests connection type determination, factory functions, and conversation lifecycle
   - Includes mocked LiveKit integration tests

### Examples

8. **`examples/webrtc_conversation_example.py`**
   - Complete working examples of WebRTC conversation usage
   - Shows both explicit token and automatic token fetching approaches
   - Demonstrates the differences between WebSocket and WebRTC connections

## Files Modified

### Dependencies

1. **`pyproject.toml`**
   - Added `livekit = ">=0.15.0"` dependency for WebRTC support

### Core Conversation Module

2. **`src/elevenlabs/conversational_ai/conversation.py`**
   - Updated `ConversationInitiationData` to include `connection_type` and `conversation_token` parameters
   - Added imports for the new connection system
   - Added helper methods `_determine_connection_type()` and `_create_connection()` to `BaseConversation`

## Key Features

### Connection Types

- **WebSocket (existing)**: Traditional WebSocket-based connections
- **WebRTC (new)**: Real-time connections using LiveKit infrastructure

### Authentication Methods

- **Agent ID**: For public agents, no additional authentication required
- **Conversation Token**: For private agents, obtained from ElevenLabs API
- **Automatic Token Fetching**: SDK can automatically fetch tokens when agent ID is provided

### API Design

The implementation follows the same patterns as the JavaScript SDK:

```python
# WebRTC conversation with explicit token
conversation = create_webrtc_conversation(
    client=client,
    agent_id="your-agent-id",
    conversation_token="your-token",
    audio_interface=async_audio_interface,
    callback_agent_response=on_response
)

# WebRTC conversation with automatic token fetching
conversation = create_webrtc_conversation(
    client=client,
    agent_id="your-agent-id",  # Token will be fetched automatically
    audio_interface=async_audio_interface
)

# Generic factory with connection type
conversation = create_conversation(
    client=client,
    agent_id="your-agent-id",
    connection_type=ConnectionType.WEBRTC,
    audio_interface=async_audio_interface
)
```

### Backward Compatibility

- All existing WebSocket-based conversation code continues to work unchanged
- New connection types are opt-in through explicit parameters
- Default behavior remains WebSocket connections

## Technical Architecture

### Connection Hierarchy

```
BaseConnection (abstract)
├── WebSocketConnection
└── WebRTCConnection (uses LiveKit)
```

### Conversation Hierarchy

```
BaseConversation
├── Conversation (sync WebSocket)
├── AsyncConversation (async WebSocket)
└── WebRTCConversation (async WebRTC)
```

### Factory Pattern

The implementation uses factory functions to create appropriate conversation types based on:
- Explicit connection type parameter
- Presence of conversation token (implies WebRTC)
- Audio interface type (sync vs async)
- Callback function types (sync vs async)

## Benefits of WebRTC Implementation

1. **Lower Latency**: Direct peer-to-peer audio streaming
2. **Better Audio Quality**: Optimized for real-time audio
3. **Reduced Server Load**: Audio doesn't go through application servers
4. **Adaptive Bitrate**: Automatic quality adjustment based on network conditions
5. **Better Connectivity**: NAT traversal and firewall handling

## Usage Examples

### Basic WebRTC Conversation

```python
import asyncio
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation_factory import create_webrtc_conversation

async def main():
    client = ElevenLabs(api_key="your-api-key")

    conversation = create_webrtc_conversation(
        client=client,
        agent_id="your-agent-id",
        audio_interface=YourAsyncAudioInterface(),
    )

    await conversation.start_session()
    await conversation.send_user_message("Hello!")
    # ... conversation logic
    await conversation.end_session()

asyncio.run(main())
```

### Connection Type Comparison

```python
# WebSocket (existing)
ws_conversation = create_conversation(
    client=client,
    agent_id="agent-id",
    connection_type=ConnectionType.WEBSOCKET,
    audio_interface=SyncAudioInterface()  # Sync interface
)

# WebRTC (new)
webrtc_conversation = create_conversation(
    client=client,
    agent_id="agent-id",
    connection_type=ConnectionType.WEBRTC,
    audio_interface=AsyncAudioInterface()  # Async interface required
)
```

## Testing

The implementation includes comprehensive tests covering:

- Connection type determination logic
- Factory function behavior
- WebRTC conversation lifecycle
- Message handling
- Error conditions
- Token fetching

All tests use proper mocking to avoid external dependencies during testing.

## Future Considerations

1. **Audio Interface Implementations**: Additional concrete audio interface implementations for common use cases
2. **Advanced WebRTC Features**: Support for video, screen sharing, or advanced audio processing
3. **Monitoring and Analytics**: Integration with LiveKit's monitoring features
4. **Connection Fallback**: Automatic fallback from WebRTC to WebSocket in case of connection issues

## Migration Guide

For users wanting to upgrade from WebSocket to WebRTC:

1. Install the updated SDK with `livekit` dependency
2. Update audio interface to async (`AsyncAudioInterface`)
3. Update callback functions to async
4. Change connection type to `ConnectionType.WEBRTC`
5. Provide conversation token or agent ID for authentication

The migration is non-breaking - existing code continues to work without changes.