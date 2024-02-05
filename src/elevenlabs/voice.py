import httpx
from typing import Dict, List, Optional

from elevenlabs import environment

from .core.jsonable_encoder import jsonable_encoder
from .client import ElevenLabs
from .types import (
  GetVoicesResponseModel, 
  VoiceSettings, 
  VoiceSample, 
  Age, 
  Gender, 
  Accent
  )

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class Voice(pydantic.BaseModel):
    voice_id: str
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    samples: Optional[List[VoiceSample]] = None
    preview_url: Optional[str] = None
    settings: Optional[VoiceSettings] = None


def voices() -> List[Voice]:
    client = ElevenLabs()
    response = client.voices.get_all()
    return [Voice(**voice.dict()) for voice in response.voices]


class VoiceClone(pydantic.BaseModel):
    name: str
    description: str = ""
    files: List[str]
    labels: Optional[Dict[str, str]] = None
