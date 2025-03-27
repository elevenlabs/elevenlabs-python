# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from .chapter_with_content_response_model_state import (
    ChapterWithContentResponseModelState,
)
from .chapter_statistics_response import ChapterStatisticsResponse
from .chapter_content_response_model import ChapterContentResponseModel
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ChapterWithContentResponseModel(UncheckedBaseModel):
    chapter_id: str = pydantic.Field()
    """
    The ID of the chapter.
    """

    name: str = pydantic.Field()
    """
    The name of the chapter.
    """

    last_conversion_date_unix: typing.Optional[int] = pydantic.Field(default=None)
    """
    The last conversion date of the chapter.
    """

    conversion_progress: typing.Optional[float] = pydantic.Field(default=None)
    """
    The conversion progress of the chapter.
    """

    can_be_downloaded: bool = pydantic.Field()
    """
    Whether the chapter can be downloaded.
    """

    state: ChapterWithContentResponseModelState = pydantic.Field()
    """
    The state of the chapter.
    """

    statistics: typing.Optional[ChapterStatisticsResponse] = pydantic.Field(default=None)
    """
    The statistics of the chapter.
    """

    last_conversion_error: typing.Optional[str] = pydantic.Field(default=None)
    """
    The last conversion error of the chapter.
    """

    content: ChapterContentResponseModel

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
