from __future__ import annotations

from enum import Enum
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


class VoiceSample(API):
    sample_id: str = ""
    file_name: str = ""
    mime_type: str = ""
    size_bytes: Optional[int] = None
    hash: str = ""


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

class VoiceEdit(API):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = ""
    files: Optional[List[str]] = []
    labels: Optional[Dict[str, str]]
    _files_tuple: Optional[List[Tuple]] = None

    @root_validator
    def computed_files_tuple(cls, values) -> List[str]:
        files_tuple = []
        if 'files' in values:
            for filepath in values["files"]:
                b = open(filepath, "rb")
                file_tuple = ("files", (f"{Path(filepath).stem}_{id(b)}", b, "audio/mpeg"))
                files_tuple.append(file_tuple)
            values["_files_tuple"] = files_tuple
            return values


class Gender(str, Enum):
    female = "female"
    male = "male"


class Age(str, Enum):
    young = "young"
    middle_aged = "middle_aged"
    old = "old"


class Accent(str, Enum):
    british = "british"
    american = "american"
    african = "african"
    australian = "australian"
    indian = "indian"


class VoiceDesign(API):
    name: str
    text: str = Field(..., min_length=100)
    gender: Gender
    age: Age
    accent: Accent
    accent_strength: float = Field(..., gt=0.3, lt=2.0)
    # The following fields are populated only after `generate` is called
    generated_voice_id: Optional[str]
    audio: Optional[bytes]

    def generate(self) -> bytes:
        url = f"{api_base_url_v1}/voice-generation/generate-voice"
        response = API.post(url, json=self.dict())
        self.generated_voice_id = response.headers["generated_voice_id"]
        self.audio = response.content
        return self.audio  # type: ignore


class Voice(API):
    voice_id: str
    name: Optional[str]
    category: Optional[str]
    description: Optional[str]
    labels: Optional[Dict[str, str]]
    samples: Optional[List[VoiceSample]]
    settings: Optional[VoiceSettings]
    design: Optional[VoiceDesign]

    @classmethod
    def from_id(cls, voice_id: str):
        url = f"{api_base_url_v1}/voices/{voice_id}?with_settings=true"
        return cls(**API.get(url).json())

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
        return cls.from_id(voice_id)

    @classmethod
    def from_design(cls, voice_design: VoiceDesign):
        # If the voice design has not been generated yet, generate it
        if voice_design.generated_voice_id is None:
            voice_design.generate()
        # Create the voice from the voice design
        url = f"{api_base_url_v1}/voice-generation/create-voice"
        data = dict(
            voice_name=voice_design.name,
            generated_voice_id=voice_design.generated_voice_id,
        )
        response = API.post(url, json=data)
        voice = cls.from_id(voice_id=response.json()["voice_id"])
        voice.design = voice_design
        return voice

    @classmethod
    def edit_voice(cls, voice_id: str, voice_clone: VoiceClone) -> Voice:
        """
        Args:
            - voice_id - Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
            - voice_clone - VoiceEdit(name='changed', description='changed') 
        """
        url = f"{api_base_url_v1}/voices/{voice_id}/edit"
        data = voice_clone.dict()
        data["lables"] = str(data.pop("labels"))
        del data["files"]
        files = data.pop("_files_tuple")
        status = API.post(url, data=data, files=files).json()['status']
        return cls.from_id(voice_id)
    
    @validator("settings")
    def computed_settings(cls, v: VoiceSettings, values) -> VoiceSettings:
        url = f"{api_base_url_v1}/voices/{values['voice_id']}/settings"
        return v if v else VoiceSettings(**API.get(url).json())

    def delete(self):
        API.delete(f"{api_base_url_v1}/voices/{self.voice_id}")

class Voices(API):
    voices: List[Voice]

    @classmethod
    def from_api(cls, api_key: Optional[str] = None):
        url = f"{api_base_url_v1}/voices"
        response = API.get(url).json()
        print(response)
        return cls(**response)

    def add_clone(self, voice_clone: VoiceClone) -> Voice:
        pass

    def __getitem__(self, idx: int) -> Voice:
        return self.voices[idx]

    def __iter__(self):
        return iter(self.voices)
