# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import pydantic
import typing_extensions

from ...core.pydantic_utilities import IS_PYDANTIC_V2
from ...core.unchecked_base_model import UncheckedBaseModel, UnionMetadata


class PronunciationDictionaryRule_Alias(UncheckedBaseModel):
    string_to_replace: str
    alias: str
    type: typing.Literal["alias"] = "alias"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class PronunciationDictionaryRule_Phoneme(UncheckedBaseModel):
    string_to_replace: str
    phoneme: str
    alphabet: str
    type: typing.Literal["phoneme"] = "phoneme"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


PronunciationDictionaryRule = typing_extensions.Annotated[
    typing.Union[PronunciationDictionaryRule_Alias, PronunciationDictionaryRule_Phoneme],
    UnionMetadata(discriminant="type"),
]
