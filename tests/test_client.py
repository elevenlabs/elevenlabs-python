from elevenlabs import play, \
    Voice, VoiceSettings, stream
from .utils import IN_GITHUB, client


def test_voices() -> None:
    print("Voices are...", client.voices.get_all())


def test_generate() -> None:
    audio = client.generate(
        text="Hello! My name is Bella.",
        voice=Voice(
            voice_id='EXAVITQu4vr4xnSDxMaL',
            settings=VoiceSettings(
                stability=0.71,
                similarity_boost=0.5,
                style=0.0,
                use_speaker_boost=True
            )
        ))
    if not IN_GITHUB:
        play(audio)  # type: ignore


def test_generate_stream() -> None:
    def text_stream():
        yield "Hi there, I'm Eleven "
        yield "I'm a text to speech API "

    audio_stream = client.generate(
        text=text_stream(),
        voice="Nicole",
        model="eleven_monolingual_v1",
        stream=True
    )

    if not IN_GITHUB:
        stream(audio_stream)  # type: ignore
