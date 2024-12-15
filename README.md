# ElevenLabs Python Library

![LOGO](https://github.com/elevenlabs/elevenlabs-python/assets/12028621/21267d89-5e82-4e7e-9c81-caf30b237683)

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://buildwithfern.com/?utm_source=fern-elevenlabs/elevenlabs-python/readme)
[![Discord](https://badgen.net/badge/black/ElevenLabs/icon?icon=discord&label)](https://discord.gg/elevenlabs)
[![Twitter](https://badgen.net/badge/black/elevenlabsio/icon?icon=twitter&label)](https://twitter.com/elevenlabsio)
[![PyPI - Python Version](https://img.shields.io/pypi/v/elevenlabs?style=flat&colorA=black&colorB=black)](https://pypi.org/project/elevenlabs/)
[![Downloads](https://static.pepy.tech/personalized-badge/elevenlabs?period=total&units=international_system&left_color=black&right_color=black&left_text=Downloads)](https://pepy.tech/project/elevenlabs)

The official Python API for [ElevenLabs](https://elevenlabs.io/) [text-to-speech software.](https://elevenlabs.io/text-to-speech) Eleven brings the most compelling, rich and lifelike voices to creators and developers in just a few lines of code.

## 📖 API & Docs

Check out the [HTTP API documentation](https://elevenlabs.io/docs/api-reference).

## ⚙️ Install

```bash
pip install elevenlabs
```

## 🗣️ Usage

[![Open in Spaces](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue.svg)](https://huggingface.co/spaces/elevenlabs/tts)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/flavioschneider/49468d728a816c6538fd2f56b3b50b96/elevenlabs-python.ipynb)

### Main Models

1. **Eleven Multilingual v2** (`eleven_multilingual_v2`)

   - Excels in stability, language diversity, and accent accuracy
   - Supports 29 languages
   - Recommended for most use cases

2. **Eleven Turbo v2.5** (`eleven_turbo_v2_5`)
   - High quality, lowest latency
   - Ideal for developer use cases where speed is crucial
   - Supports 32 languages

For more detailed information about these models and others, visit the [ElevenLabs Models documentation](https://elevenlabs.io/docs/speech-synthesis/models).

```py
from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="YOUR_API_KEY", # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

audio = client.generate(
  text="Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!",
  voice="Brian",
  model="eleven_multilingual_v2"
)
play(audio)
```

<details> <summary> Play </summary>

🎧 **Try it out!** Want to hear our voices in action? Visit the [ElevenLabs Voice Lab](https://elevenlabs.io/voice-lab) to experiment with different voices, languages, and settings.

</details>

## 🗣️ Voices

List all your available voices with `voices()`.

```py
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="YOUR_API_KEY", # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

response = client.voices.get_all()
audio = client.generate(text="Hello there!", voice=response.voices[0])
print(response.voices)
```

For information about the structure of the voices output, please refer to the [official ElevenLabs API documentation for Get Voices](https://elevenlabs.io/docs/api-reference/get-voices).

Build a voice object with custom settings to personalize the voice style, or call
`client.voices.get_settings("your-voice-id")` to get the default settings for the voice.

```py
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="YOUR_API_KEY", # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

audio = client.generate(
    text="Hello! My name is Brian.",
    voice=Voice(
        voice_id='nPczCjzI2devNBz1zQrb',
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
    )
)

play(audio)
```

</details>

## Clone Voice

Clone your voice in an instant. Note that voice cloning requires an API key, see below.

```py
from elevenlabs.client import ElevenLabs
from elevenlabs import play

client = ElevenLabs(
  api_key="YOUR_API_KEY", # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

voice = client.clone(
    name="Alex",
    description="An old American male voice with a slight hoarseness in his throat. Perfect for news", # Optional
    files=["./sample_0.mp3", "./sample_1.mp3", "./sample_2.mp3"],
)

audio = client.generate(text="Hi! I'm a cloned voice!", voice=voice)

play(audio)
```

## 🚿 Streaming

Stream audio in real-time, as it's being generated.

```py
from elevenlabs.client import ElevenLabs
from elevenlabs import stream

client = ElevenLabs(
  api_key="YOUR_API_KEY", # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

audio_stream = client.generate(
  text="This is a... streaming voice!!",
  stream=True
)

stream(audio_stream)
```

Note that `generate` is a helper function. If you'd like to access
the raw method, simply use `client.text_to_speech.convert_as_stream`.

### Input streaming

Stream text chunks into audio as it's being generated, with <1s latency. Note: if chunks don't end with space or punctuation (" ", ".", "?", "!"), the stream will wait for more text.

```py
from elevenlabs.client import ElevenLabs
from elevenlabs import stream

client = ElevenLabs(
  api_key="YOUR_API_KEY", # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

def text_stream():
    yield "Hi there, I'm Eleven "
    yield "I'm a text to speech API "

audio_stream = client.generate(
    text=text_stream(),
    voice="Brian",
    model="eleven_multilingual_v2",
    stream=True
)

stream(audio_stream)
```

Note that `generate` is a helper function. If you'd like to access
the raw method, simply use `client.text_to_speech.convert_realtime`.

## Async Client

Use `AsyncElevenLabs` if you want to make API calls asynchronously.

```python
import asyncio

from elevenlabs.client import AsyncElevenLabs

eleven = AsyncElevenLabs(
  api_key="MY_API_KEY" # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

async def print_models() -> None:
    models = await eleven.models.get_all()
    print(models)

asyncio.run(print_models())
```

## Languages Supported

We support 32 languages and 100+ accents. Explore [all languages](https://elevenlabs.io/languages).

<img src="https://github.com/elevenlabs/elevenlabs-js/blob/main/assets/languages.png" width="900">

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
