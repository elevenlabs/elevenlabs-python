from elevenlabs import GetSpeechHistoryResponse, ElevenLabs


def test_history():
    client = ElevenLabs()
    page_size = 5
    history = client.history.get_all(page_size=page_size)
    assert isinstance(history, GetSpeechHistoryResponse)
