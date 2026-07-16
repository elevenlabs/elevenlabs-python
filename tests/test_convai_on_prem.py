import json
from unittest.mock import MagicMock

import pytest

from elevenlabs.conversational_ai.conversation import (
    AudioInterface,
    Conversation,
    OnPremInitiationData,
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


def _make_conversation(on_prem_config: OnPremInitiationData) -> Conversation:
    mock_client = MagicMock()
    mock_client._client_wrapper.get_base_url.return_value = "https://api.elevenlabs.io"
    return Conversation(
        client=mock_client,
        agent_id="",
        requires_auth=False,
        audio_interface=MockAudioInterface(),
        on_prem_config=on_prem_config,
    )


def test_post_call_webhook_config_to_dict():
    assert PostCallWebhookConfig(url="https://example.com/hook").to_dict() == {"url": "https://example.com/hook"}
    assert PostCallWebhookConfig(url="https://example.com/hook", hmac_secret="0123456789abcdef").to_dict() == {
        "url": "https://example.com/hook",
        "hmac_secret": "0123456789abcdef",
    }


def test_on_prem_initiation_message_includes_typed_webhooks():
    conversation = _make_conversation(
        OnPremInitiationData(
            on_prem_conversation_url="ws://localhost:8000/sagemaker/convai/conversation",
            post_call_transcription_webhook=PostCallWebhookConfig(
                url="https://example.com/transcript", hmac_secret="0123456789abcdef"
            ),
            post_call_audio_webhook=PostCallWebhookConfig(url="https://example.com/audio"),
        )
    )

    message = json.loads(conversation._create_on_prem_initiation_message())

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
        OnPremInitiationData(
            on_prem_conversation_url="ws://localhost:8000/sagemaker/convai/conversation",
            post_call_transcription_webhook_url="https://example.com/transcript",
        )
    )

    message = json.loads(conversation._create_on_prem_initiation_message())

    assert "post_call_transcription_webhook" not in message
    assert "post_call_audio_webhook" not in message
    assert message["post_call_transcription_webhook_url"] == "https://example.com/transcript"


@pytest.mark.parametrize(
    ("legacy_kwarg", "typed_kwarg"),
    [
        ("post_call_transcription_webhook_url", "post_call_transcription_webhook"),
        ("post_call_audio_webhook_url", "post_call_audio_webhook"),
    ],
)
def test_on_prem_initiation_data_rejects_legacy_and_typed_for_same_webhook(legacy_kwarg: str, typed_kwarg: str):
    with pytest.raises(ValueError, match="not both"):
        OnPremInitiationData(
            on_prem_conversation_url="ws://localhost:8000/sagemaker/convai/conversation",
            **{
                legacy_kwarg: "https://example.com/hook",
                typed_kwarg: PostCallWebhookConfig(url="https://example.com/hook"),
            },
        )
