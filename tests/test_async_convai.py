import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from elevenlabs.conversational_ai.conversation import (
    AsyncConversation,
    AsyncAudioInterface,
    ConversationInitiationData,
)


class MockAsyncAudioInterface(AsyncAudioInterface):
    async def start(self, input_callback):
        print("Async audio interface started")
        self.input_callback = input_callback

    async def stop(self):
        print("Async audio interface stopped")

    async def output(self, audio):
        print(f"Would play audio of length: {len(audio)} bytes")

    async def interrupt(self):
        print("Async audio interrupted")


# Add test constants and helpers at module level
TEST_CONVERSATION_ID = "test123"
TEST_AGENT_ID = "test_agent"


def create_mock_async_websocket(messages=None):
    """Helper to create a mock async websocket with predefined responses"""
    mock_ws = AsyncMock()

    if messages is None:
        messages = [
            {
                "type": "conversation_initiation_metadata",
                "conversation_initiation_metadata_event": {"conversation_id": TEST_CONVERSATION_ID},
            },
            {"type": "agent_response", "agent_response_event": {"agent_response": "Hello there!"}},
        ]

    # Convert messages to JSON strings
    json_messages = [json.dumps(msg) for msg in messages]
    json_messages.extend(['{"type": "keep_alive"}'] * 10)  # Add some keep-alive messages

    # Create an iterator
    message_iter = iter(json_messages)

    async def mock_recv():
        try:
            return next(message_iter)
        except StopIteration:
            # Simulate connection close after messages
            raise asyncio.TimeoutError()

    mock_ws.recv = mock_recv
    return mock_ws


@pytest.mark.asyncio
async def test_async_conversation_basic_flow():
    # Mock setup
    mock_ws = create_mock_async_websocket()
    mock_client = MagicMock()
    agent_response_callback = AsyncMock()
    test_user_id = "test_user_123"

    # Setup the conversation
    config = ConversationInitiationData(user_id=test_user_id)
    conversation = AsyncConversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        config=config,
        requires_auth=False,
        audio_interface=MockAsyncAudioInterface(),
        callback_agent_response=agent_response_callback,
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.websockets.connect") as mock_connect:
        mock_connect.return_value.__aenter__.return_value = mock_ws

        await conversation.start_session()

        # Wait a bit for the callback to be called
        await asyncio.sleep(0.1)

        await conversation.end_session()
        await conversation.wait_for_session_end()

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


@pytest.mark.asyncio
async def test_async_conversation_with_auth():
    # Mock setup
    mock_client = MagicMock()
    mock_client.conversational_ai.conversations.get_signed_url.return_value.signed_url = "wss://signed.url"
    mock_ws = create_mock_async_websocket(
        [
            {
                "type": "conversation_initiation_metadata",
                "conversation_initiation_metadata_event": {"conversation_id": TEST_CONVERSATION_ID},
            }
        ]
    )

    conversation = AsyncConversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        requires_auth=True,
        audio_interface=MockAsyncAudioInterface(),
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.websockets.connect") as mock_connect:
        mock_connect.return_value.__aenter__.return_value = mock_ws

        await conversation.start_session()
        await conversation.end_session()
        await conversation.wait_for_session_end()

    # Assertions
    mock_client.conversational_ai.conversations.get_signed_url.assert_called_once_with(agent_id=TEST_AGENT_ID)


@pytest.mark.asyncio
async def test_async_conversation_with_dynamic_variables():
    # Mock setup
    mock_ws = create_mock_async_websocket()
    mock_client = MagicMock()
    agent_response_callback = AsyncMock()

    dynamic_variables = {"name": "angelo"}
    config = ConversationInitiationData(dynamic_variables=dynamic_variables)

    # Setup the conversation
    conversation = AsyncConversation(
        client=mock_client,
        config=config,
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=MockAsyncAudioInterface(),
        callback_agent_response=agent_response_callback,
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.websockets.connect") as mock_connect:
        mock_connect.return_value.__aenter__.return_value = mock_ws

        await conversation.start_session()

        # Wait a bit for the callback to be called
        await asyncio.sleep(0.1)

        await conversation.end_session()
        await conversation.wait_for_session_end()

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


@pytest.mark.asyncio
async def test_async_conversation_with_contextual_update():
    # Mock setup
    mock_ws = create_mock_async_websocket([])
    mock_client = MagicMock()

    # Setup the conversation
    conversation = AsyncConversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=MockAsyncAudioInterface(),
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.websockets.connect") as mock_connect:
        mock_connect.return_value.__aenter__.return_value = mock_ws

        await conversation.start_session()
        await asyncio.sleep(0.1)

        await conversation.send_contextual_update("User appears to be looking at pricing page")

        # Teardown
        await conversation.end_session()
        await conversation.wait_for_session_end()

    # Assertions
    expected = json.dumps({"type": "contextual_update", "text": "User appears to be looking at pricing page"})
    mock_ws.send.assert_any_call(expected)


@pytest.mark.asyncio
async def test_async_conversation_send_user_message():
    # Mock setup
    mock_ws = create_mock_async_websocket([])
    mock_client = MagicMock()

    # Setup the conversation
    conversation = AsyncConversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=MockAsyncAudioInterface(),
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.websockets.connect") as mock_connect:
        mock_connect.return_value.__aenter__.return_value = mock_ws

        await conversation.start_session()
        await asyncio.sleep(0.1)

        await conversation.send_user_message("Hello, how are you?")

        # Teardown
        await conversation.end_session()
        await conversation.wait_for_session_end()

    # Assertions
    expected = json.dumps({"type": "user_message", "text": "Hello, how are you?"})
    mock_ws.send.assert_any_call(expected)


@pytest.mark.asyncio
async def test_async_conversation_register_user_activity():
    # Mock setup
    mock_ws = create_mock_async_websocket([])
    mock_client = MagicMock()

    # Setup the conversation
    conversation = AsyncConversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=MockAsyncAudioInterface(),
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.websockets.connect") as mock_connect:
        mock_connect.return_value.__aenter__.return_value = mock_ws

        await conversation.start_session()
        await asyncio.sleep(0.1)

        await conversation.register_user_activity()

        # Teardown
        await conversation.end_session()
        await conversation.wait_for_session_end()

    # Assertions
    expected = json.dumps({"type": "user_activity"})
    mock_ws.send.assert_any_call(expected)


@pytest.mark.asyncio
async def test_async_conversation_callback_flows():
    # Mock setup for testing all callback types
    messages = [
        {
            "type": "conversation_initiation_metadata",
            "conversation_initiation_metadata_event": {"conversation_id": TEST_CONVERSATION_ID},
        },
        {"type": "agent_response", "agent_response_event": {"agent_response": "Hello there!"}},
        {
            "type": "agent_response_correction",
            "agent_response_correction_event": {
                "original_agent_response": "Hello ther!",
                "corrected_agent_response": "Hello there!"
            }
        },
        {
            "type": "user_transcript",
            "user_transcription_event": {"user_transcript": "Hi, how are you?"}
        },
        {
            "type": "ping",
            "ping_event": {"event_id": "123", "ping_ms": 50}
        },
        {
            "type": "interruption",
            "interruption_event": {"event_id": "456"}
        },
        {
            "type": "audio",
            "audio_event": {"event_id": "789", "audio_base_64": "dGVzdA=="}  # "test" in base64
        }
    ]

    mock_ws = create_mock_async_websocket(messages)
    mock_client = MagicMock()

    # Setup callbacks
    agent_response_callback = AsyncMock()
    agent_response_correction_callback = AsyncMock()
    user_transcript_callback = AsyncMock()
    latency_measurement_callback = AsyncMock()
    end_session_callback = AsyncMock()

    # Setup the conversation
    conversation = AsyncConversation(
        client=mock_client,
        agent_id=TEST_AGENT_ID,
        requires_auth=False,
        audio_interface=MockAsyncAudioInterface(),
        callback_agent_response=agent_response_callback,
        callback_agent_response_correction=agent_response_correction_callback,
        callback_user_transcript=user_transcript_callback,
        callback_latency_measurement=latency_measurement_callback,
        callback_end_session=end_session_callback,
    )

    # Run the test
    with patch("elevenlabs.conversational_ai.conversation.websockets.connect") as mock_connect:
        mock_connect.return_value.__aenter__.return_value = mock_ws

        await conversation.start_session()

        # Wait for callbacks to be processed
        await asyncio.sleep(0.2)

        await conversation.end_session()
        await conversation.wait_for_session_end()

    # Assertions
    agent_response_callback.assert_called_with("Hello there!")
    agent_response_correction_callback.assert_called_with("Hello ther!", "Hello there!")
    user_transcript_callback.assert_called_with("Hi, how are you?")
    latency_measurement_callback.assert_called_with(50)
    end_session_callback.assert_called_once()
    assert conversation._conversation_id == TEST_CONVERSATION_ID
    assert conversation._last_interrupt_id == 456


@pytest.mark.asyncio
async def test_async_conversation_wss_url_generation_without_get_environment():

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

        conversation = AsyncConversation(
            client=mock_client,
            agent_id=TEST_AGENT_ID,
            requires_auth=False,
            audio_interface=MockAsyncAudioInterface()
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
