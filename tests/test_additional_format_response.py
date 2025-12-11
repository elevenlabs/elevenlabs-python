from elevenlabs.types import AdditionalFormatResponseModel

def test_alias_parsing():
    data = {
        "requested_format": "wav",
        "file_extension": "wav",
        "content_type": "audio/wav",
        "is_base64_encoded": True,
        "content": "abcd1234"
    }

    model = AdditionalFormatResponseModel(**data)

    assert model.is_base_64_encoded is True
