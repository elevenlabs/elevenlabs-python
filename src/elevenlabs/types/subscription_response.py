# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel
from .subscription_response_model_billing_period import SubscriptionResponseModelBillingPeriod
from .subscription_response_model_character_refresh_period import SubscriptionResponseModelCharacterRefreshPeriod
from .subscription_response_model_currency import SubscriptionResponseModelCurrency
from .subscription_status_type import SubscriptionStatusType


class SubscriptionResponse(UncheckedBaseModel):
    tier: str = pydantic.Field()
    """
    The tier of the user's subscription.
    """

    character_count: int = pydantic.Field()
    """
    The number of characters used by the user.
    """

    character_limit: int = pydantic.Field()
    """
    The maximum number of characters allowed in the current billing period.
    """

    max_character_limit_extension: typing.Optional[int] = pydantic.Field(default=None)
    """
    Maximum number of characters that the character limit can be exceeded by. Managed by the workspace admin.
    """

    can_extend_character_limit: bool = pydantic.Field()
    """
    Whether the user can extend their character limit.
    """

    allowed_to_extend_character_limit: bool = pydantic.Field()
    """
    Whether the user is allowed to extend their character limit.
    """

    next_character_count_reset_unix: typing.Optional[int] = pydantic.Field(default=None)
    """
    The Unix timestamp of the next character count reset.
    """

    voice_slots_used: int = pydantic.Field()
    """
    The number of voice slots used by the user.
    """

    professional_voice_slots_used: int = pydantic.Field()
    """
    The number of professional voice slots used by the workspace/user if single seat.
    """

    voice_limit: int = pydantic.Field()
    """
    The maximum number of voice slots allowed for the user.
    """

    max_voice_add_edits: typing.Optional[int] = pydantic.Field(default=None)
    """
    The maximum number of voice add/edits allowed for the user.
    """

    voice_add_edit_counter: int = pydantic.Field()
    """
    The number of voice add/edits used by the user.
    """

    professional_voice_limit: int = pydantic.Field()
    """
    The maximum number of professional voices allowed for the user.
    """

    can_extend_voice_limit: bool = pydantic.Field()
    """
    Whether the user can extend their voice limit.
    """

    can_use_instant_voice_cloning: bool = pydantic.Field()
    """
    Whether the user can use instant voice cloning.
    """

    can_use_professional_voice_cloning: bool = pydantic.Field()
    """
    Whether the user can use professional voice cloning.
    """

    currency: typing.Optional[SubscriptionResponseModelCurrency] = pydantic.Field(default=None)
    """
    The currency of the user's subscription.
    """

    status: SubscriptionStatusType = pydantic.Field()
    """
    The status of the user's subscription.
    """

    billing_period: typing.Optional[SubscriptionResponseModelBillingPeriod] = pydantic.Field(default=None)
    """
    The billing period of the user's subscription.
    """

    character_refresh_period: typing.Optional[SubscriptionResponseModelCharacterRefreshPeriod] = pydantic.Field(
        default=None
    )
    """
    The character refresh period of the user's subscription.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
