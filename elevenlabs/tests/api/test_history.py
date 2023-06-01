import warnings


def test_history():
    from elevenlabs import History, HistoryItem

    page_size = 5
    # Test that we can get history
    history = History.from_api(page_size=page_size)
    assert isinstance(history, History)

    # Test that we lazily can iterate over multiple pages
    it = iter(history)
    for i in range(page_size * 3):
        try:
            assert isinstance(next(it), HistoryItem)
        except StopIteration:
            warnings.warn("Warning: not enough history items to test multiple pages.")
            break
