from typing import List, Optional

from pydantic import validator

from .base import API, api_base_url_v1


class VoiceSettings(API):
    stability: float
    similarity_boost: float


class Voice(API):
    voice_id: str
    name: Optional[str]
    category: Optional[str]
    settings: Optional[VoiceSettings]

    @classmethod
    def from_id(cls, voice_id: str):
        url = f"{api_base_url_v1}/voices/{voice_id}?with_settings=true"
        return cls(**cls.get(url).json())

    @validator("settings")
    def computed_settings(cls, v: VoiceSettings, values) -> VoiceSettings:
        url = f"{api_base_url_v1}/voices/{values['voice_id']}/settings"
        return v if v else VoiceSettings(**cls.get(url).json())


class Voices(API):
    voices: List[Voice]

    @classmethod
    def from_api(cls):
        url = f"{api_base_url_v1}/voices"
        response = cls.get(url).json()
        return cls(**response)

    def __getitem__(self, idx: int) -> Voice:
        return self.voices[idx]

    def __iter__(self):
        return iter(self.voices)
