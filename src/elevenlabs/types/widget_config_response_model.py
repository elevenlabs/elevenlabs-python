# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .embed_variant import EmbedVariant
import pydantic
from .widget_expandable import WidgetExpandable
from .widget_config_response_model_avatar import WidgetConfigResponseModelAvatar
from .widget_feedback_mode import WidgetFeedbackMode
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class WidgetConfigResponseModel(UncheckedBaseModel):
    variant: typing.Optional[EmbedVariant] = pydantic.Field(default=None)
    """
    The variant of the widget
    """

    expandable: typing.Optional[WidgetExpandable] = pydantic.Field(default=None)
    """
    Whether the widget is expandable
    """

    avatar: typing.Optional[WidgetConfigResponseModelAvatar] = pydantic.Field(default=None)
    """
    The avatar of the widget
    """

    feedback_mode: typing.Optional[WidgetFeedbackMode] = pydantic.Field(default=None)
    """
    The feedback mode of the widget
    """

    bg_color: typing.Optional[str] = pydantic.Field(default=None)
    """
    The background color of the widget
    """

    text_color: typing.Optional[str] = pydantic.Field(default=None)
    """
    The text color of the widget
    """

    btn_color: typing.Optional[str] = pydantic.Field(default=None)
    """
    The button color of the widget
    """

    btn_text_color: typing.Optional[str] = pydantic.Field(default=None)
    """
    The button text color of the widget
    """

    border_color: typing.Optional[str] = pydantic.Field(default=None)
    """
    The border color of the widget
    """

    focus_color: typing.Optional[str] = pydantic.Field(default=None)
    """
    The focus color of the widget
    """

    border_radius: typing.Optional[int] = pydantic.Field(default=None)
    """
    The border radius of the widget
    """

    btn_radius: typing.Optional[int] = pydantic.Field(default=None)
    """
    The button radius of the widget
    """

    action_text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The action text of the widget
    """

    start_call_text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The start call text of the widget
    """

    end_call_text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The end call text of the widget
    """

    expand_text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The expand text of the widget
    """

    listening_text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The text to display when the agent is listening
    """

    speaking_text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The text to display when the agent is speaking
    """

    shareable_page_text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The text to display when sharing
    """

    shareable_page_show_terms: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether to show terms and conditions on the shareable page
    """

    terms_text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The text to display for terms and conditions
    """

    terms_html: typing.Optional[str] = pydantic.Field(default=None)
    """
    The HTML to display for terms and conditions
    """

    terms_key: typing.Optional[str] = pydantic.Field(default=None)
    """
    The key to display for terms and conditions
    """

    show_avatar_when_collapsed: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether to show the avatar when the widget is collapsed
    """

    disable_banner: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether to disable the banner
    """

    mic_muting_enabled: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether to enable mic muting
    """

    language: str
    supported_language_overrides: typing.Optional[typing.List[str]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
