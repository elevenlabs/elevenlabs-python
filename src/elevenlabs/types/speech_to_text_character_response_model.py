# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class SpeechToTextCharacterResponseModel(UncheckedBaseModel):
    text: str = pydantic.Field()
    """
    The character that was transcribed.
    """

    start: float = pydantic.Field()
    """
    The start time of the character in seconds.
    """

    end: float = pydantic.Field()
    """
    The end time of the character in seconds.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
