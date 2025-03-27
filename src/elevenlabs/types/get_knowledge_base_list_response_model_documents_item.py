# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .knowledge_base_document_metadata_response_model import KnowledgeBaseDocumentMetadataResponseModel
from .resource_access_info import ResourceAccessInfo
from .get_knowledge_base_summary_file_response_model_dependent_agents_item import (
    GetKnowledgeBaseSummaryFileResponseModelDependentAgentsItem,
)
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from .get_knowledge_base_summary_url_response_model_dependent_agents_item import (
    GetKnowledgeBaseSummaryUrlResponseModelDependentAgentsItem,
)
import typing_extensions
from ..core.unchecked_base_model import UnionMetadata


class GetKnowledgeBaseListResponseModelDocumentsItem_File(UncheckedBaseModel):
    type: typing.Literal["file"] = "file"
    id: str
    name: str
    metadata: KnowledgeBaseDocumentMetadataResponseModel
    prompt_injectable: bool
    access_info: ResourceAccessInfo
    dependent_agents: typing.List[GetKnowledgeBaseSummaryFileResponseModelDependentAgentsItem]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class GetKnowledgeBaseListResponseModelDocumentsItem_Url(UncheckedBaseModel):
    type: typing.Literal["url"] = "url"
    id: str
    name: str
    metadata: KnowledgeBaseDocumentMetadataResponseModel
    prompt_injectable: bool
    access_info: ResourceAccessInfo
    dependent_agents: typing.List[GetKnowledgeBaseSummaryUrlResponseModelDependentAgentsItem]
    url: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


GetKnowledgeBaseListResponseModelDocumentsItem = typing_extensions.Annotated[
    typing.Union[
        GetKnowledgeBaseListResponseModelDocumentsItem_File, GetKnowledgeBaseListResponseModelDocumentsItem_Url
    ],
    UnionMetadata(discriminant="type"),
]
