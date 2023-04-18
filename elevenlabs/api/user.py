from __future__ import annotations

from typing import List

from .base import API, api_base_url_v1


class Models(API):
    model_id: str
    display_name: str


class Subscription(API):
    character_count: int
    character_limit: int
    available_models: List[Models]
    status: str


class User(API):
    subscription: Subscription

    @classmethod
    def from_api(cls) -> User:
        url = f"{api_base_url_v1}/user"
        response = cls.get(url).json()
        return cls(**response)
