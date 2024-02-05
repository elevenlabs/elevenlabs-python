import json
import os
from typing import Dict, List, Optional

from .client import ElevenLabs
from .voice import Voice


def clone(
    name: str,
    api_key: Optional[str] = os.getenv("ELEVEN_API_KEY"),
    description: str = "",
    files: List[str] = [],
    labels: Optional[Dict[str, str]] = dict(),
) -> Voice:
    client = ElevenLabs(api_key=api_key)
    add_voice_response = client.voices.add(
        name=name,
        description=description, 
        files=[open(file, 'rb') for file in files],
        labels=str(json.dumps(labels or {}))
    )
    voice = client.voices.get(voice_id=add_voice_response.voice_id)
    return Voice(
        **voice.dict()
    )