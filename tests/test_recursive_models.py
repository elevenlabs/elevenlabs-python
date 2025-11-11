from elevenlabs import AgentWorkflowRequestModel, ObjectJsonSchemaPropertyInput, ObjectJsonSchemaPropertyOutput


def test_recursive_models():
    # Should be able to import and use the recursive types without PydanticUserError
    # ObjectJsonSchemaPropertyInput has no required fields, so it can be instantiated
    ObjectJsonSchemaPropertyInput()
    
    ObjectJsonSchemaPropertyOutput()

    AgentWorkflowRequestModel()
