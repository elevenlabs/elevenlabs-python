# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel
from .conversation_config_client_override_output import ConversationConfigClientOverrideOutput
from .conversation_initiation_client_data_request_output_dynamic_variables_value import (
    ConversationInitiationClientDataRequestOutputDynamicVariablesValue,
)


class ConversationInitiationClientDataRequestOutput(UncheckedBaseModel):
    conversation_config_override: typing.Optional[ConversationConfigClientOverrideOutput] = None
    custom_llm_extra_body: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = None
    user_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    ID of the end user participating in this conversation (for agent owner's user identification)
    """

    dynamic_variables: typing.Optional[
        typing.Dict[str, typing.Optional[ConversationInitiationClientDataRequestOutputDynamicVariablesValue]]
    ] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
