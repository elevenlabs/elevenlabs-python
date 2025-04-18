# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .system_tool_config_output_params import SystemToolConfigOutputParams
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class SystemToolConfigOutput(UncheckedBaseModel):
    """
    A system tool is a tool that is used to call a system method in the server
    """

    id: typing.Optional[str] = None
    name: str
    description: str
    params: SystemToolConfigOutputParams

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
