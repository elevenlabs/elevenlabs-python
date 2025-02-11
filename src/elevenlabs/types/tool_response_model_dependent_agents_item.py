# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .dependent_available_agent_identifier_access_level import DependentAvailableAgentIdentifierAccessLevel
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
import typing_extensions
from ..core.unchecked_base_model import UnionMetadata


class ToolResponseModelDependentAgentsItem_Available(UncheckedBaseModel):
    type: typing.Literal["available"] = "available"
    id: str
    name: str
    created_at_unix_secs: int
    access_level: DependentAvailableAgentIdentifierAccessLevel

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class ToolResponseModelDependentAgentsItem_Unknown(UncheckedBaseModel):
    type: typing.Literal["unknown"] = "unknown"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


ToolResponseModelDependentAgentsItem = typing_extensions.Annotated[
    typing.Union[ToolResponseModelDependentAgentsItem_Available, ToolResponseModelDependentAgentsItem_Unknown],
    UnionMetadata(discriminant="type"),
]
