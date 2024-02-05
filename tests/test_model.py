import pytest


def test_model():
    from elevenlabs import Model
    from elevenlabs.client import ElevenLabs
    
    client = ElevenLabs()

    # Test that we can get all models
    models = client.models.get_all()
    print(models)
    assert len(models) > 0
    assert isinstance(models[0], Model)