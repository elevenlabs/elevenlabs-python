# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .dubbing_media_metadata import DubbingMediaMetadata
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class DubbingMetadataResponse(UncheckedBaseModel):
    dubbing_id: str
    name: str
    status: str
    target_languages: typing.List[str]
    media_metadata: typing.Optional[DubbingMediaMetadata] = None
    error: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
