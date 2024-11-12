import asyncio
import pytest

from .utils import IN_GITHUB, async_client
from elevenlabs import play

def test_async_generation(): 
    async def main():
        results = await async_client.generate(
          voice='Rachel',
          model='eleven_multilingual_v2',
          text='This is an example sentence',
        )
        out = b''
        async for value in results:
            out += value
        if not IN_GITHUB:
            play(out)

        results = await async_client.generate(
          voice='Rachel',
          model='eleven_multilingual_v2',
          text='This is an example sentence with streaming',
          stream=True
        )
        out = b''
        async for value in results:
            out += value
        if not IN_GITHUB:
            play(out)
    asyncio.run(main())

def test_generate_stream() -> None:
    async def main():
        async def text_stream():
            yield "Hi there, I'm Eleven "
            yield "I'm a text to speech API "

        audio_stream = await async_client.generate(
            text=text_stream(),
            voice="Nicole",
            model="eleven_monolingual_v1",
            stream=True
        )

        if not IN_GITHUB:
            stream(audio_stream)  # type: ignore
    asyncio.run(main())
