import json
import time
import hmac
import hashlib
from unittest import mock

from elevenlabs.client import AsyncElevenLabs, ElevenLabs
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


def _signed_header(body: str, timestamp: str, secret: str = "test_secret") -> str:
    digest = hmac.new(secret.encode("utf-8"), f"{timestamp}.{body}".encode("utf-8"), hashlib.sha256).hexdigest()
    return f"t={timestamp},v0={digest}"


@pytest.fixture(params=["sync", "async"])
def webhooks(request):
    """Both clients carry their own copy of construct_event, so every case below runs against each."""
    client = ElevenLabs() if request.param == "sync" else AsyncElevenLabs()
    return client.webhooks


@pytest.mark.parametrize("timestamp", ["abc", "1e12", "-1", " 1600000000", "1600000000.5"])
def test_construct_event_rejects_non_integer_timestamp(webhooks, timestamp):
    """A correctly signed event whose timestamp is not whole Unix seconds is rejected with BadRequestError.

    int("abc") used to raise ValueError instead, and int(" 1600000000") was accepted.
    """
    body = json.dumps({"event_type": "speech.completed", "id": "123456"})

    with mock.patch("time.time", return_value=1600000000):
        with pytest.raises(BadRequestError) as excinfo:
            webhooks.construct_event(body, _signed_header(body, timestamp), "test_secret")

    assert "Timestamp outside the tolerance zone" in str(excinfo.value)


@pytest.mark.parametrize("signature", ["v0=ünïcode", "v0=" + "0" * 64, "v0="])
def test_construct_event_rejects_wrong_signature_with_bad_request(webhooks, signature):
    """A wrong signature, including one with non-ASCII characters, is a BadRequestError and never a TypeError."""
    body = json.dumps({"event_type": "speech.completed", "id": "123456"})
    timestamp = str(int(time.time()))

    with pytest.raises(BadRequestError) as excinfo:
        webhooks.construct_event(body, f"t={timestamp},{signature}", "test_secret")

    assert "Signature hash does not match" in str(excinfo.value)


def test_construct_event_compares_signature_in_constant_time(webhooks):
    """The signature check goes through hmac.compare_digest rather than ==, which stops at the first difference."""
    body = json.dumps({"event_type": "speech.completed", "id": "123456"})
    timestamp = str(int(time.time()))

    with mock.patch("elevenlabs.webhooks_custom.hmac.compare_digest", wraps=hmac.compare_digest) as compare:
        event = webhooks.construct_event(body, _signed_header(body, timestamp), "test_secret")

    assert event == json.loads(body)
    compare.assert_called_once()
