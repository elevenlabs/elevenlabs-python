from __future__ import annotations

from .base import API, api_base_url_v1


class Subscription(API):
    status: str
    tier: str
    currency: str
    character_count: int
    character_limit: int
    voice_limit: int
    professional_voice_limit: int
    allowed_to_extend_character_limit: bool
    can_extend_character_limit: bool
    can_extend_voice_limit: bool
    can_use_instant_voice_cloning: bool
    next_character_count_reset_unix: int


class User(API):
    subscription: Subscription

    @classmethod
    def from_api(cls) -> User:
        url = f"{api_base_url_v1}/user"
        response = cls.get(url).json()
        return cls(**response)
