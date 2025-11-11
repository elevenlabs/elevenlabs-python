from elevenlabs import ElevenLabs


def test_convai_imports():
    client = ElevenLabs(api_key="")
    client.conversational_ai.agents
