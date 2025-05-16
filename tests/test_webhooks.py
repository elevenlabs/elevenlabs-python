import json
import time
import hmac
import hashlib
from unittest import mock

from elevenlabs.client import ElevenLabs
from elevenlabs.errors import BadRequestError

import pytest


def test_construct_event_valid_signature():
    """Test webhook event construction with valid signature."""
    # Setup
    client = ElevenLabs()
    webhook_secret = "test_secret"
    payload = {"event_type": "speech.completed", "id": "123456"}

    # Create a valid signature
    body = json.dumps(payload)
    timestamp = str(int(time.time()))
    message = f"{timestamp}.{body}"
    signature = "v0=" + hmac.new(
        webhook_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    sig_header = f"t={timestamp},{signature}"

    # Verify event construction
    event = client.webhooks.construct_event(body, sig_header, webhook_secret)
    assert event == payload, "Event should match the original payload"


def test_construct_event_missing_signature():
    """Test webhook event construction with missing signature header."""
    client = ElevenLabs()
    webhook_secret = "test_secret"
    payload = {"event_type": "speech.completed", "id": "123456"}

    with pytest.raises(BadRequestError) as excinfo:
        client.webhooks.construct_event(payload, "", webhook_secret)

    assert "Missing signature header" in str(excinfo.value)


def test_construct_event_invalid_signature_format():
    """Test webhook event construction with invalid signature format."""
    client = ElevenLabs()
    webhook_secret = "test_secret"
    payload = {"event_type": "speech.completed", "id": "123456"}
    body = json.dumps(payload)
    sig_header = "invalid_format"

    with pytest.raises(BadRequestError) as excinfo:
        client.webhooks.construct_event(body, sig_header, webhook_secret)

    assert "No signature hash found with expected scheme v0" in str(excinfo.value)


def test_construct_event_expired_timestamp():
    """Test webhook event construction with expired timestamp."""
    client = ElevenLabs()
    webhook_secret = "test_secret"
    payload = {"event_type": "speech.completed", "id": "123456"}

    # Create an expired timestamp (31 minutes old)
    expired_time = int(time.time()) - 31 * 60
    timestamp = str(expired_time)

    body = json.dumps(payload)
    message = f"{timestamp}.{body}"
    signature = "v0=" + hmac.new(
        webhook_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    sig_header = f"t={timestamp},{signature}"

    with pytest.raises(BadRequestError) as excinfo:
        client.webhooks.construct_event(body, sig_header, webhook_secret)

    assert "Timestamp outside the tolerance zone" in str(excinfo.value)


def test_construct_event_invalid_signature():
    """Test webhook event construction with invalid signature."""
    client = ElevenLabs()
    webhook_secret = "test_secret"
    payload = {"event_type": "speech.completed", "id": "123456"}
    body = json.dumps(payload)

    timestamp = str(int(time.time()))
    sig_header = f"t={timestamp},v0=invalid_signature"

    with pytest.raises(BadRequestError) as excinfo:
        client.webhooks.construct_event(body, sig_header, webhook_secret)

    assert "Signature hash does not match" in str(excinfo.value)


def test_construct_event_missing_secret():
    """Test webhook event construction with missing secret."""
    client = ElevenLabs()
    payload = {"event_type": "speech.completed", "id": "123456"}
    body = json.dumps(payload)

    timestamp = str(int(time.time()))
    sig_header = f"t={timestamp},v0=some_signature"

    with pytest.raises(BadRequestError) as excinfo:
        client.webhooks.construct_event(body, sig_header, "")

    assert "Webhook secret not configured" in str(excinfo.value)


@mock.patch('time.time')
def test_construct_event_mocked_time(mock_time):
    """Test webhook event construction with mocked time."""
    mock_time.return_value = 1600000000

    client = ElevenLabs()
    webhook_secret = "test_secret"
    payload = {"event_type": "speech.completed", "id": "123456"}

    # Create a valid signature with fixed timestamp
    body = json.dumps(payload)
    timestamp = "1600000000"
    message = f"{timestamp}.{body}"
    signature = "v0=" + hmac.new(
        webhook_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    sig_header = f"t={timestamp},{signature}"

    # Verify event construction
    event = client.webhooks.construct_event(body, sig_header, webhook_secret)
    assert event == payload, "Event should match the original payload"
