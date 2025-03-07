# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class AudioNativeProjectSettingsResponseModel(UncheckedBaseModel):
    title: str = pydantic.Field()
    """
    The title of the project.
    """

    image: str = pydantic.Field()
    """
    The image of the project.
    """

    author: str = pydantic.Field()
    """
    The author of the project.
    """

    small: bool = pydantic.Field()
    """
    Whether the project is small.
    """

    text_color: str = pydantic.Field()
    """
    The text color of the project.
    """

    background_color: str = pydantic.Field()
    """
    The background color of the project.
    """

    sessionization: int = pydantic.Field()
    """
    The sessionization of the project. Specifies for how many minutes to persist the session across page reloads.
    """

    audio_path: typing.Optional[str] = pydantic.Field(default=None)
    """
    The path of the audio file.
    """

    audio_url: typing.Optional[str] = pydantic.Field(default=None)
    """
    The URL of the audio file.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
