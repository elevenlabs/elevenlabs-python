import asyncio
import pytest

from .utils import IN_GITHUB
from elevenlabs import AsyncElevenLabs
from elevenlabs import play

async_client = AsyncElevenLabs()

def test_generate_stream() -> None:
    async def main():
        async def text_stream():
            yield "Hi there, I'm Eleven Labs "
            yield "I'm an AI Audio Research Company "

        audio_stream = await async_client.generate(
            text=text_stream(),
            voice="Adam",
            model="eleven_monolingual_v1",
            stream=True
        )

        if not IN_GITHUB:
            stream(audio_stream)  # type: ignore
    asyncio.run(main())