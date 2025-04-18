# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from .speech_history_item_response_model_voice_category import (
    SpeechHistoryItemResponseModelVoiceCategory,
)
from .feedback_item import FeedbackItem
from .speech_history_item_response_model_source import (
    SpeechHistoryItemResponseModelSource,
)
from .history_alignments_response_model import HistoryAlignmentsResponseModel
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class SpeechHistoryItemResponse(UncheckedBaseModel):
    history_item_id: str = pydantic.Field()
    """
    The ID of the history item.
    """

    request_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The ID of the request.
    """

    voice_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The ID of the voice used.
    """

    model_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The ID of the model.
    """

    voice_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The name of the voice.
    """

    voice_category: typing.Optional[SpeechHistoryItemResponseModelVoiceCategory] = pydantic.Field(default=None)
    """
    The category of the voice. Either 'premade', 'cloned', 'generated' or 'professional'.
    """

    text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The text used to generate the audio item.
    """

    date_unix: typing.Optional[int] = pydantic.Field(default=None)
    """
    Unix timestamp of when the item was created.
    """

    character_count_change_from: typing.Optional[int] = pydantic.Field(default=None)
    """
    The character count change from.
    """

    character_count_change_to: typing.Optional[int] = pydantic.Field(default=None)
    """
    The character count change to.
    """

    content_type: typing.Optional[str] = pydantic.Field(default=None)
    """
    The content type of the generated item.
    """

    state: typing.Optional[typing.Optional[typing.Any]] = None
    settings: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = pydantic.Field(default=None)
    """
    The settings of the history item.
    """

    feedback: typing.Optional[FeedbackItem] = pydantic.Field(default=None)
    """
    Feedback associated with the generated item. Returns null if no feedback has been provided.
    """

    share_link_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The ID of the share link.
    """

    source: typing.Optional[SpeechHistoryItemResponseModelSource] = pydantic.Field(default=None)
    """
    The source of the history item. Either TTS (text to speech), STS (speech to text), AN (audio native), Projects, Dubbing or PlayAPI.
    """

    alignments: typing.Optional[HistoryAlignmentsResponseModel] = pydantic.Field(default=None)
    """
    The alignments of the history item.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
