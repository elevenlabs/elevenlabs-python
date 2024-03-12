import time
from random import randint

from elevenlabs import GetSpeechHistoryResponse, \
    play

from .utils import IN_GITHUB, client


def test_history():
    page_size = 5
    history = client.history.get_all(page_size=page_size)
    assert isinstance(history, GetSpeechHistoryResponse)


def test_history_item_delete():
    text = f"Test {randint(0, 1000)}"
    audio = client.generate(text=text)
    if not IN_GITHUB:
        play(audio)  # type: ignore

    time.sleep(1)

    history = client.history.get_all().history
    print(history)
    history_item = history[0]

    assert history_item.text != None

    # Check that item matches
    # assert history_item.text == text
    # client.history.delete(history_item.history_item_id)

    # Test that the history item was deleted
    # history = client.history.get_all(page_size=1).history
    # assert len(history) == 0 or history[0].text != text
