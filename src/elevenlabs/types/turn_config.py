# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
import pydantic
from .turn_mode import TurnMode
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class TurnConfig(UncheckedBaseModel):
    turn_timeout: typing.Optional[float] = pydantic.Field(default=None)
    """
    Maximum wait time for the user’s reply before re-engaging the user
    """

    silence_end_call_timeout: typing.Optional[float] = pydantic.Field(default=None)
    """
    Maximum wait time since the user last spoke before terminating the call
    """

    mode: typing.Optional[TurnMode] = pydantic.Field(default=None)
    """
    The mode of turn detection
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
