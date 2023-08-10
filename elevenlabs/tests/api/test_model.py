import pytest
import asyncio


def test_model():
    from elevenlabs import Model, Models

    # Test that we can get all models
    models = Models.from_api()
    assert isinstance(models, Models)
    assert len(models) > 0
    assert isinstance(models[0], Model)


@pytest.mark.asyncio
async def test_amodel():
    from elevenlabs import Model, Models

    # Test that we can get all models
    models = await Models.afrom_api()
    assert isinstance(models, Models)
    assert len(models) > 0
    assert isinstance(models[0], Model)


@pytest.mark.asyncio
async def test_gather_model():
    from elevenlabs import Model, Models

    gather_models = await asyncio.gather(*[Models.afrom_api() for _ in range(10)])
    # Test that we can get all models

    for models in gather_models:
        assert isinstance(models, Models)
        assert len(models) > 0
        assert isinstance(models[0], Model)
