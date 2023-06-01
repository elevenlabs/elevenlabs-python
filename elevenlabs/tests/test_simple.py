from .utils import no_api_key, repeat_test_without_api_key


def test_api_key():
    from elevenlabs import get_api_key

    assert get_api_key() is not None
    with no_api_key():
        assert get_api_key() is None
    assert get_api_key() is not None


@repeat_test_without_api_key
def test_voices():
    from elevenlabs import voices

    # Test that we can get all voices
    all_voices = voices()
    assert len(all_voices) > 0
