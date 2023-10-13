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

We support two main models: the newest `eleven_multilingual_v2`, a single foundational model supporting 29 languages including English, Chinese, Spanish, Hindi, Portuguese, French, German, Japanese, Arabic, Korean, Indonesian, Italian, Dutch, Turkish, Polish, Swedish, Filipino, Malay, Russian, Romanian, Ukrainian, Greek, Czech, Danish, Finnish, Bulgarian, Croatian, Slovak, and Tamil; and `eleven_monolingual_v1`, a low-latency model specifically trained for English speech.

```py
from elevenlabs import generate, play

audio = generate(
  text="Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!",
  voice="Bella",
  model="eleven_multilingual_v2"
)

play(audio)
```

<details> <summary> Play </summary>

<i> Don't forget to unmute the player! </i>

[audio (3).webm](https://github.com/elevenlabs/elevenlabs-python/assets/12028621/778fd3ed-0a3a-4d66-8f73-faee099dfdd6)


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
            settings=None,
        ),
        Voice(
            voice_id='AZnzlk1XvdvUeBnXmlld',
            name='Domi',
            category='premade',
            settings=None,
        ),
        ...
    ]
)
```

</details>

Build a voice object with custom settings to personalize the voice style, or call `voice.fetch_settings()` to get the default settings for the voice.

```py
from elevenlabs import Voice, VoiceSettings, generate

audio = generate(
    text="Hello! My name is Bella.",
    voice=Voice(
        voice_id='EXAVITQu4vr4xnSDxMaL',
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
    )
)

play(audio)
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

### Input streaming
Stream text chunks into audio as it's being generated, with <1s latency. Note: if chunks don't end with space or punctuation (" ", ".", "?", "!"), the stream will wait for more text.
```py
from elevenlabs import generate, stream

def text_stream():
    yield "Hi there, I'm Eleven "
    yield "I'm a text to speech API "

audio_stream = generate(
    text=text_stream(),
    voice="Nicole",
    model="eleven_monolingual_v1",
    stream=True
)

stream(audio_stream)
```

## 🔑 API Key

The basic API has a limited number of characters. To increase this limit, you can get a free API key from [Elevenlabs](https://elevenlabs.io/) ([step-by-step guide](https://docs.elevenlabs.io/authentication/01-xi-api-key)) and set is as environment variable `ELEVEN_API_KEY`. Alternatively, you can provide the `api_key` string argument to the `generate` function, or set it globally in code with:

```py
from elevenlabs import set_api_key
set_api_key("<YOUR_API_KEY>")
```

## 📖 API & Docs

Learn more about the [Python API](API.md), or check out the [HTTP API documentation](https://docs.elevenlabs.io/quickstart).
