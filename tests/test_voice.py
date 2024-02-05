from elevenlabs.client import ElevenLabs
from elevenlabs.types.voice_response import VoiceResponse
from .utils import IN_GITHUB


def test_voice_from_id():
    from elevenlabs import Voice, VoiceSettings
    from elevenlabs.client import ElevenLabs

    # Test that we can get a voice from id
    voice_id = "21m00Tcm4TlvDq8ikWAM"

    client = ElevenLabs()
    voice = client.voices.get(voice_id)
    assert isinstance(voice, VoiceResponse)

    assert voice.voice_id == voice_id
    assert voice.name == "Rachel"
    assert voice.category == "premade"
    if voice.settings is not None: 
        assert isinstance(voice.settings, VoiceSettings)


def test_voice_clone():
    from elevenlabs import Voice, clone, generate, play

    from .utils import as_local_files

    client = ElevenLabs()

    voice_file_urls = [
        "https://user-images.githubusercontent.com/12028621/235474694-584f7103-dab2-4c39-bb9a-8e5f00be85da.webm",
    ]

    with as_local_files(voice_file_urls) as files:
        voice = clone(
            name="Alex",
            description=(
                "An old American male voice with a slight hoarseness in his throat."
                " Perfect for news"
            ),
            files=files,
        )

    assert isinstance(voice, Voice)
    assert voice.voice_id is not None
    assert voice.name == "Alex"
    assert voice.category == "cloned"
    assert len(voice.samples) == len(voice_file_urls)

    audio = generate(
        text="Voice clone test successful.",
        voice=voice,
    )
    assert isinstance(audio, bytes) and len(audio) > 0

    client.voices.delete(voice.voice_id)

    if not IN_GITHUB:
        play(audio)


def test_voice_design():
    from elevenlabs import Accent, Age, Gender, Voice, generate, play
    from elevenlabs.client import ElevenLabs

    client = ElevenLabs()

    audio = client.voices.design(
        name="Lexa",
        text=(
            "Hi! My name is Lexa, I'm a voice design test. I should have a middle aged"
            " female voice with a british accent. "
        ),
        voice_description="Middle aged female with british accent.",
        gender=Gender.FEMALE,
        age=Age.MIDDLE_AGED,
        accent=Accent.BRITISH,
        accent_strength=1.5,
    )

    assert isinstance(audio, bytes) and len(audio) > 0
    
    if not IN_GITHUB:
        play(audio)



def test_voices():
    from elevenlabs import voices, Voice

    # Test that we can get voices from api
    eleven_voices = voices()

    assert len(eleven_voices) > 0
    assert isinstance(eleven_voices[0], Voice)

    for voice in eleven_voices:
        assert isinstance(voice, Voice)
        