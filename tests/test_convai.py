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
    test_user_id = "test_user_123"

    # Setup the conversation
    config = ConversationInitiationData(user_id=test_user_id)
    conversation = Conversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        config=config,
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

    # Assertions - check the call was made with the right structure
    send_calls = [call[0][0] for call in mock_ws.send.call_args_list]
    init_messages = [json.loads(call) for call in send_calls if 'conversation_initiation_client_data' in call]
    assert len(init_messages) == 1
    init_message = init_messages[0]

    assert init_message["type"] == "conversation_initiation_client_data"
    assert init_message["custom_llm_extra_body"] == {}
    assert init_message["conversation_config_override"] == {}
    assert init_message["dynamic_variables"] == {}
    assert init_message["source_info"]["source"] == "python_sdk"
    assert "version" in init_message["source_info"]
    assert init_message["user_id"] == test_user_id
    agent_response_callback.assert_called_once_with("Hello there!")
    assert conversation._conversation_id == TEST_CONVERSATION_ID
    assert conversation.config.user_id == test_user_id


def test_conversation_with_auth():
    # Mock setup
    mock_client = MagicMock()
    mock_client.conversational_ai.conversations.get_signed_url.return_value.signed_url = "wss://signed.url"
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
    mock_client.conversational_ai.conversations.get_signed_url.assert_called_once_with(agent_id=TEST_AGENT_ID)


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

    # Assertions - check the call was made with the right structure
    send_calls = [call[0][0] for call in mock_ws.send.call_args_list]
    init_messages = [json.loads(call) for call in send_calls if 'conversation_initiation_client_data' in call]
    assert len(init_messages) == 1
    init_message = init_messages[0]

    assert init_message["type"] == "conversation_initiation_client_data"
    assert init_message["custom_llm_extra_body"] == {}
    assert init_message["conversation_config_override"] == {}
    assert init_message["dynamic_variables"] == {"name": "angelo"}
    assert init_message["source_info"]["source"] == "python_sdk"
    assert "version" in init_message["source_info"]
    agent_response_callback.assert_called_once_with("Hello there!")
    assert conversation._conversation_id == TEST_CONVERSATION_ID


def test_conversation_with_contextual_update():
    # Mock setup
    mock_ws = create_mock_websocket([])
    mock_client = MagicMock()

    # Setup the conversation
    conversation = Conversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=MockAudioInterface(),
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_ws

        conversation.start_session()
        time.sleep(0.1)

        conversation.send_contextual_update("User appears to be looking at pricing page")

        # Teardown
        conversation.end_session()
        conversation.wait_for_session_end()

    # Assertions
    expected = json.dumps({"type": "contextual_update", "text": "User appears to be looking at pricing page"})
    mock_ws.send.assert_any_call(expected)


def test_conversation_wss_url_generation_without_get_environment():

    from elevenlabs.core.client_wrapper import SyncClientWrapper

    # Test with various base URL formats to ensure robustness
    test_cases = [
        ("https://api.elevenlabs.io", "wss://api.elevenlabs.io"),
        ("https://api.us.elevenlabs.io", "wss://api.us.elevenlabs.io"),
        ("https://api.eu.residency.elevenlabs.io", "wss://api.eu.residency.elevenlabs.io"),
        ("http://localhost:8000", "ws://localhost:8000"),
    ]

    for base_url, expected_ws_base in test_cases:
        # Create a real SyncClientWrapper to ensure it doesn't have get_environment method
        mock_client = MagicMock()
        mock_client._client_wrapper = SyncClientWrapper(
            base_url=base_url,
            api_key="test_key",
            httpx_client=MagicMock(),
            timeout=30.0
        )

        # Create conversation with requires_auth=False
        conversation = Conversation(
            client=mock_client,
            agent_id=TEST_AGENT_ID,
            requires_auth=False,
            audio_interface=MockAudioInterface()
        )

        try:
            wss_url = conversation._get_wss_url()

            # Verify the URL is correctly generated
            expected_url = f"{expected_ws_base}/v1/convai/conversation?agent_id={TEST_AGENT_ID}&source=python_sdk&version="
            assert wss_url.startswith(expected_url), f"URL should start with {expected_url}, got {wss_url}"

            # Verify the URL contains version parameter
            assert "version=" in wss_url, f"URL should contain version parameter, got {wss_url}"

        except AttributeError as e:
            if "get_environment" in str(e):
                assert False
            else:
                raise  # Re-raise if it's a different AttributeError

        except Exception as e:
            assert False, f"Unexpected error generating WebSocket URL: {e}"
