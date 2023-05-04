from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pydantic import Field, root_validator, validator

from .base import API, api_base_url_v1
from .error import APIError


class UnauthorizedVoiceCloningError(APIError):
    pass


class VoiceSettings(API):
    stability: float = Field(..., ge=0.0, le=1.0)
    similarity_boost: float = Field(..., ge=0.0, le=1.0)


class VoiceClone(API):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = ""
    files: List[str] = Field(..., min_items=1, max_items=25)
    labels: Optional[Dict[str, str]]
    _files_tuple: Optional[List[Tuple]] = None

    @root_validator
    def computed_files_tuple(cls, values) -> List[str]:
        files_tuple = []
        for filepath in values["files"]:
            b = open(filepath, "rb")
            file_tuple = ("files", (f"{Path(filepath).stem}_{id(b)}", b, "audio/mpeg"))
            files_tuple.append(file_tuple)
        values["_files_tuple"] = files_tuple
        return values


class Voice(API):
    voice_id: str
    name: Optional[str]
    category: Optional[str]
    settings: Optional[VoiceSettings]

    @classmethod
    def from_id(cls, voice_id: str):
        url = f"{api_base_url_v1}/voices/{voice_id}?with_settings=true"
        return cls(**cls.get(url).json())

    @classmethod
    def from_clone(cls, voice_clone: VoiceClone) -> Voice:
        url = f"{api_base_url_v1}/voices/add"
        data = voice_clone.dict()
        data["lables"] = str(data.pop("labels"))
        del data["files"]
        files = data.pop("_files_tuple")
        try:
            voice_id = API.post(url, data=data, files=files).json()["voice_id"]
        except APIError as e:
            if e.http_error.status == "can_not_use_instant_voice_cloning":
                raise UnauthorizedVoiceCloningError(e.http_error)
            raise
        return voice_id

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

    def add_clone(self, voice_clone: VoiceClone) -> Voice:
        pass

    def __getitem__(self, idx: int) -> Voice:
        return self.voices[idx]

    def __iter__(self):
        return iter(self.voices)
