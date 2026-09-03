import json
from unittest.mock import MagicMock

import pytest

from elevenlabs.agents.conversation import (
    AudioInterface,
    Conversation,
    OrchestratorConfig,
    PostCallWebhookConfig,
)


class MockAudioInterface(AudioInterface):
    def start(self, input_callback):
        self.input_callback = input_callback

    def stop(self):
        pass

    def output(self, audio):
        pass

    def interrupt(self):
        pass


def _make_conversation(orchestrator_config: OrchestratorConfig) -> Conversation:
    mock_client = MagicMock()
    mock_client._client_wrapper.get_base_url.return_value = "https://api.elevenlabs.io"
    return Conversation(
        client=mock_client,
        agent_id="",
        requires_auth=False,
        audio_interface=MockAudioInterface(),
        # Mocked so the constructor's client_tools.start() does not spawn a real
        # event-loop thread; these tests only exercise message serialization.
        client_tools=MagicMock(),
        orchestrator_config=orchestrator_config,
    )


def test_post_call_webhook_config_to_dict():
    assert PostCallWebhookConfig(url="https://example.com/hook").to_dict() == {"url": "https://example.com/hook"}
    assert PostCallWebhookConfig(url="https://example.com/hook", hmac_secret="0123456789abcdef").to_dict() == {
        "url": "https://example.com/hook",
        "hmac_secret": "0123456789abcdef",
    }


def test_on_prem_initiation_message_includes_typed_webhooks():
    conversation = _make_conversation(
        OrchestratorConfig(
            url="ws://localhost:8000/sagemaker/convai/conversation",
            post_call_transcription_webhook=PostCallWebhookConfig(
                url="https://example.com/transcript", hmac_secret="0123456789abcdef"
            ),
            post_call_audio_webhook=PostCallWebhookConfig(url="https://example.com/audio"),
        )
    )

    message = json.loads(conversation._create_orchestrator_initiation_message())

    assert message["type"] == "enclave_setup_config"
    assert message["post_call_transcription_webhook"] == {
        "url": "https://example.com/transcript",
        "hmac_secret": "0123456789abcdef",
    }
    assert message["post_call_audio_webhook"] == {"url": "https://example.com/audio"}
    assert message["post_call_transcription_webhook_url"] is None
    assert message["post_call_audio_webhook_url"] is None


def test_on_prem_initiation_message_omits_typed_webhooks_when_unset():
    conversation = _make_conversation(
        OrchestratorConfig(
            url="ws://localhost:8000/sagemaker/convai/conversation",
            post_call_transcription_webhook_url="https://example.com/transcript",
        )
    )

    message = json.loads(conversation._create_orchestrator_initiation_message())

    assert "post_call_transcription_webhook" not in message
    assert "post_call_audio_webhook" not in message
    assert message["post_call_transcription_webhook_url"] == "https://example.com/transcript"


def test_on_prem_initiation_data_rejects_legacy_and_typed_transcription_webhook():
    with pytest.raises(ValueError, match="not both"):
        OrchestratorConfig(
            url="ws://localhost:8000/sagemaker/convai/conversation",
            post_call_transcription_webhook_url="https://example.com/hook",
            post_call_transcription_webhook=PostCallWebhookConfig(url="https://example.com/hook"),
        )


def test_on_prem_initiation_data_rejects_legacy_and_typed_audio_webhook():
    with pytest.raises(ValueError, match="not both"):
        OrchestratorConfig(
            url="ws://localhost:8000/sagemaker/convai/conversation",
            post_call_audio_webhook_url="https://example.com/hook",
            post_call_audio_webhook=PostCallWebhookConfig(url="https://example.com/hook"),
        )


def test_on_prem_initiation_message_includes_bedrock_inference_profile():
    conversation = _make_conversation(
        OrchestratorConfig(
            url="ws://localhost:8000/sagemaker/convai/conversation",
            bedrock_inference_profile="global",
        )
    )

    message = json.loads(conversation._create_orchestrator_initiation_message())

    assert message["bedrock_inference_profile"] == "global"


def test_on_prem_initiation_message_omits_bedrock_inference_profile_when_unset():
    conversation = _make_conversation(
        OrchestratorConfig(url="ws://localhost:8000/sagemaker/convai/conversation")
    )

    message = json.loads(conversation._create_orchestrator_initiation_message())

    assert "bedrock_inference_profile" not in message


def test_on_prem_initiation_message_merges_extra_setup_config():
    conversation = _make_conversation(
        OrchestratorConfig(
            url="ws://localhost:8000/sagemaker/convai/conversation",
            prompt_knowledge_base=["kb entry"],
            extra_setup_config={"some_future_field": {"nested": 1}, "another": "value"},
        )
    )

    message = json.loads(conversation._create_orchestrator_initiation_message())

    assert message["some_future_field"] == {"nested": 1}
    assert message["another"] == "value"
    # Typed fields still serialize as before.
    assert message["type"] == "enclave_setup_config"
    assert message["prompt_knowledge_base"] == ["kb entry"]


def test_on_prem_initiation_data_rejects_reserved_keys_in_extra_setup_config():
    with pytest.raises(ValueError, match="prompt_knowledge_base"):
        OrchestratorConfig(
            url="ws://localhost:8000/sagemaker/convai/conversation",
            extra_setup_config={"prompt_knowledge_base": ["sneaky"]},
        )


def test_on_prem_initiation_data_copies_extra_setup_config():
    extra = {"some_future_field": 1}
    config = OrchestratorConfig(
        url="ws://localhost:8000/sagemaker/convai/conversation",
        extra_setup_config=extra,
    )
    extra["mutated_after_construction"] = True

    assert config.extra_setup_config == {"some_future_field": 1}
