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

## 👥 Voices

```py
from elevenlabs import generate, play

voice = "Adam"
text = f""" Hi! My name is {voice}, nice to meet you! """
audio = generate(text, voice=voice)
play(audio)
```

## Streaming

```py
from elevenlabs import generate, stream

text = """ This is a... streaming voice!! """
audio_stream = generate(text, stream=True)
stream(audio_stream)
```
