![LOGO](https://github.com/elevenlabs/elevenlabs-python/assets/12028621/21267d89-5e82-4e7e-9c81-caf30b237683)

[![Discord](https://badgen.net/badge/black/ElevenLabs/icon?icon=discord&label)](https://discord.gg/elevenlabs)
[![Twitter](https://badgen.net/badge/black/elevenlabsio/icon?icon=twitter&label)](https://twitter.com/elevenlabsio)
[![PyPI - Python Version](https://img.shields.io/pypi/v/elevenlabs?style=flat&colorA=black&colorB=black)](https://pypi.org/project/elevenlabs/)
[![Downloads](https://static.pepy.tech/personalized-badge/elevenlabs?period=total&units=international_system&left_color=black&right_color=black&left_text=Downloads)](https://pepy.tech/project/elevenlabs)

The official Python API for [ElevenLabs](https://elevenlabs.io/) text-to-speech software. Eleven brings the most compelling, rich and lifelike voices to creators and developers in just a few lines of code.


## ⚙️ Install

```bash
pip install elevenlabs
```

## 🗣️ Usage
[![Open in Spaces](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue.svg)](https://huggingface.co/spaces/elevenlabs/tts)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/flavioschneider/49468d728a816c6538fd2f56b3b50b96/elevenlabs-python.ipynb)


```py
from elevenlabs import generate, play

audio = generate(
  text="Hi! My name is Bella, nice to meet you!",
  voice="Bella",
  model="eleven_monolingual_v1"
)

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

## 🌎 Multilingual

The `eleven_multilingual_v1` model supports multiple languages, including English, German, Polish, Spanish, Italian, French, Portuguese, and Hindi.
```py
from elevenlabs import generate, play

audio = generate(
    text="¡Hola! Mi nombre es Arnold, encantado de conocerte!",
    voice="Arnold",
    model='eleven_multilingual_v1'
)

play(audio)
```

<details> <summary> Play </summary>

<i> Don't forget to unmute the player! </i>

[hola.webm](https://user-images.githubusercontent.com/12028621/235474694-584f7103-dab2-4c39-bb9a-8e5f00be85da.webm)

</details>


## 🗣️ Voices

List all your available voices with `voices()`.
```py
from elevenlabs import voices, generate

voices = voices()

audio = generate(text="Hello there!", voice=voices[0])

print(voices)
```

<details> <summary> Show output </summary>

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
        ),
        Voice(
            voice_id='3KehPe3gxEYqOFSGDzGM',
            name='test',
            category='cloned',
            settings=VoiceSettings(stability=0.75, similarity_boost=0.75)
        ),
        Voice(
            voice_id='duorpit9NOULscUJ2OAp',
            name='test',
            category='cloned',
            settings=VoiceSettings(stability=0.75, similarity_boost=0.75)
        ),
        Voice(
            voice_id='h2rNV1Iql95D2QSSuvLY',
            name='test',
            category='cloned',
            settings=VoiceSettings(stability=0.75, similarity_boost=0.75)
        )
    ]
)
```

</details>


### Clone Voice

Clone your voice in an instant. Note that voice cloning requires an API key, see below.

```py
from elevenlabs import clone, generate, play

voice = clone(
    name="Alex",
    description="An old American male voice with a slight hoarseness in his throat. Perfect for news", # Optional
    files=["./sample_0.mp3", "./sample_1.mp3", "./sample_2.mp3"],
)

audio = generate(text="Hi! I'm a cloned voice!", voice=voice)

play(audio)
```

## 🚿 Streaming

Stream audio in real-time, as it's being generated.

```py
from elevenlabs import generate, stream

audio_stream = generate(
  text="This is a... streaming voice!!",
  stream=True
)

stream(audio_stream)
```

## 🔑 API Key

The basic API has a limited number of characters. To increase this limit, you can get a free API key from [Elevenlabs](https://elevenlabs.io/) ([step-by-step guide](https://docs.elevenlabs.io/authentication/01-xi-api-key)) and set is as environment variable `ELEVEN_API_KEY`. Alternatively you can provide the `api_key` string argument to the `generate` function, or set it globally in code with:

```py
from elevenlabs import set_api_key
set_api_key("<YOUR_API_KEY>")
```

## 📖 API & Docs

Learn more about the [Python API](API.md), or check out the [HTTP API documentation](https://docs.elevenlabs.io/quickstart).
