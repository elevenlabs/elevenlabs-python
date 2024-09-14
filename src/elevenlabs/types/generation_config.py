# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class GenerationConfig(UncheckedBaseModel):
    chunk_length_schedule: typing.Optional[typing.List[float]] = pydantic.Field(default=None)
    """
    This is an advanced setting that most users shouldn't need to use. It relates to our
    generation schedule explained [here](https://elevenlabs.io/docs/api-reference/websockets#understanding-how-our-websockets-buffer-text).
    
    Determines the minimum amount of text that needs to be sent and present in our
    buffer before audio starts being generated. This is to maximise the amount of context available to
    the model to improve audio quality, whilst balancing latency of the returned audio chunks.
    
    The default value is: [120, 160, 250, 290].
    
    This means that the first chunk of audio will not be generated until you send text that
    totals at least 120 characters long. The next chunk of audio will only be generated once a
    further 160 characters have been sent. The third audio chunk will be generated after the
    next 250 characters. Then the fourth, and beyond, will be generated in sets of at least 290 characters.
    
    Customize this array to suit your needs. If you want to generate audio more frequently
    to optimise latency, you can reduce the values in the array. Note that setting the values
    too low may result in lower quality audio. Please test and adjust as needed.
    
    Each item should be in the range 50-500.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
