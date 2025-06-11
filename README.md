# ElevenLabs Python Library

![LOGO](https://github.com/elevenlabs/elevenlabs-python/assets/12028621/21267d89-5e82-4e7e-9c81-caf30b237683)

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://buildwithfern.com/?utm_source=fern-elevenlabs/elevenlabs-python/readme)
[![Discord](https://badgen.net/badge/black/ElevenLabs/icon?icon=discord&label)](https://discord.gg/elevenlabs)
[![Twitter](https://badgen.net/badge/black/elevenlabsio/icon?icon=twitter&label)](https://twitter.com/elevenlabsio)
[![PyPI - Python Version](https://img.shields.io/pypi/v/elevenlabs?style=flat&colorA=black&colorB=black)](https://pypi.org/project/elevenlabs/)
[![Downloads](https://static.pepy.tech/personalized-badge/elevenlabs?period=total&units=international_system&left_color=black&right_color=black&left_text=Downloads)](https://pepy.tech/project/elevenlabs)

The official Python SDK for [ElevenLabs](https://elevenlabs.io/). ElevenLabs brings the most compelling, rich and lifelike voices to creators and developers in just a few lines of code.

## 📖 API & Docs

Check out the [HTTP API documentation](https://elevenlabs.io/docs/api-reference).

## Install

```bash
pip install elevenlabs
```

## Usage

### Main Models

1. **Eleven Multilingual v2** (`eleven_multilingual_v2`)

    - Excels in stability, language diversity, and accent accuracy
    - Supports 29 languages
    - Recommended for most use cases

2. **Eleven Flash v2.5** (`eleven_flash_v2_5`)

    - Ultra-low latency
    - Supports 32 languages
    - Faster model, 50% lower price per character

2. **Eleven Turbo v2.5** (`eleven_turbo_v2_5`)

    - Good balance of quality and latency
    - Ideal for developer use cases where speed is crucial
    - Supports 32 languages

For more detailed information about these models and others, visit the [ElevenLabs Models documentation](https://elevenlabs.io/docs/models).

```py
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

load_dotenv()

client = ElevenLabs()

audio = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

play(audio)
```

<details> <summary> Play </summary>

🎧 **Try it out!** Want to hear our voices in action? Visit the [ElevenLabs Voice Lab](https://elevenlabs.io/voice-lab) to experiment with different voices, languages, and settings.

</details>

## Voices

List all your available voices with `voices()`.

```py
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="YOUR_API_KEY",
)

response = client.voices.search()
print(response.voices)
```

For information about the structure of the voices output, please refer to the [official ElevenLabs API documentation for Get Voices](https://elevenlabs.io/docs/api-reference/get-voices).

Build a voice object with custom settings to personalize the voice style, or call
`client.voices.get_settings("your-voice-id")` to get the default settings for the voice.

</details>

## Clone Voice

Clone your voice in an instant. Note that voice cloning requires an API key, see below.

```py
from elevenlabs.client import ElevenLabs
from elevenlabs import play

client = ElevenLabs(
  api_key="YOUR_API_KEY",
)

voice = client.voices.ivc.create(
    name="Alex",
    description="An old American male voice with a slight hoarseness in his throat. Perfect for news", # Optional
    files=["./sample_0.mp3", "./sample_1.mp3", "./sample_2.mp3"],
)
```

## Streaming

Stream audio in real-time, as it's being generated.

```py
from elevenlabs import stream
from elevenlabs.client import ElevenLabs

client = ElevenLabs()

audio_stream = client.text_to_speech.stream(
    text="This is a test",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2"
)

# option 1: play the streamed audio locally
stream(audio_stream)

# option 2: process the audio bytes manually
for chunk in audio_stream:
    if isinstance(chunk, bytes):
        print(chunk)

```

## Async Client

Use `AsyncElevenLabs` if you want to make API calls asynchronously.

```python
import asyncio

from elevenlabs.client import AsyncElevenLabs

eleven = AsyncElevenLabs(
  api_key="MY_API_KEY"
)

async def print_models() -> None:
    models = await eleven.models.list()
    print(models)

asyncio.run(print_models())
```

## Languages Supported

Explore [all models & languages](https://elevenlabs.io/docs/models).

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
