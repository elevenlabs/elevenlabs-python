# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class BodyAddToKnowledgeBaseV1ConvaiAddToKnowledgeBasePost(UncheckedBaseModel):
    url: typing.Optional[str] = pydantic.Field(default=None)
    """
    URL to a page of documentation that the agent will have access to in order to interact with users.
    """

    file: typing.Optional[str] = pydantic.Field(default=None)
    """
    Documentation that the agent will have access to in order to interact with users.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
