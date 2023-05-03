from __future__ import annotations

from .base import API, api_base_url_v1


class Subscription(API):
    character_count: int
    character_limit: int
    status: str


class User(API):
    subscription: Subscription

    @classmethod
    def from_api(cls) -> User:
        url = f"{api_base_url_v1}/user"
        response = cls.get(url).json()
        return cls(**response)
