# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .dependent_available_agent_tool_identifier_access_level import DependentAvailableAgentToolIdentifierAccessLevel
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class DependentAvailableAgentToolIdentifier(UncheckedBaseModel):
    agent_id: str
    agent_name: str
    used_by: typing.List[str]
    created_at_unix_secs: int
    access_level: DependentAvailableAgentToolIdentifierAccessLevel

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
