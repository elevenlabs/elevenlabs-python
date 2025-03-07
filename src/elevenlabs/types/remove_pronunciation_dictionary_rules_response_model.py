# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class RemovePronunciationDictionaryRulesResponseModel(UncheckedBaseModel):
    id: str = pydantic.Field()
    """
    The ID of the pronunciation dictionary.
    """

    version_id: str = pydantic.Field()
    """
    The version ID of the pronunciation dictionary.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
