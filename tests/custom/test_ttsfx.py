from elevenlabs import play
from elevenlabs.client import ElevenLabs

from .utils import IN_GITHUB


def test_text_to_sound_effects_convert() -> None:
    """Test basic sound-effect generation."""
    client = ElevenLabs()
    audio_generator = client.text_to_sound_effects.convert(
        text="Hypnotic throbbing sound effect. Increases in imtensity.",
        duration_seconds=2,
    )
    audio = b"".join(audio_generator)
    assert isinstance(audio, bytes), "TTS should return bytes"
    if not IN_GITHUB:
        play(audio)
