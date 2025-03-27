# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .tts_conversational_model import TtsConversationalModel
import pydantic
from .tts_output_format import TtsOutputFormat
from .tts_optimize_streaming_latency import TtsOptimizeStreamingLatency
from .pydantic_pronunciation_dictionary_version_locator import (
    PydanticPronunciationDictionaryVersionLocator,
)
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class TtsConversationalConfig(UncheckedBaseModel):
    model_id: typing.Optional[TtsConversationalModel] = pydantic.Field(default=None)
    """
    The model to use for TTS
    """

    voice_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The voice ID to use for TTS
    """

    agent_output_audio_format: typing.Optional[TtsOutputFormat] = pydantic.Field(default=None)
    """
    The audio format to use for TTS
    """

    optimize_streaming_latency: typing.Optional[TtsOptimizeStreamingLatency] = pydantic.Field(default=None)
    """
    The optimization for streaming latency
    """

    stability: typing.Optional[float] = pydantic.Field(default=None)
    """
    The stability of generated speech
    """

    speed: typing.Optional[float] = pydantic.Field(default=None)
    """
    The speed of generated speech
    """

    similarity_boost: typing.Optional[float] = pydantic.Field(default=None)
    """
    The similarity boost for generated speech
    """

    pronunciation_dictionary_locators: typing.Optional[typing.List[PydanticPronunciationDictionaryVersionLocator]] = (
        pydantic.Field(default=None)
    )
    """
    The pronunciation dictionary locators
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
