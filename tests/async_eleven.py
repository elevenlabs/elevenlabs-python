import asyncio
from elevenlabs import AsyncElevenLabs

client = AsyncElevenLabs(
    api_key="YOUR_API_KEY",
)

async def main() -> None:
    audio = await client.text_to_speech.convert_to_bytes(
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        output_format="mp3_44100_128",
        text="The first move is what sets everything in motion.",
        model_id="eleven_multilingual_v2",
    )

    print(type(audio))
    print(len(audio))

    with open("test.mp3", "wb") as f:
        f.write(audio)

asyncio.run(main())