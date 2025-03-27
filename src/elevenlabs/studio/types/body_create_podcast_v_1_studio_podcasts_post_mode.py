# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ...core.unchecked_base_model import UncheckedBaseModel
import typing
from ...types.podcast_conversation_mode_data import PodcastConversationModeData
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from ...types.podcast_bulletin_mode_data import PodcastBulletinModeData
import typing_extensions
from ...core.unchecked_base_model import UnionMetadata


class BodyCreatePodcastV1StudioPodcastsPostMode_Conversation(UncheckedBaseModel):
    """
    The type of podcast to generate. Can be 'conversation', an interaction between two voices, or 'bulletin', a monologue.
    """

    type: typing.Literal["conversation"] = "conversation"
    conversation: PodcastConversationModeData

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class BodyCreatePodcastV1StudioPodcastsPostMode_Bulletin(UncheckedBaseModel):
    """
    The type of podcast to generate. Can be 'conversation', an interaction between two voices, or 'bulletin', a monologue.
    """

    type: typing.Literal["bulletin"] = "bulletin"
    bulletin: PodcastBulletinModeData

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


BodyCreatePodcastV1StudioPodcastsPostMode = typing_extensions.Annotated[
    typing.Union[
        BodyCreatePodcastV1StudioPodcastsPostMode_Conversation,
        BodyCreatePodcastV1StudioPodcastsPostMode_Bulletin,
    ],
    UnionMetadata(discriminant="type"),
]
