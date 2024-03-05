# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class LibraryVoiceResponse(pydantic.BaseModel):
    public_owner_id: str
    voice_id: str
    date_unix: int
    name: str
    accent: str
    gender: str
    age: str
    descriptive: str
    use_case: str
    category: str
    language: str
    description: str
    preview_url: str
    usage_character_count_1_y: int = pydantic.Field(alias="usage_character_count_1y")
    usage_character_count_7_d: int = pydantic.Field(alias="usage_character_count_7d")
    cloned_by_count: int
    rate: float
    free_users_allowed: bool
    live_moderation_enabled: bool
    notice_period: int
    instagram_username: str
    twitter_username: str
    youtube_username: str
    tiktok_username: str
    featured: bool

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        json_encoders = {dt.datetime: serialize_datetime}
