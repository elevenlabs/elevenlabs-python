# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .generation_config import GenerationConfig
from .realtime_voice_settings import RealtimeVoiceSettings

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class SendText(pydantic.BaseModel):
    text: str = pydantic.Field()
    """
    Should always end with a single space string `" "`. In the first message, the text should be a space `" "`.
    """

    try_trigger_generation: typing.Optional[bool] = pydantic.Field(default=None)
    """
    This is an advanced setting that most users shouldn't need to use. It relates to our generation schedule
    explained [here](#understanding-how-our-websockets-buffer-text).
    
    Use this to attempt to immediately trigger the generation of audio, overriding the `chunk_length_schedule`.
    Unlike flush, `try_trigger_generation` will only generate audio if our
    buffer contains more than a minimum
    threshold of characters, this is to ensure a higher quality response from our model.
    
    Note that overriding the chunk schedule to generate small amounts of
    text may result in lower quality audio, therefore, only use this parameter if you
    really need text to be processed immediately. We generally recommend keeping the default value of
    `false` and adjusting the `chunk_length_schedule` in the `generation_config` instead.
    """

    voice_settings: typing.Optional[RealtimeVoiceSettings] = None
    generation_config: typing.Optional[GenerationConfig] = pydantic.Field(default=None)
    """
    This property should only be provided in the first message you send.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
