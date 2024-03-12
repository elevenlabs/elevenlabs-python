from contextlib import contextmanager
import os
import tempfile
import requests
from typing import Sequence, Generator

from elevenlabs.client import ElevenLabs

IN_GITHUB = "GITHUB_ACTIONS" in os.environ

client = ElevenLabs()

@contextmanager
def as_local_files(urls: Sequence[str]) -> Generator[list[str], None, None]:
    """Util to download files from urls and return local file paths"""
    file_paths = []
    temp_files = []
    for url in urls:
        response = requests.get(url)
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(response.content)
        file_paths.append(temp_file.name)
        temp_files.append(temp_file)
    yield file_paths
    # Remove the files
    for temp_file in temp_files:
        temp_file.close()