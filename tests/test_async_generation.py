import asyncio
import pytest

from .utils import async_client
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
        play(out)
    asyncio.run(main())
