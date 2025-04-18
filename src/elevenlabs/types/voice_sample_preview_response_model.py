# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class VoiceSamplePreviewResponseModel(UncheckedBaseModel):
    audio_base_64: str = pydantic.Field()
    """
    The base64 encoded audio.
    """

    voice_id: str = pydantic.Field()
    """
    The ID of the voice.
    """

    sample_id: str = pydantic.Field()
    """
    The ID of the sample.
    """

    media_type: str = pydantic.Field()
    """
    The media type of the audio.
    """

    duration_secs: typing.Optional[float] = pydantic.Field(default=None)
    """
    The duration of the audio in seconds.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
