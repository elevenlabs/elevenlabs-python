<img src="LOGO.png"></img>

The official Python library to access [Elevenlabs](https://elevenlabs.io/) text-to-speech software. Eleven brings the most compelling, rich and lifelike voices to creators and publishers seeking the ultimate tools for storytelling.


## ⚙️ Install

```bash
pip install elevenlabs
```

## 🗣️ Usage

```py
from elevenlabs import generate, play

text = """ Hi! I'm the world's most advanced text-to-speech system, made by elevenlabs. """
audio = generate(text)
play(audio)
```


<details> <summary> Play </summary>

<i> Don't forget to unmute the player! </i>

[voice.webm](https://user-images.githubusercontent.com/12028621/232730309-e47bc907-78ec-4acf-a73a-0d77ba25fd6b.webm)

</details>

### 👥 Voices

```py
from elevenlabs import generate, play

voice = "Adam"
text = f""" Hi! My name is {voice}, nice to meet you! """
audio = generate(text, voice=voice)
play(audio)
```

<details> <summary> Play </summary>

<i> Don't forget to unmute the player! </i>

<b>Adam</b>

[Adam.webm](https://user-images.githubusercontent.com/12028621/232730475-4babdd1b-6078-47d0-811a-68678d009918.webm)

<b>Antoni</b>

[Antoni.webm](https://user-images.githubusercontent.com/12028621/232730870-164e2423-26d2-4423-89ff-36e78483e4e2.webm)

<b>Arnold</b>

[Arnold.webm](https://user-images.githubusercontent.com/12028621/232731257-f7cccbf0-e4d3-49de-9bc8-280e54a29e88.webm)

<b>Bella</b>

[Bella.webm](https://user-images.githubusercontent.com/12028621/232731276-00a8e665-5f7c-4fe7-adcf-47ac0d634874.webm)

<b>Domi</b>

[Domi.webm](https://user-images.githubusercontent.com/12028621/232731299-ca33fdab-fa79-4343-afad-ece0d4363ffe.webm)

<b>Elli</b>

[Elli.webm](https://user-images.githubusercontent.com/12028621/232731318-a1debbd9-ce06-4e71-8199-119cddb2f19c.webm)

<b>Josh</b>

[Josh.webm](https://user-images.githubusercontent.com/12028621/232731374-f81bcc7c-d30c-4958-8086-2271274d6f12.webm)

<b>Rachel</b>

[Rachel.webm](https://user-images.githubusercontent.com/12028621/232731393-9ccdcf54-a957-44ac-b882-67a95e95d7d0.webm)

<b>Sam</b>

[Sam.webm](https://user-images.githubusercontent.com/12028621/232731428-18bca274-6b84-42e4-b4d8-819b0bd0a19a.webm)

</details>

### 🚿 Streaming

```py
from elevenlabs import generate, stream

text = """ This is a... streaming voice!! """
audio_stream = generate(text, stream=True)
stream(audio_stream)
```

### 🔑 API Key

The basic API has a limited number of characters. To increase this limit, you can get a free API key from [Elevenlabs](https://elevenlabs.io/) and set is as environment variable `ELEVEN_API_KEY`. Alternatively pass the `api_key` string argument to the `generate` function, or set it programmatically as:
```py
from elevenlabs import set_api_key
set_api_key("<YOUR_API_KEY>")
```

### `generate` API

```py
generate(
    text: str,
    api_key: Optional[str] = None,          # Defautls to env variable ELEVEN_API_KEY, or None if not set but quota will be limited
    voice: Union[str, Voice] = "Bella",     # Either a voice name, voice_id, or Voice object (use voice object to control stability and similarity_boost)
    stream: bool = False,                   # If True, returns a generator streaming bytes
    stream_chunk_size: int = 2048,          # Size of each chunk when stream=True
) -> Union[bytes, Iterator[bytes]]
```

## API

### User
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


### Voices

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

### History

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
