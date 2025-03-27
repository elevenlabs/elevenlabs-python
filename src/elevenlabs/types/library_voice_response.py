# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
from .library_voice_response_model_category import LibraryVoiceResponseModelCategory
import typing
import typing_extensions
from ..core.serialization import FieldMetadata
from .verified_voice_language_response_model import VerifiedVoiceLanguageResponseModel
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class LibraryVoiceResponse(UncheckedBaseModel):
    public_owner_id: str = pydantic.Field()
    """
    The public owner id of the voice.
    """

    voice_id: str = pydantic.Field()
    """
    The id of the voice.
    """

    date_unix: int = pydantic.Field()
    """
    The date the voice was added to the library in Unix time.
    """

    name: str = pydantic.Field()
    """
    The name of the voice.
    """

    accent: str = pydantic.Field()
    """
    The accent of the voice.
    """

    gender: str = pydantic.Field()
    """
    The gender of the voice.
    """

    age: str = pydantic.Field()
    """
    The age of the voice.
    """

    descriptive: str = pydantic.Field()
    """
    The descriptive of the voice.
    """

    use_case: str = pydantic.Field()
    """
    The use case of the voice.
    """

    category: LibraryVoiceResponseModelCategory = pydantic.Field()
    """
    The category of the voice.
    """

    language: typing.Optional[str] = pydantic.Field(default=None)
    """
    The language of the voice.
    """

    locale: typing.Optional[str] = pydantic.Field(default=None)
    """
    The locale of the voice.
    """

    description: typing.Optional[str] = pydantic.Field(default=None)
    """
    The description of the voice.
    """

    preview_url: typing.Optional[str] = pydantic.Field(default=None)
    """
    The preview URL of the voice.
    """

    usage_character_count_1_y: typing_extensions.Annotated[int, FieldMetadata(alias="usage_character_count_1y")] = (
        pydantic.Field()
    )
    """
    The usage character count of the voice in the last year.
    """

    usage_character_count_7_d: typing_extensions.Annotated[int, FieldMetadata(alias="usage_character_count_7d")] = (
        pydantic.Field()
    )
    """
    The usage character count of the voice in the last 7 days.
    """

    play_api_usage_character_count_1_y: typing_extensions.Annotated[
        int, FieldMetadata(alias="play_api_usage_character_count_1y")
    ] = pydantic.Field()
    """
    The play API usage character count of the voice in the last year.
    """

    cloned_by_count: int = pydantic.Field()
    """
    The number of times the voice has been cloned.
    """

    rate: typing.Optional[float] = pydantic.Field(default=None)
    """
    The rate of the voice.
    """

    free_users_allowed: bool = pydantic.Field()
    """
    Whether free users are allowed to use the voice.
    """

    live_moderation_enabled: bool = pydantic.Field()
    """
    Whether live moderation is enabled for the voice.
    """

    featured: bool = pydantic.Field()
    """
    Whether the voice is featured.
    """

    verified_languages: typing.Optional[typing.List[VerifiedVoiceLanguageResponseModel]] = pydantic.Field(default=None)
    """
    The verified languages of the voice.
    """

    notice_period: typing.Optional[int] = pydantic.Field(default=None)
    """
    The notice period of the voice.
    """

    instagram_username: typing.Optional[str] = pydantic.Field(default=None)
    """
    The Instagram username of the voice.
    """

    twitter_username: typing.Optional[str] = pydantic.Field(default=None)
    """
    The Twitter username of the voice.
    """

    youtube_username: typing.Optional[str] = pydantic.Field(default=None)
    """
    The YouTube username of the voice.
    """

    tiktok_username: typing.Optional[str] = pydantic.Field(default=None)
    """
    The TikTok username of the voice.
    """

    image_url: typing.Optional[str] = pydantic.Field(default=None)
    """
    The image URL of the voice.
    """

    is_added_by_user: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether the voice was added by the user.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
