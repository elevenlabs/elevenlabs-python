# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.unchecked_base_model import UncheckedBaseModel
from .array_json_schema_property import ArrayJsonSchemaProperty
from .object_json_schema_property import ObjectJsonSchemaProperty
import typing
from .webhook_tool_api_schema_config import WebhookToolApiSchemaConfig
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
import typing_extensions
from ..core.unchecked_base_model import UnionMetadata
from ..core.pydantic_utilities import update_forward_refs


class PromptAgentToolsItem_Webhook(UncheckedBaseModel):
    type: typing.Literal["webhook"] = "webhook"
    name: str
    description: str
    api_schema: WebhookToolApiSchemaConfig

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class PromptAgentToolsItem_Client(UncheckedBaseModel):
    type: typing.Literal["client"] = "client"
    name: str
    description: str
    parameters: typing.Optional[ObjectJsonSchemaProperty] = None
    expects_response: typing.Optional[bool] = None
    response_timeout_secs: typing.Optional[int] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class PromptAgentToolsItem_System(UncheckedBaseModel):
    type: typing.Literal["system"] = "system"
    name: str
    description: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True) 
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


PromptAgentToolsItem = typing_extensions.Annotated[
    typing.Union[PromptAgentToolsItem_Webhook, PromptAgentToolsItem_Client, PromptAgentToolsItem_System],
    UnionMetadata(discriminant="type"),
]
update_forward_refs(ArrayJsonSchemaProperty, PromptAgentToolsItem_Webhook=PromptAgentToolsItem_Webhook)
update_forward_refs(ObjectJsonSchemaProperty, PromptAgentToolsItem_Webhook=PromptAgentToolsItem_Webhook)
update_forward_refs(ArrayJsonSchemaProperty, PromptAgentToolsItem_Client=PromptAgentToolsItem_Client)
update_forward_refs(ObjectJsonSchemaProperty, PromptAgentToolsItem_Client=PromptAgentToolsItem_Client)
update_forward_refs(ArrayJsonSchemaProperty, PromptAgentToolsItem_System=PromptAgentToolsItem_System)
update_forward_refs(ObjectJsonSchemaProperty, PromptAgentToolsItem_System=PromptAgentToolsItem_System)