import pytest
from elevenlabs import ElevenLabs
from elevenlabs.types.agent_config import AgentConfig, PromptAgent
from elevenlabs.types.prompt_agent_tools_item import PromptAgentToolsItem_Webhook, WebhookToolApiSchemaConfig
from elevenlabs.types import LiteralJsonSchemaProperty, ObjectJsonSchemaProperty
from elevenlabs.types.conversational_config import ConversationalConfig

@pytest.fixture
def client():
    """Create an ElevenLabs client fixture."""
    return ElevenLabs()

@pytest.fixture
def webhook_tool():
    """Create a webhook tool configuration fixture."""
    return PromptAgentToolsItem_Webhook(
        type="webhook",
        name="test",
        description="test",
        api_schema=WebhookToolApiSchemaConfig(
            url="https://api.somecompany.com/tools/add-notes",
            method="POST",
            request_body_schema=ObjectJsonSchemaProperty(
                type="object",
                properties={
                    "id": LiteralJsonSchemaProperty(
                        type="string",
                        description="ID for the reservation",
                    ),
                    "notes": LiteralJsonSchemaProperty(
                        type="string",
                        description="notes",
                    ),
                },
                required=["reservation_id", "notes"],
                description="notes that will be added to the reservation with the given ID",
            ),
        )
    )

def test_create_agent(client, webhook_tool):
    """Test creating an agent with the conversational AI client."""
    # Arrange
    agent_config = AgentConfig(
        prompt=PromptAgent(
            tools=[webhook_tool],
            prompt="You are a helpful assistant that can answer questions and help with tasks."
        ),
        model="eleven_multimodal_v2",
        voice_id="21m00Tcm4TlvDq8ikWAM",
    )

    conversational_config = ConversationalConfig(
        agent=agent_config,
    )

    # Act
    response = client.conversational_ai.create_agent(
        name="test_agent",
        conversation_config=conversational_config,
    )

    # Assert
    assert response is not None
    assert response.agent_id is not None
    assert len(response.agent_id) > 0

    # Verify the created agent
    agent = client.conversational_ai.get_agent(response.agent_id)
    assert agent.name == "test_agent"
    assert agent.conversation_config.agent.model == "eleven_multimodal_v2"
    assert agent.conversation_config.agent.voice_id == "21m00Tcm4TlvDq8ikWAM"
    assert agent.conversation_config.agent.prompt.prompt == "You are a helpful assistant that can answer questions and help with tasks."
    
    # Verify webhook tool configuration
    created_tool = agent.conversation_config.agent.prompt.tools[0]
    assert created_tool.type == "webhook"
    assert created_tool.name == "test"
    assert created_tool.description == "test"
    assert created_tool.api_schema.url == "https://api.something.com/tools/add-notes"
    assert created_tool.api_schema.method == "POST"

    # Clean up
    client.conversational_ai.delete_agent(response.agent_id)
