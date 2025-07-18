# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel


class VoicePreviewResponseModel(UncheckedBaseModel):
    audio_base_64: str = pydantic.Field()
    """
    The base64 encoded audio of the preview.
    """

    generated_voice_id: str = pydantic.Field()
    """
    The ID of the generated voice. Use it to create a voice from the preview.
    """

    media_type: str = pydantic.Field()
    """
    The media type of the preview.
    """

    duration_secs: float = pydantic.Field()
    """
    The duration of the preview in seconds.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
