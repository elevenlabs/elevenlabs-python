import pytest

from elevenlabs import generate, voices, Voice, VoiceSettings, play, stream


# @pytest.mark.skip(reason="skip in ci")
def test_voices() -> None:
    print("Voices are...", voices())


@pytest.mark.skip(reason="skip in ci")
def test_generate() -> None:
    audio = generate(
        text="Hello! My name is Bella.",
        voice=Voice(
            voice_id='EXAVITQu4vr4xnSDxMaL',
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        )
    )
    play(audio)  # type: ignore

@pytest.mark.skip(reason="skip in ci")
def test_generate_stream() -> None:
    def text_stream():
        yield "Hi there, I'm Eleven "
        yield "I'm a text to speech API "

    audio_stream = generate(
        text=text_stream(),
        voice="Nicole",
        model="eleven_monolingual_v1",
        stream=True
    )

    stream(audio_stream)  # type: ignore