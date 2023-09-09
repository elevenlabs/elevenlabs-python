from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import Field

from .base import API, Listable, api_base_url_v1
from .error import APIError


class UnauthorizedVoiceCloningError(APIError):
    pass


class VoiceSettings(API):
    stability: float = Field(..., ge=0.0, le=1.0)
    similarity_boost: float = Field(..., ge=0.0, le=1.0)
    style: Optional[float] = Field(None, ge=0.0, le=1.0)
    use_speaker_boost: Optional[bool] = None

    @classmethod
    def from_voice_id(cls, voice_id: str) -> VoiceSettings:
        url = f"{api_base_url_v1}/voices/{voice_id}/settings"
        return cls(**API.get(url).json())

    @classmethod
    def from_default(cls) -> VoiceSettings:
        url = f"{api_base_url_v1}/voices/settings/default"
        return cls(**API.get(url).json())


class VoiceSample(API):
    sample_id: str = ""
    file_name: str = ""
    mime_type: str = ""
    size_bytes: Optional[int] = None
    hash: str = ""


class VoiceClone(API):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = ""
    files: List[str] = Field(..., min_length=1, max_length=25)
    labels: Optional[Dict[str, str]] = None

    @property
    def files_tuple(self):
        files_tuple = []
        for filepath in self.files:
            b = open(filepath, "rb")
            file_tuple = ("files", (f"{Path(filepath).stem}_{id(b)}", b, "audio/mpeg"))
            files_tuple.append(file_tuple)
        return files_tuple


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
    voice_description: str
    gender: Gender
    age: Age
    accent: Accent
    accent_strength: float = Field(..., gt=0.3, lt=2.0)
    # The following fields are populated only after `generate` is called
    generated_voice_id: Optional[str] = None
    audio: Optional[bytes] = None

    def generate(self) -> bytes:
        url = f"{api_base_url_v1}/voice-generation/generate-voice"
        response = API.post(url, json=self.model_dump())
        self.generated_voice_id = response.headers["generated_voice_id"]
        self.audio = response.content
        return self.audio  # type: ignore


class Voice(API):
    voice_id: str
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    samples: Optional[List[VoiceSample]] = None
    design: Optional[VoiceDesign] = None
    preview_url: Optional[str] = None
    settings: Optional[VoiceSettings] = None

    @classmethod
    def from_id(cls, voice_id: str):
        url = f"{api_base_url_v1}/voices/{voice_id}?with_settings=true"
        return cls(**API.get(url).json())

    @classmethod
    def from_clone(cls, voice_clone: VoiceClone) -> Voice:
        url = f"{api_base_url_v1}/voices/add"
        data = dict(
            name=voice_clone.name,
            description=voice_clone.description,
            labels=str(json.dumps(voice_clone.labels or {})),
        )
        files = voice_clone.files_tuple
        try:
            voice_id = API.post(url, data=data, files=files).json()["voice_id"]
        except APIError as e:
            if e.status == "can_not_use_instant_voice_cloning":
                raise UnauthorizedVoiceCloningError(e.message)
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
            voice_description=voice_design.voice_description,
        )
        response = API.post(url, json=data)
        voice = cls.from_id(voice_id=response.json()["voice_id"])
        voice.design = voice_design
        return voice

    def fetch_settings(self):
        self.settings = VoiceSettings.from_voice_id(self.voice_id)

    @staticmethod
    def default_settings() -> VoiceSettings:
        return VoiceSettings.from_default()

    def delete(self):
        API.delete(f"{api_base_url_v1}/voices/{self.voice_id}")

    @classmethod
    def edit_by_id(
        cls,
        voice_id: str,
        name: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        voice_settings: Optional[VoiceSettings] = None,
        voice_clone: Optional[VoiceClone] = None,
    ) -> Voice:
        url = f"{api_base_url_v1}/voices/{voice_id}/edit"
        data = {}
        data.update(dict(name=name) if name else {})
        data.update(dict(labels=str(labels)) if labels else {})
        data.update(dict(description=description) if description else {})

        files = None
        if voice_clone:
            clone_data = voice_clone.model_dump()
            clone_data["labels"] = str(clone_data.pop("labels"))
            del clone_data["files"]
            files = clone_data.pop("_files_tuple")

        if data or files:
            API.post(url, data=data, files=files)

        if voice_settings:
            settings_url = f"{api_base_url_v1}/voices/{voice_id}/settings/edit"
            API.post(settings_url, json=voice_settings.model_dump())

        return Voice.from_id(voice_id)

    def edit(self, **kwargs):
        updated_voice = Voice.edit_by_id(voice_id=self.voice_id, **kwargs)
        self.__dict__.update(updated_voice.model_dump())


class Voices(Listable, API):
    voices: List[Voice]

    @classmethod
    def from_api(cls, api_key: Optional[str] = None):
        url = f"{api_base_url_v1}/voices"
        response = API.get(url).json()
        return cls(**response)

    @property
    def items(self):
        return self.voices
