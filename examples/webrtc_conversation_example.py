#!/usr/bin/env python3
"""
Example demonstrating WebRTC conversation support in the ElevenLabs Python SDK.

This example shows how to use the new WebRTC connection type for real-time
conversations with ElevenLabs agents using LiveKit.
"""

import asyncio
import os
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation_factory import create_webrtc_conversation
from elevenlabs.conversational_ai.conversation import AsyncAudioInterface
from elevenlabs.conversational_ai.base_connection import ConnectionType


class SimpleAsyncAudioInterface(AsyncAudioInterface):
    """A simple example audio interface for WebRTC conversations."""

    async def start(self, input_callback):
        """Start the audio interface with input callback."""
        print("Audio interface started")
        self.input_callback = input_callback
        # In a real implementation, you would set up audio capture here

    async def stop(self):
        """Stop the audio interface."""
        print("Audio interface stopped")
        # In a real implementation, you would clean up audio resources here

    async def output(self, audio: bytes):
        """Output audio to the user."""
        print(f"Received audio output: {len(audio)} bytes")
        # In a real implementation, you would play the audio here

    async def interrupt(self):
        """Handle interruption signal."""
        print("Audio output interrupted")
        # In a real implementation, you would stop current audio playback here


async def webrtc_conversation_example():
    """Example of using WebRTC conversation with ElevenLabs."""

    # Initialize the ElevenLabs client
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    # Create audio interface
    audio_interface = SimpleAsyncAudioInterface()

    # Define callback functions
    async def on_agent_response(response: str):
        print(f"Agent: {response}")

    async def on_user_transcript(transcript: str):
        print(f"User: {transcript}")

    async def on_session_end():
        print("Conversation session ended")

    # Example 1: WebRTC conversation with conversation token
    print("Example 1: WebRTC conversation with explicit token")
    conversation_token = "your-conversation-token"  # Get this from your server

    conversation = create_webrtc_conversation(
        client=client,
        agent_id="your-agent-id",
        conversation_token=conversation_token,
        audio_interface=audio_interface,
        callback_agent_response=on_agent_response,
        callback_user_transcript=on_user_transcript,
        callback_end_session=on_session_end,
    )

    try:
        # Start the conversation
        await conversation.start_session()
        print("WebRTC conversation started!")

        # Send a message to the agent
        await conversation.send_user_message("Hello, how are you today?")

        # Keep the conversation running for a bit
        await asyncio.sleep(10)

        # Send contextual information
        await conversation.send_contextual_update("The user seems interested in learning about WebRTC")

        # Keep running for a bit more
        await asyncio.sleep(5)

    finally:
        # End the conversation
        await conversation.end_session()
        print("Conversation ended")


async def auto_fetch_token_example():
    """Example of WebRTC conversation with automatic token fetching."""

    print("\nExample 2: WebRTC conversation with automatic token fetching")

    # Initialize the ElevenLabs client
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    # Create audio interface
    audio_interface = SimpleAsyncAudioInterface()

    # Define callback functions
    async def on_agent_response(response: str):
        print(f"Agent: {response}")

    # Create WebRTC conversation without explicit token - it will be fetched automatically
    conversation = create_webrtc_conversation(
        client=client,
        agent_id="your-agent-id",  # Make sure this agent exists and you have access
        audio_interface=audio_interface,
        callback_agent_response=on_agent_response,
    )

    try:
        # Start the conversation (token will be fetched automatically)
        await conversation.start_session()
        print("WebRTC conversation started with auto-fetched token!")

        # Send a message
        await conversation.send_user_message("Tell me about WebRTC advantages over WebSockets")

        # Wait for response
        await asyncio.sleep(10)

    except Exception as e:
        print(f"Error in conversation: {e}")

    finally:
        # End the conversation
        await conversation.end_session()


async def compare_connection_types():
    """Example showing the difference between WebSocket and WebRTC connections."""

    print("\nExample 3: Comparing connection types")

    from elevenlabs.conversational_ai.conversation_factory import create_conversation

    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    # WebSocket conversation (traditional)
    print("Creating WebSocket conversation...")
    ws_conversation = create_conversation(
        client=client,
        agent_id="your-agent-id",
        connection_type=ConnectionType.WEBSOCKET,
        # Note: WebSocket conversations use AudioInterface (sync), not AsyncAudioInterface
    )
    print(f"WebSocket conversation type: {type(ws_conversation)}")

    # WebRTC conversation (new)
    print("Creating WebRTC conversation...")
    webrtc_conversation = create_conversation(
        client=client,
        agent_id="your-agent-id",
        connection_type=ConnectionType.WEBRTC,
        conversation_token="your-token",  # Required for WebRTC
        audio_interface=SimpleAsyncAudioInterface(),
    )
    print(f"WebRTC conversation type: {type(webrtc_conversation)}")

    print("\nKey differences:")
    print("- WebSocket: Uses sync AudioInterface, established WebSocket protocol")
    print("- WebRTC: Uses AsyncAudioInterface, lower latency, real-time audio streaming")


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("Please set the ELEVENLABS_API_KEY environment variable")
        exit(1)

    print("ElevenLabs WebRTC Conversation Examples")
    print("=" * 40)

    # Run the examples
    asyncio.run(webrtc_conversation_example())
    asyncio.run(auto_fetch_token_example())
    asyncio.run(compare_connection_types())

    print("\nAll examples completed!")