from pydantic import ValidationError
import pytest
from elevenlabs import ObjectJsonSchemaPropertyInput


def test_convai_imports():
    # Should raise a validation error (missing required fields) but not a PydanticUserError due to undefined model
    with pytest.raises(ValidationError):
        ObjectJsonSchemaPropertyInput()
