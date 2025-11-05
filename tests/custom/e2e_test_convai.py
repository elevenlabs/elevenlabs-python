import os
import time
import asyncio

import pytest
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skip live conversation test in CI environment")
def test_live_conversation():
    """Test a live conversation with actual audio I/O"""

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable missing.")

    agent_id = os.getenv("AGENT_ID")
    if not api_key or not agent_id:
        raise ValueError("AGENT_ID environment variable missing.")

    client = ElevenLabs(api_key=api_key)

    # Create conversation handlers
    def on_agent_response(text: str):
        print(f"Agent: {text}")

    def on_user_transcript(text: str):
        print(f"You: {text}")

    def on_latency(ms: int):
        print(f"Latency: {ms}ms")

    # Initialize client tools
    client_tools = ClientTools()

    def test(parameters):
        print("Sync tool called with parameters:", parameters)
        return "Tool called successfully"

    async def test_async(parameters):
        # Simulate some async work
        await asyncio.sleep(10)
        print("Async tool called with parameters:", parameters)
        return "Tool called successfully"

    client_tools.register("test", test)
    client_tools.register("test_async", test_async, is_async=True)

    # Initialize conversation
    conversation = Conversation(
        client=client,
        agent_id=agent_id,
        requires_auth=False,
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=on_agent_response,
        callback_user_transcript=on_user_transcript,
        callback_latency_measurement=on_latency,
        client_tools=client_tools,
    )

    # Start the conversation
    conversation.start_session()

    # Let it run for 100 seconds
    time.sleep(100)

    # End the conversation
    conversation.end_session()
    conversation.wait_for_session_end()

    # Get the conversation ID for reference
    conversation_id = conversation._conversation_id
    print(f"Conversation ID: {conversation_id}")


if __name__ == "__main__":
    test_live_conversation()
