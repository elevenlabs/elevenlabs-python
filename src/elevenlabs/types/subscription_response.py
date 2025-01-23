# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
from .subscription_response_model_currency import SubscriptionResponseModelCurrency
from .subscription_status import SubscriptionStatus
from .subscription_response_model_billing_period import SubscriptionResponseModelBillingPeriod
from .subscription_response_model_character_refresh_period import SubscriptionResponseModelCharacterRefreshPeriod
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class SubscriptionResponse(UncheckedBaseModel):
    tier: str
    character_count: int
    character_limit: int
    can_extend_character_limit: bool
    allowed_to_extend_character_limit: bool
    next_character_count_reset_unix: int
    voice_slots_used: int
    voice_limit: int
    max_voice_add_edits: int
    voice_add_edit_counter: int
    professional_voice_limit: int
    can_extend_voice_limit: bool
    can_use_instant_voice_cloning: bool
    can_use_professional_voice_cloning: bool
    currency: SubscriptionResponseModelCurrency
    status: SubscriptionStatus
    billing_period: SubscriptionResponseModelBillingPeriod
    character_refresh_period: SubscriptionResponseModelCharacterRefreshPeriod

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
