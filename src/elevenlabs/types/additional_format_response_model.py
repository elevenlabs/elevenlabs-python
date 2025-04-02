# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing_extensions
from ..core.serialization import FieldMetadata
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class AdditionalFormatResponseModel(UncheckedBaseModel):
    requested_format: str = pydantic.Field()
    """
    The requested format.
    """

    file_extension: str = pydantic.Field()
    """
    The file extension of the additional format.
    """

    content_type: str = pydantic.Field()
    """
    The content type of the additional format.
    """

    is_base_64_encoded: typing_extensions.Annotated[bool, FieldMetadata(alias="is_base64_encoded")] = pydantic.Field()
    """
    Whether the content is base64 encoded.
    """

    content: str = pydantic.Field()
    """
    The content of the additional format.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
