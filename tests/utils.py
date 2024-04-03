import os
import tempfile
import httpx

from typing import Sequence, Generator
from elevenlabs.client import ElevenLabs, \
    AsyncElevenLabs

IN_GITHUB = "GITHUB_ACTIONS" in os.environ

client = ElevenLabs()

async_client = AsyncElevenLabs()


def as_local_files(urls: Sequence[str]) -> Generator[str, None, None]:
    """Util to download files from urls and return local file paths"""

    temp_files = []
    for url in urls:
        response = httpx.get(url)
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(response.content)
        temp_files.append(temp_file)
        yield temp_file.name
    # Remove the files
    for temp_file in temp_files:
        temp_file.close()