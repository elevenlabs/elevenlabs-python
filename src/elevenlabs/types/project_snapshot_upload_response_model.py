# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
from .project_snapshot_upload_response_model_status import ProjectSnapshotUploadResponseModelStatus
import pydantic
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ProjectSnapshotUploadResponseModel(UncheckedBaseModel):
    status: ProjectSnapshotUploadResponseModelStatus = pydantic.Field()
    """
    The status of the snapshot upload.
    """

    acx_volume_normalization: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether volume normalization was applied to the snapshot.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
