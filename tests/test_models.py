from elevenlabs import Model
from elevenlabs.client import ElevenLabs


def test_models():
    client = ElevenLabs()
    models = client.models.get_all()
    assert len(models) > 0
    assert isinstance(models[0], Model)
