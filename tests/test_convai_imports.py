from elevenlabs import ElevenLabs


def test_convai_imports():
    client = ElevenLabs(api_key="test")
    client.conversational_ai.agents
