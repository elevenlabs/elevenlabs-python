from elevenlabs import Voice, \
    VoiceSettings, play
from .utils import IN_GITHUB, as_local_files, client


def test_voice_from_id():

    # Test that we can get a voice from id
    voice_id = "21m00Tcm4TlvDq8ikWAM"

    voice = client.voices.get(voice_id)
    assert isinstance(voice, Voice)

    assert voice.voice_id == voice_id
    assert voice.name == "Rachel"
    assert voice.category == "premade"
    if voice.settings is not None: 
        assert isinstance(voice.settings, VoiceSettings)


def test_voice_clone():
    voice_file_urls = [
        "https://user-images.githubusercontent.com/12028621/235474694-584f7103-dab2-4c39-bb9a-8e5f00be85da.webm",
    ]

    for file in as_local_files(voice_file_urls): 
        voice = client.clone(
            name="Alex",
            description=(
                "An old American male voice with a slight hoarseness in his throat."
                " Perfect for news"
            ),
            files=[file],
        )

    assert isinstance(voice, Voice)  # type: ignore
    assert voice.voice_id is not None
    assert voice.name == "Alex"
    assert voice.category == "cloned"
    assert len(voice.samples or []) == len(voice_file_urls)

    audio = client.generate(
        text="Voice clone test successful.",
        voice=voice,
    )

    if not IN_GITHUB:
        play(audio)
    
    client.voices.delete(voice.voice_id)


def test_voice_design():
    audio = client.voice_generation.generate(
        text=(
            "Hi! My name is Lexa, I'm a voice design test. I should have a middle aged"
            " female voice with a british accent. "
        ),
        gender="female",
        age="middle_aged",
        accent="british",
        accent_strength=1.5,
    )

    if not IN_GITHUB:
        play(audio)


def test_voices():
    # Test that we can get voices from api
    response = client.voices.get_all()

    assert len(response.voices) > 0

    for voice in response.voices:
        assert isinstance(voice, Voice)
