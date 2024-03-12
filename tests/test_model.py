from elevenlabs import Model
from .utils import client


def test_model():
    # Test that we can get all models
    models = client.models.get_all()
    print(models)
    assert len(models) > 0
    assert isinstance(models[0], Model)