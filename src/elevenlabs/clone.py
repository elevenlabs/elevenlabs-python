import json
from typing import Dict, List, Optional

from .client import ElevenLabs
from .voice import Voice


def clone(
    name: str,
    api_key: Optional[str] = None,
    description: str = "",
    files: List[str] = [],
    labels: Optional[Dict[str, str]] = dict(),
) -> Voice:
    client = ElevenLabs(api_key=api_key)
    addVoiceResponse = client.voices.add(
        name=name, description=description, files=files, labels=str(json.dumps(labels))
    )
    voiceResponse = client.voices.get(voice_id=addVoiceResponse.voice_id)
    return Voice(
        voice_id=voiceResponse.voice_id,
        name=voiceResponse.name,
        settings=voiceResponse.settings,
    )