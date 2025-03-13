# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from .send_text_voice_settings import SendTextVoiceSettings
from .send_text_generator_config import SendTextGeneratorConfig
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class SendText(UncheckedBaseModel):
    text: str = pydantic.Field()
    """
    The text to be sent to the API for audio generation. SHould always end with a single space string.
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

    voice_settings: typing.Optional[SendTextVoiceSettings] = None
    generator_config: typing.Optional[SendTextGeneratorConfig] = None
    flush: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Flush forces the generation of audio. Set this value to true when you have finished sending text, but want to keep the websocket connection open.
    
    This is useful when you want to ensure that the last chunk of audio is generated even when the length of text sent is smaller than the value set in chunk_length_schedule (e.g. 120 or 50).
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
