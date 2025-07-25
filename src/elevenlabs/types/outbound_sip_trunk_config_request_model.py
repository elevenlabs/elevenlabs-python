# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel
from .sip_media_encryption_enum import SipMediaEncryptionEnum
from .sip_trunk_credentials_request_model import SipTrunkCredentialsRequestModel
from .sip_trunk_transport_enum import SipTrunkTransportEnum


class OutboundSipTrunkConfigRequestModel(UncheckedBaseModel):
    address: str = pydantic.Field()
    """
    Hostname or IP the SIP INVITE is sent to.
    """

    transport: typing.Optional[SipTrunkTransportEnum] = pydantic.Field(default=None)
    """
    Protocol to use for SIP transport (signalling layer).
    """

    media_encryption: typing.Optional[SipMediaEncryptionEnum] = pydantic.Field(default=None)
    """
    Whether or not to encrypt media (data layer).
    """

    headers: typing.Optional[typing.Dict[str, str]] = pydantic.Field(default=None)
    """
    SIP X-* headers for INVITE request. These headers are sent as-is and may help identify this call.
    """

    credentials: typing.Optional[SipTrunkCredentialsRequestModel] = pydantic.Field(default=None)
    """
    Optional digest authentication credentials (username/password). If not provided, ACL authentication is assumed.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
