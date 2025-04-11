# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .pronunciation_dictionary_version_response_model_permission_on_resource import (
    PronunciationDictionaryVersionResponseModelPermissionOnResource,
)
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class PronunciationDictionaryVersionResponseModel(UncheckedBaseModel):
    version_id: str
    version_rules_num: int
    pronunciation_dictionary_id: str
    dictionary_name: str
    version_name: str
    permission_on_resource: typing.Optional[PronunciationDictionaryVersionResponseModelPermissionOnResource] = None
    created_by: str
    creation_time_unix: int
    archived_time_unix: typing.Optional[int] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
