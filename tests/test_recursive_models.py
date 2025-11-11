from elevenlabs import ObjectJsonSchemaPropertyInput


def test_recursive_models():
    # Should be able to import and use the recursive types without PydanticUserError
    # ObjectJsonSchemaPropertyInput has no required fields, so it can be instantiated
    obj = ObjectJsonSchemaPropertyInput()
    assert obj is not None
