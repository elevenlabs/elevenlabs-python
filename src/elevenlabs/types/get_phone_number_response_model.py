# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
from .telephony_provider import TelephonyProvider
import typing
from .phone_number_agent_info import PhoneNumberAgentInfo
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class GetPhoneNumberResponseModel(UncheckedBaseModel):
    phone_number: str = pydantic.Field()
    """
    Phone number
    """

    provider: TelephonyProvider = pydantic.Field(default="twilio")
    """
    Phone provider
    """

    label: str = pydantic.Field()
    """
    Label for the phone number
    """

    phone_number_id: str
    assigned_agent: typing.Optional[PhoneNumberAgentInfo] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
