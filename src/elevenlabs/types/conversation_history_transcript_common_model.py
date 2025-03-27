# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
from .conversation_history_transcript_common_model_role import ConversationHistoryTranscriptCommonModelRole
import typing
from .conversation_history_transcript_tool_call_common_model import ConversationHistoryTranscriptToolCallCommonModel
from .conversation_history_transcript_tool_result_common_model import ConversationHistoryTranscriptToolResultCommonModel
from .user_feedback import UserFeedback
from .conversation_turn_metrics import ConversationTurnMetrics
from .rag_retrieval_info import RagRetrievalInfo
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ConversationHistoryTranscriptCommonModel(UncheckedBaseModel):
    role: ConversationHistoryTranscriptCommonModelRole
    message: typing.Optional[str] = None
    tool_calls: typing.Optional[typing.List[ConversationHistoryTranscriptToolCallCommonModel]] = None
    tool_results: typing.Optional[typing.List[ConversationHistoryTranscriptToolResultCommonModel]] = None
    feedback: typing.Optional[UserFeedback] = None
    llm_override: typing.Optional[str] = None
    time_in_call_secs: int
    conversation_turn_metrics: typing.Optional[ConversationTurnMetrics] = None
    rag_retrieval_info: typing.Optional[RagRetrievalInfo] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
