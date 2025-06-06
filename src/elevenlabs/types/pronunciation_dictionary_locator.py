# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel


class PronunciationDictionaryLocator(UncheckedBaseModel):
    """
    Identifies a specific pronunciation dictionary to use
    """

    pronunciation_dictionary_id: str = pydantic.Field()
    """
    The unique identifier of the pronunciation dictionary
    """

    version_id: str = pydantic.Field()
    """
    The version identifier of the pronunciation dictionary
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
