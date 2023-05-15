from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import root_validator

from .base import API, api_base_url_v1
from .voice import VoiceSettings


class FeedbackItem(API):
    thumbs_up: bool
    feedback: str
    emotions: bool
    inaccurate_clone: bool
    glitches: bool
    audio_quality: bool
    other: bool
    review_status: str


class HistoryItem(API):
    history_item_id: str
    request_id: Optional[str]
    voice_id: str
    text: str
    date: Optional[datetime]
    date_unix: int
    character_count_change_from: int
    character_count_change_to: int
    character_count_change: Optional[int]
    content_type: str
    settings: Optional[VoiceSettings]
    feedback: Optional[FeedbackItem]
    _audio: Optional[bytes] = None

    @root_validator
    def computed(cls, values):
        # Compute character count field
        change_from = values["character_count_change_from"]
        change_to = values["character_count_change_to"]
        values["character_count_change"] = change_to - change_from
        # Compute datetime field
        values["date"] = datetime.utcfromtimestamp(values["date_unix"])
        return values

    @classmethod
    def from_id(cls, history_item_id: str) -> HistoryItem:
        url = f"{api_base_url_v1}/history/{history_item_id}"
        response = API.get(url).json()
        return cls(**response)

    @property
    def audio(self) -> bytes:
        url = f"{api_base_url_v1}/history/{self.history_item_id}/audio"
        if self._audio is None:
            self._audio = API.get(url).content
        return self._audio


class History(API):
    history: List[HistoryItem]

    @classmethod
    def from_api(cls) -> History:
        url = f"{api_base_url_v1}/history"
        response = API.get(url).json()
        return cls(**response)

    def __getitem__(self, idx: int) -> HistoryItem:
        return self.history[idx]

    def __iter__(self):
        return iter(self.history)
