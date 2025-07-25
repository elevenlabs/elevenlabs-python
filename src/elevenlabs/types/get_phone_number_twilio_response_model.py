# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel
from .phone_number_agent_info import PhoneNumberAgentInfo


class GetPhoneNumberTwilioResponseModel(UncheckedBaseModel):
    phone_number: str = pydantic.Field()
    """
    Phone number
    """

    label: str = pydantic.Field()
    """
    Label for the phone number
    """

    supports_inbound: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether this phone number supports inbound calls
    """

    supports_outbound: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether this phone number supports outbound calls
    """

    phone_number_id: str = pydantic.Field()
    """
    The ID of the phone number
    """

    assigned_agent: typing.Optional[PhoneNumberAgentInfo] = pydantic.Field(default=None)
    """
    The agent that is assigned to the phone number
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
