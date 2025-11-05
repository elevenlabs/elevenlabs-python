import os
import tempfile
import httpx

from typing import Sequence, Generator

IN_GITHUB = "GITHUB_ACTIONS" in os.environ

DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"
DEFAULT_TEXT = "Hello"
DEFAULT_MODEL = "eleven_multilingual_v2"
DEFAULT_VOICE_FILE = "tests/fixtures/voice_sample.mp3"


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
