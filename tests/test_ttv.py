from elevenlabs.client import ElevenLabs


def test_voice_preview_generation():
    """Test generating voice previews from description."""
    client = ElevenLabs()

    # Test parameters
    description = "A warm and friendly female voice with a slight British accent, speaking clearly and professionally"
    sample_text = "This is a test message that needs to be at least one hundred characters long to meet the API requirements. Here it is."

    previews = client.text_to_voice.create_previews(voice_description=description, text=sample_text)

    assert hasattr(previews, "previews"), "Response should have 'previews' attribute"
    assert len(previews.previews) > 0, "Should receive at least one preview"
    assert hasattr(previews.previews[0], "generated_voice_id"), "Preview should contain generated_voice_id"
    assert hasattr(previews.previews[0], "audio_base_64"), "Preview should contain audio_base_64"
