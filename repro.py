from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="foo")

client.conversational_ai.agents.list()
