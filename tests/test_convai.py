from unittest.mock import MagicMock, patch
from elevenlabs.conversational_ai.conversation import Conversation, AudioInterface, ConversationInitiationData
import json
import time


class MockAudioInterface(AudioInterface):
    def start(self, input_callback):
        print("Audio interface started")
        self.input_callback = input_callback

    def stop(self):
        print("Audio interface stopped")

    def output(self, audio):
        print(f"Would play audio of length: {len(audio)} bytes")

    def interrupt(self):
        print("Audio interrupted")


# Add test constants and helpers at module level
TEST_CONVERSATION_ID = "test123"
TEST_AGENT_ID = "test_agent"


def create_mock_websocket(messages=None):
    """Helper to create a mock websocket with predefined responses"""
    mock_ws = MagicMock()

    if messages is None:
        messages = [
            {
                "type": "conversation_initiation_metadata",
                "conversation_initiation_metadata_event": {"conversation_id": TEST_CONVERSATION_ID},
            },
            {"type": "agent_response", "agent_response_event": {"agent_response": "Hello there!"}},
        ]

    def response_generator():
        for msg in messages:
            yield json.dumps(msg)
        while True:
            yield '{"type": "keep_alive"}'

    mock_ws.recv = MagicMock(side_effect=response_generator())
    return mock_ws


def test_conversation_basic_flow():
    # Mock setup
    mock_ws = create_mock_websocket()
    mock_client = MagicMock()
    agent_response_callback = MagicMock()

    # Setup the conversation
    conversation = Conversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=MockAudioInterface(),
        callback_agent_response=agent_response_callback,
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_ws
        conversation.start_session()

        # Add a wait for the callback to be called
        timeout = 5  # 5 seconds timeout
        start_time = time.time()
        while not agent_response_callback.called and time.time() - start_time < timeout:
            time.sleep(0.1)

        conversation.end_session()
        conversation.wait_for_session_end()

    # Assertions
    expected_init_message = {
        "type": "conversation_initiation_client_data",
        "custom_llm_extra_body": {},
        "conversation_config_override": {},
        "dynamic_variables": {},
    }
    mock_ws.send.assert_any_call(json.dumps(expected_init_message))
    agent_response_callback.assert_called_once_with("Hello there!")
    assert conversation._conversation_id == TEST_CONVERSATION_ID


def test_conversation_with_auth():
    # Mock setup
    mock_client = MagicMock()
    mock_client.conversational_ai.get_signed_url.return_value.signed_url = "wss://signed.url"
    mock_ws = create_mock_websocket(
        [
            {
                "type": "conversation_initiation_metadata",
                "conversation_initiation_metadata_event": {"conversation_id": TEST_CONVERSATION_ID},
            }
        ]
    )

    conversation = Conversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        requires_auth=True,
        audio_interface=MockAudioInterface(),
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_ws
        conversation.start_session()
        conversation.end_session()
        conversation.wait_for_session_end()

    # Assertions
    mock_client.conversational_ai.get_signed_url.assert_called_once_with(agent_id=TEST_AGENT_ID)

def test_conversation_with_dynamic_variables():
    # Mock setup
    mock_ws = create_mock_websocket()
    mock_client = MagicMock()
    agent_response_callback = MagicMock()

    dynamic_variables = {"name": "angelo"}
    config = ConversationInitiationData(dynamic_variables=dynamic_variables)

    # Setup the conversation
    conversation = Conversation(
        client=mock_client,
        config=config,
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=MockAudioInterface(),
        callback_agent_response=agent_response_callback,
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_ws
        conversation.start_session()

        # Add a wait for the callback to be called
        timeout = 5  # 5 seconds timeout
        start_time = time.time()
        while not agent_response_callback.called and time.time() - start_time < timeout:
            time.sleep(0.1)

        conversation.end_session()
        conversation.wait_for_session_end()

    # Assertions
    expected_init_message = {
        "type": "conversation_initiation_client_data",
        "custom_llm_extra_body": {},
        "conversation_config_override": {},
        "dynamic_variables": {
            "name": "angelo"
        },
    }
    mock_ws.send.assert_any_call(json.dumps(expected_init_message))
    agent_response_callback.assert_called_once_with("Hello there!")
    assert conversation._conversation_id == TEST_CONVERSATION_ID