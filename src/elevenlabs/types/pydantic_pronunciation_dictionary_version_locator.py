# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class PydanticPronunciationDictionaryVersionLocator(UncheckedBaseModel):
    """
    A locator for other documents to be able to reference a specific dictionary and it's version.
    This is a pydantic version of PronunciationDictionaryVersionLocatorDBModel.
    Required to ensure compat with the rest of the agent data models.
    """

    pronunciation_dictionary_id: str = pydantic.Field()
    """
    The ID of the pronunciation dictionary
    """

    version_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The ID of the version of the pronunciation dictionary
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
