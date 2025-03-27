# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from .audio_native_project_settings_response_model import (
    AudioNativeProjectSettingsResponseModel,
)
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class GetAudioNativeProjectSettingsResponseModel(UncheckedBaseModel):
    enabled: bool = pydantic.Field()
    """
    Whether the project is enabled.
    """

    snapshot_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The ID of the latest snapshot of the project.
    """

    settings: typing.Optional[AudioNativeProjectSettingsResponseModel] = pydantic.Field(default=None)
    """
    The settings of the project.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
