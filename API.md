# Elevenlabs API

## Function Signatures

### `generate`

```py
from elevenlabs import generate

generate(
    text: str,
    api_key: Optional[str] = None,                      # Defautls to env variable ELEVEN_API_KEY, or None if not set but quota will be limited
    voice: Union[str, Voice] = "Bella",                 # Either a voice name, voice_id, or Voice object (use voice object to control stability and similarity_boost)
    model: Union[str, Model] = "eleven_monolingual_v1", # Either a model name or Model object
    stream: bool = False,                               # If True, returns a generator streaming bytes
    stream_chunk_size: int = 2048,                      # Size of each chunk when stream=True
    latency: int = 1                                    # [1-4] the higher the more optimized for streaming latency (only works with stream=True)
) -> Union[bytes, Iterator[bytes]]
```

### `play`

Plays audio bytes returned by generate. Note playing requires [ffmpeg](https://ffmpeg.org/download.html) to be installed (`brew install ffmpeg` on mac), alternatively you can set `use_ffmpeg=False`, this requires sounddevice and soundfile: `pip install sounddevice soundfile`.

```py
from elevenlabs import play

play(
    audio: bytes,               # Audio bytes (returned by generate)
    notebook: bool = False,     # If True, plays audio in notebook (using IPython.display.Audio) else uses ffmpeg
    use_ffmpeg: bool = True,    # If False, uses sounddevice and soundfile to play audio
) -> None
```

### `save`

```py
from elevenlabs import save

save(
    audio: bytes,               # Audio bytes (returned by generate)
    filename: str               # Filename to save audio to (e.g. "audio.wav")
) -> None
```

### `stream`

Streams audio bytes returned by generate with `stream=True`. Note that this function requires [mpv](https://mpv.io/installation/) to be installed (`brew install mpv` on mac).

```py
from elevenlabs import stream

stream(
    audio_stream: Iterator[bytes]   # Audio stream (returned by generate with stream=True)
) -> bytes                          # Returns the full audio bytes
```

### `voices`

```py
from elevenlabs import voices

voices(                             # Lists all voices for the authenticated user, or the default voices if no API key is set
    api_key: Optional[str] = None
) -> List[Voice]
```

### `clone`

This function requires an API key.

```py
from elevenlabs import clone

clone(
    name: str,                          # Name of the new voice
    description: Optional[str],         # Description of the new voice
    files: List[str],                   # List of audio files to use for cloning
    labels: Optional[dict[str, str]]    # Optional labels to add to the new voice
) -> Voice                              # Returns the new voice object
```

### `set_api_key`

```py
from elevenlabs import set_api_key

set_api_key(api_key: str) -> None
```

### `get_api_key`

```py
from elevenlabs import get_api_key

get_api_key() -> Optional[str]
```



## API Objects

### `User`
The `User` API is used to request the user's subscription information, such as the number of character remaining in the quota. Note that you must set an API key to use this object.

```py
from elevenlabs.api import User
user = User.from_api()
print(user)
```
<details> <summary> Show output </summary>

```py
User(
    subscription=Subscription(
        character_count=5185,
        character_limit=10000,
        available_models=[Models(model_id='prod', display_name='Prod')],
        status='free'
    )
)
```

</details>

### `Models`

The `Models` API is used to get a list of all available models for the authenticated user. The `Model` contains all the info for a model, and can be passed to the `generate` function as the `model` argument to select the model. Note that you must set an API key to use this object.

```py
from elevenlabs.api import Models
models = Models.from_api()
print(models[0])
print(models)
```

<details> <summary> Show output </summary>

```py
Model(
    model_id='eleven_monolingual_v1',
    name='Eleven Monolingual v1',
    token_cost_factor=1.0,
    description='Use our standard English language model to generate speech in a variety of voices, styles and moods.'
)
```

```py
Models(
    models=[
        Model(
            model_id='eleven_monolingual_v1',
            name='Eleven Monolingual v1',
            token_cost_factor=1.0,
            description='Use our standard English language model to generate speech in a variety of voices, styles and moods.'
        ),
        Model(
            model_id='eleven_multilingual_v1',
            name='Eleven Multilingual v1',
            token_cost_factor=1.0,
            description='Generate lifelike speech in multiple languages and create content that resonates with a broader audience. '
        )
    ]
)
```

</details>

### `Voices`

The `Voices` API is used to get a list of all available voices for the authenticated user. The `Voice` contains all the info for a voice, such as the voice's stability and similarity_boost, and can be passed to the `generate` function as the `voice` argument to select the voice. The voice settings can be changed to control the voice behaviour.

```py
from elevenlabs.api import Voices
voices = Voices.from_api()
print(voices[0])
print(voices)
```

<details> <summary> Show output </summary>

```py
Voice(
    voice_id='21m00Tcm4TlvDq8ikWAM',
    name='Rachel',
    category='premade',
    settings=VoiceSettings(stability=0.75, similarity_boost=0.75)
)
```

```py
Voices(
    voices=[
        Voice(
            voice_id='21m00Tcm4TlvDq8ikWAM',
            name='Rachel',
            category='premade',
            settings=VoiceSettings(stability=0.75, similarity_boost=0.75)
        ),
        Voice(
            voice_id='AZnzlk1XvdvUeBnXmlld',
            name='Domi',
            category='premade',
            settings=VoiceSettings(stability=0.1, similarity_boost=0.75)
        ),
        Voice(
            voice_id='EXAVITQu4vr4xnSDxMaL',
            name='Bella',
            category='premade',
            settings=VoiceSettings(stability=0.245, similarity_boost=0.75)
        ),
        Voice(
            voice_id='ErXwobaYiN019PkySvjV',
            name='Antoni',
            category='premade',
            settings=VoiceSettings(stability=0.195, similarity_boost=0.75)
        ),
        Voice(
            voice_id='MF3mGyEYCl7XYWbV9V6O',
            name='Elli',
            category='premade',
            settings=VoiceSettings(stability=0.755, similarity_boost=0.75)
        ),
        Voice(
            voice_id='TxGEqnHWrfWFTfGW9XjX',
            name='Josh',
            category='premade',
            settings=VoiceSettings(stability=0.15, similarity_boost=0.51)
        ),
        Voice(
            voice_id='VR6AewLTigWG4xSOukaG',
            name='Arnold',
            category='premade',
            settings=VoiceSettings(stability=0.15, similarity_boost=0.75)
        ),
        Voice(
            voice_id='pNInz6obpgDQGcFmaJgB',
            name='Adam',
            category='premade',
            settings=VoiceSettings(stability=0.2, similarity_boost=0.75)
        ),
        Voice(
            voice_id='yoZ06aMxZJJ28mfd3POQ',
            name='Sam',
            category='premade',
            settings=VoiceSettings(stability=0.25, similarity_boost=0.75)
        )
    ]
)
```

</details>

An example of changing the `Voice` object to control the voice behaviour:

```py
my_voice = voices[0]
my_voice.settings.stability = 0.1
my_voice.settings.similarity_boost = 0.75

text = f""" Hi! My name is {my_voice.name}, nice to meet you! """
audio = generate(text, voice=my_voice)
```

### `VoiceDesign`

The `VoiceDesign` API is used to get design a voice with a custom gender, accent and age group. Note that you must set an API key to use this object.
```py
from elevenlabs import Voice, VoiceDesign, Gender, Age, Accent, play

# Build a voice deisgn object
design = VoiceDesign(
    name='Lexa',
    text="Hello, my name is Lexa. I'm your personal assistant, I can help you with your daily tasks and I can also read you the news.",
    description="A young british female voice, resembling a secretary. Perfect for office assistant roles.",
    labels={'accent': 'british', 'gender': 'female', 'age': 'young'},
    gender=Gender.female,
    age=Age.young,
    accent=Accent.british,
    accent_strength=1.0,
)

# Generate audio from the design, and play it to test if it sounds good (optional)
audio = design.generate()
play(audio)

# Convert design to usable voice
voice = Voice.from_design(design)
```

### `History`

The `History` API is used to get the list of generations of the authenticated user.

```py
from elevenlabs.api import History
history = History.from_api()
print(history)
```

<details> <summary> Show output </summary>

```py
History(
    history=[
        HistoryItem(
            history_item_id='coDAIxWBxUhQuIaMIicv',
            request_id='d680d4160837cb610a64e1a28d72e37b',
            voice_id='EXAVITQu4vr4xnSDxMaL',
            text=' This is a... streaming voice!! ',
            date=datetime.datetime(2023, 4, 18, 14, 24, 5),
            date_unix=1681827845,
            character_count_change_from=5153,
            character_count_change_to=5185,
            character_count_change=32,
            content_type='audio/mpeg',
            settings=VoiceSettings(stability=0.245, similarity_boost=0.75),
            feedback=None
        ),
        HistoryItem(
            history_item_id='lXryIJPkG4KmR4lZFAPF',
            request_id='31e1ead811826efb38e4c867d383da77',
            voice_id='EXAVITQu4vr4xnSDxMaL',
            text=" Hi! I'm the world's most advanced text-to-speech system, made by elevenlabs. ",
            date=datetime.datetime(2023, 4, 18, 14, 21, 32),
            date_unix=1681827692,
            character_count_change_from=5075,
            character_count_change_to=5153,
            character_count_change=78,
            content_type='audio/mpeg',
            settings=VoiceSettings(stability=0.245, similarity_boost=0.75),
            feedback=None
        ),
        ...
    ]
)
```

</details>

An example of playing the `HistoryItem` audio at index 3:
```py
from elevenlabs import play
play(history[3].audio)
```
