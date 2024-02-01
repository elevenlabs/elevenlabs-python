from typing import Dict, List, Optional

from .client import ElevenLabs
from .types import GetVoicesResponseModel, VoiceSettings

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


def voices() -> GetVoicesResponseModel:
    client = ElevenLabs()
    return client.voices.get_all()


class Voice(pydantic.BaseModel):
    voice_id: str
    name: Optional[str] = None
    settings: Optional[VoiceSettings] = None


class VoiceClone(pydantic.BaseModel):
    name: str
    description: str = ""
    files: List[str]
    labels: Optional[Dict[str, str]] = None