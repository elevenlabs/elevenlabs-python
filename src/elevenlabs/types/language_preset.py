# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
from .conversation_config_client_override import ConversationConfigClientOverride
import typing
from .language_preset_translation import LanguagePresetTranslation
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class LanguagePreset(UncheckedBaseModel):
    overrides: ConversationConfigClientOverride
    first_message_translation: typing.Optional[LanguagePresetTranslation] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
