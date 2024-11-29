# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .ban_reason_type import BanReasonType
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class AgentBan(UncheckedBaseModel):
    at_unix: int
    reason: typing.Optional[str] = None
    reason_type: BanReasonType

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
