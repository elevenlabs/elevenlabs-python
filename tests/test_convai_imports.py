def test_convai_imports():
    from elevenlabs import ElevenLabs
    client = ElevenLabs(api_key="")
    # Just access the property to trigger the import chain
    _ = client.conversational_ai.agents
