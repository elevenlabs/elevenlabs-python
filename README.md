<img src="LOGO.png"></img>
[![PyPI - Python Version](https://img.shields.io/pypi/v/elevenlabs?style=flat&colorA=black&colorB=black)](https://pypi.org/project/elevenlabs/)
[![Downloads](https://static.pepy.tech/personalized-badge/elevenlabs?period=total&units=international_system&left_color=black&right_color=black&left_text=Downloads)](https://pepy.tech/project/elevenlabs)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com?style=social&label=elevenlabsio)](https://twitter.com/elevenlabsio)


The official Python API for [Elevenlabs](https://elevenlabs.io/) text-to-speech software. Eleven brings the most compelling, rich and lifelike voices to creators and developers in just a few lines of code.


## ⚙️ Install

```bash
pip install elevenlabs
```

## 🗣️ Usage
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/flavioschneider/49468d728a816c6538fd2f56b3b50b96/elevenlabs-python.ipynb)

```py
from elevenlabs import generate, play

audio = generate("Hi! I'm the world's most advanced text-to-speech system, made by elevenlabs.")

play(audio)
```

<details> <summary> Play </summary>

<i> Don't forget to unmute the player! </i>

[voice.webm](https://user-images.githubusercontent.com/12028621/232730309-e47bc907-78ec-4acf-a73a-0d77ba25fd6b.webm)

</details>

### 👥 Voices

```py
from elevenlabs import generate, play

voice = "Bella"
audio = generate(
  text=f"Hi! My name is {voice}, nice to meet you!",
  voice=voice
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

### 🚿 Streaming

```py
from elevenlabs import generate, stream

audio_stream = generate(
  text="This is a... streaming voice!!",
  stream=True
)

stream(audio_stream)
```

### 🔑 API Key

The basic API has a limited number of characters. To increase this limit, you can get a free API key from [Elevenlabs](https://elevenlabs.io/) and set is as environment variable `ELEVEN_API_KEY`. Alternatively pass the `api_key` string argument to the `generate` function, or set it programmatically as:
```py
from elevenlabs import set_api_key
set_api_key("<YOUR_API_KEY>")
```

## 📖 API & Docs

Learn more about the [Python API](API.md), or check out the [HTTP API documentation](https://docs.elevenlabs.io/quickstart).
