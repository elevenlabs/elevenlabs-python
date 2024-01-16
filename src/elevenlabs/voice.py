from typing import Optional
from .types import VoiceSettings

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class Voice(pydantic.BaseModel):
    voice_id: str
    name: Optional[str] = None
    settings: Optional[VoiceSettings] = None