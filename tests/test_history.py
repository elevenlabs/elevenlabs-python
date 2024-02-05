from pydoc import cli
import warnings
import pytest


def test_history():
    from elevenlabs import History, HistoryItem
    from elevenlabs.client import ElevenLabs
    
    client = ElevenLabs()

    page_size = 5
    # Test that we can get history
    history = client.history.get_all(page_size=page_size)
    assert isinstance(history, History)


def test_history_item_delete():
    import time
    from random import randint

    from elevenlabs import generate, play
    from elevenlabs.client import ElevenLabs

    # Random text
    text = f"Test {randint(0, 1000)}"
    audio = generate(text=text)  # Generate a history item to delete
    play(audio)
    time.sleep(1)

    client = ElevenLabs()
    history = client.history.get_all().history
    print(history)
    history_item = history[0]
    # Check that item matches
    assert history_item.text == text
    client.history.delete(history_item.history_item_id)
    # Test that the history item was deleted
    history = client.history.get_all(page_size=1).history
    assert len(history) == 0 or history[0].text != text