# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class GetPronunciationDictionaryMetadataResponse(UncheckedBaseModel):
    id: str = pydantic.Field()
    """
    The ID of the pronunciation dictionary.
    """

    latest_version_id: str = pydantic.Field()
    """
    The ID of the latest version of the pronunciation dictionary.
    """

    latest_version_rules_num: int = pydantic.Field()
    """
    The number of rules in the latest version of the pronunciation dictionary.
    """

    name: str = pydantic.Field()
    """
    The name of the pronunciation dictionary.
    """

    created_by: str = pydantic.Field()
    """
    The user ID of the creator of the pronunciation dictionary.
    """

    creation_time_unix: int = pydantic.Field()
    """
    The creation time of the pronunciation dictionary in Unix timestamp.
    """

    archived_time_unix: typing.Optional[int] = pydantic.Field(default=None)
    """
    The archive time of the pronunciation dictionary in Unix timestamp.
    """

    description: typing.Optional[str] = pydantic.Field(default=None)
    """
    The description of the pronunciation dictionary.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
