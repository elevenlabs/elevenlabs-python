# This file was auto-generated by Fern from our API Definition.

from .types import (
    Accent,
    AddAgentSecretResponseModel,
    AddChapterResponseModel,
    AddKnowledgeBaseResponseModel,
    AddProjectResponseModel,
    AddPronunciationDictionaryResponseModel,
    AddPronunciationDictionaryRulesResponseModel,
    AddSharingVoiceRequest,
    AddVoiceIvcResponseModel,
    AddVoiceResponseModel,
    AddWorkspaceGroupMemberResponseModel,
    AddWorkspaceInviteResponseModel,
    Age,
    AgentBan,
    AgentCallLimits,
    AgentConfigApiModel,
    AgentConfigOverride,
    AgentConfigOverrideConfig,
    AgentMetadataResponseModel,
    AgentPlatformSettingsRequestModel,
    AgentPlatformSettingsResponseModel,
    AgentSummaryResponseModel,
    AllowlistItem,
    ArrayJsonSchemaProperty,
    ArrayJsonSchemaPropertyItems,
    AsrConversationalConfig,
    AsrInputFormat,
    AsrProvider,
    AsrQuality,
    AudioNativeCreateProjectResponseModel,
    AudioNativeEditContentResponseModel,
    AudioNativeProjectSettingsResponseModel,
    AudioWithTimestampsResponseModel,
    AuthSettings,
    AuthorizationMethod,
    BanReasonType,
    BodyAddToKnowledgeBaseV1ConvaiAddToKnowledgeBasePost,
    BodyAddToKnowledgeBaseV1ConvaiAgentsAgentIdAddToKnowledgeBasePost,
    BreakdownTypes,
    ChapterContentBlockExtendableNodeResponseModel,
    ChapterContentBlockInputModel,
    ChapterContentBlockResponseModel,
    ChapterContentBlockResponseModelNodesItem,
    ChapterContentBlockResponseModelNodesItem_Other,
    ChapterContentBlockResponseModelNodesItem_TtsNode,
    ChapterContentBlockTtsNodeResponseModel,
    ChapterContentInputModel,
    ChapterContentParagraphTtsNodeInputModel,
    ChapterContentResponseModel,
    ChapterResponse,
    ChapterSnapshotExtendedResponseModel,
    ChapterSnapshotResponse,
    ChapterSnapshotsResponse,
    ChapterState,
    ChapterStatisticsResponse,
    ChapterWithContentResponseModel,
    ChapterWithContentResponseModelState,
    CharacterAlignmentModel,
    CharacterAlignmentResponseModel,
    ClientEvent,
    ClientToolConfig,
    ConvAiSecretLocator,
    ConvAiStoredSecretDependencies,
    ConvAiStoredSecretDependenciesAgentToolsItem,
    ConvAiStoredSecretDependenciesAgentToolsItem_Available,
    ConvAiStoredSecretDependenciesAgentToolsItem_Unknown,
    ConvAiStoredSecretDependenciesToolsItem,
    ConvAiStoredSecretDependenciesToolsItem_Available,
    ConvAiStoredSecretDependenciesToolsItem_Unknown,
    ConvAiWebhooks,
    ConvAiWorkspaceStoredSecretConfig,
    ConversationChargingCommonModel,
    ConversationConfig,
    ConversationConfigClientOverride,
    ConversationConfigClientOverrideConfig,
    ConversationDeletionSettings,
    ConversationHistoryAnalysisCommonModel,
    ConversationHistoryEvaluationCriteriaResultCommonModel,
    ConversationHistoryFeedbackCommonModel,
    ConversationHistoryMetadataCommonModel,
    ConversationHistoryTranscriptCommonModel,
    ConversationHistoryTranscriptCommonModelRole,
    ConversationHistoryTranscriptToolCallCommonModel,
    ConversationHistoryTranscriptToolResultCommonModel,
    ConversationInitiationClientData,
    ConversationInitiationClientDataConfig,
    ConversationInitiationClientDataDynamicVariablesValue,
    ConversationInitiationClientDataWebhook,
    ConversationInitiationClientDataWebhookRequestHeadersValue,
    ConversationSignedUrlResponseModel,
    ConversationSummaryResponseModel,
    ConversationSummaryResponseModelStatus,
    ConversationTokenDbModel,
    ConversationTokenPurpose,
    ConversationalConfigApiModel,
    ConvertChapterResponseModel,
    ConvertProjectResponseModel,
    CreateAgentResponseModel,
    CreateAudioNativeProjectRequest,
    CreatePhoneNumberResponseModel,
    CreatePronunciationDictionaryResponseModel,
    Currency,
    CustomLlm,
    DataCollectionResultCommonModel,
    DeleteChapterResponseModel,
    DeleteDubbingResponseModel,
    DeleteProjectResponseModel,
    DeleteSampleResponseModel,
    DeleteVoiceResponseModel,
    DeleteWorkspaceGroupMemberResponseModel,
    DeleteWorkspaceInviteResponseModel,
    DependentAvailableAgentIdentifier,
    DependentAvailableAgentIdentifierAccessLevel,
    DependentAvailableAgentToolIdentifier,
    DependentAvailableAgentToolIdentifierAccessLevel,
    DependentAvailableToolIdentifier,
    DependentAvailableToolIdentifierAccessLevel,
    DependentPhoneNumberIdentifier,
    DependentUnknownAgentIdentifier,
    DependentUnknownAgentToolIdentifier,
    DependentUnknownToolIdentifier,
    DoDubbingResponse,
    DocumentUsageModeEnum,
    DubbedSegment,
    DubbingMediaMetadata,
    DubbingMediaReference,
    DubbingMetadataResponse,
    DubbingResource,
    DynamicVariablesConfig,
    DynamicVariablesConfigDynamicVariablePlaceholdersValue,
    EditChapterResponseModel,
    EditProjectResponseModel,
    EditVoiceResponseModel,
    EditVoiceSettingsResponseModel,
    EmbedVariant,
    EmbeddingModelEnum,
    EvaluationSettings,
    EvaluationSuccessResult,
    ExtendedSubscriptionResponseModelBillingPeriod,
    ExtendedSubscriptionResponseModelCharacterRefreshPeriod,
    ExtendedSubscriptionResponseModelCurrency,
    FeedbackItem,
    FineTuningResponse,
    FineTuningResponseModelStateValue,
    Gender,
    GetAgentEmbedResponseModel,
    GetAgentLinkResponseModel,
    GetAgentResponseModel,
    GetAgentsPageResponseModel,
    GetAudioNativeProjectSettingsResponseModel,
    GetChaptersResponse,
    GetConvAiSettingsResponseModel,
    GetConversationResponseModel,
    GetConversationResponseModelStatus,
    GetConversationsPageResponseModel,
    GetKnowledgeBaseDependentAgentsResponseModel,
    GetKnowledgeBaseDependentAgentsResponseModelAgentsItem,
    GetKnowledgeBaseDependentAgentsResponseModelAgentsItem_Available,
    GetKnowledgeBaseDependentAgentsResponseModelAgentsItem_Unknown,
    GetKnowledgeBaseListResponseModel,
    GetKnowledgeBaseResponseModel,
    GetKnowledgeBaseResponseModelAccessLevel,
    GetKnowledgeBaseResponseModelType,
    GetKnowledgeBaseSummaryResponseModel,
    GetKnowledgeBaseSummaryResponseModelAccessLevel,
    GetKnowledgeBaseSummaryResponseModelDependentAgentsItem,
    GetKnowledgeBaseSummaryResponseModelDependentAgentsItem_Available,
    GetKnowledgeBaseSummaryResponseModelDependentAgentsItem_Unknown,
    GetKnowledgeBaseSummaryResponseModelType,
    GetLibraryVoicesResponse,
    GetPhoneNumberResponseModel,
    GetProjectsResponse,
    GetPronunciationDictionariesMetadataResponseModel,
    GetPronunciationDictionaryMetadataResponse,
    GetSpeechHistoryResponse,
    GetVoicesResponse,
    GetWorkspaceSecretsResponseModel,
    HistoryAlignmentResponseModel,
    HistoryAlignmentsResponseModel,
    HistoryItem,
    HttpValidationError,
    ImageAvatar,
    Invoice,
    KnowledgeBaseDocumentMetadataResponseModel,
    KnowledgeBaseLocator,
    KnowledgeBaseLocatorType,
    LanguageAddedResponse,
    LanguagePreset,
    LanguagePresetTranslation,
    LanguageResponse,
    LibraryVoiceResponse,
    LibraryVoiceResponseModelCategory,
    LiteralJsonSchemaProperty,
    LiteralJsonSchemaPropertyType,
    Llm,
    ManualVerificationFileResponse,
    ManualVerificationResponse,
    Model,
    ModelRatesResponseModel,
    ModelResponseModelConcurrencyGroup,
    ModerationStatusResponseModel,
    ModerationStatusResponseModelSafetyStatus,
    ModerationStatusResponseModelWarningStatus,
    ObjectJsonSchemaProperty,
    ObjectJsonSchemaPropertyPropertiesValue,
    OrbAvatar,
    OutputFormat,
    PhoneNumberAgentInfo,
    PodcastBulletinMode,
    PodcastBulletinModeData,
    PodcastConversationMode,
    PodcastConversationModeData,
    PodcastProjectResponseModel,
    PodcastTextSource,
    PodcastUrlSource,
    PostAgentAvatarResponseModel,
    PostWorkspaceSecretResponseModel,
    PrivacyConfig,
    ProfilePageResponseModel,
    ProjectCreationMetaResponseModel,
    ProjectCreationMetaResponseModelStatus,
    ProjectCreationMetaResponseModelType,
    ProjectExtendedResponseModel,
    ProjectExtendedResponseModelAccessLevel,
    ProjectExtendedResponseModelApplyTextNormalization,
    ProjectExtendedResponseModelFiction,
    ProjectExtendedResponseModelQualityPreset,
    ProjectExtendedResponseModelSourceType,
    ProjectExtendedResponseModelTargetAudience,
    ProjectResponse,
    ProjectResponseModelAccessLevel,
    ProjectResponseModelFiction,
    ProjectResponseModelSourceType,
    ProjectResponseModelTargetAudience,
    ProjectSnapshotExtendedResponseModel,
    ProjectSnapshotResponse,
    ProjectSnapshotUploadResponseModel,
    ProjectSnapshotUploadResponseModelStatus,
    ProjectSnapshotsResponse,
    ProjectState,
    PromptAgent,
    PromptAgentOverride,
    PromptAgentOverrideConfig,
    PromptAgentToolsItem,
    PromptAgentToolsItem_Client,
    PromptAgentToolsItem_System,
    PromptAgentToolsItem_Webhook,
    PromptEvaluationCriteria,
    PronunciationDictionaryAliasRuleRequestModel,
    PronunciationDictionaryPhonemeRuleRequestModel,
    PronunciationDictionaryVersionLocator,
    PronunciationDictionaryVersionResponseModel,
    PydanticPronunciationDictionaryVersionLocator,
    QueryParamsJsonSchema,
    RagConfig,
    RagIndexResponseModel,
    RagIndexStatus,
    ReaderResourceResponseModel,
    ReaderResourceResponseModelResourceType,
    RecordingResponse,
    RemovePronunciationDictionaryRulesResponseModel,
    ResourceAccessInfo,
    ResourceAccessInfoRole,
    ReviewStatus,
    SafetyCommonModel,
    SafetyEvaluation,
    SafetyResponseModel,
    SafetyRule,
    SecretDependencyType,
    SegmentCreateResponse,
    SegmentDeleteResponse,
    SegmentDubResponse,
    SegmentTranscriptionResponse,
    SegmentTranslationResponse,
    SegmentUpdateResponse,
    SpeakerSegment,
    SpeakerTrack,
    SpeechHistoryItemResponse,
    SpeechHistoryItemResponseModelSource,
    SpeechHistoryItemResponseModelVoiceCategory,
    SpeechToTextCharacterResponseModel,
    SpeechToTextChunkResponseModel,
    SpeechToTextWordResponseModel,
    SpeechToTextWordResponseModelType,
    StreamingAudioChunkWithTimestampsResponseModel,
    Subscription,
    SubscriptionResponse,
    SubscriptionResponseModelBillingPeriod,
    SubscriptionResponseModelCharacterRefreshPeriod,
    SubscriptionResponseModelCurrency,
    SubscriptionStatus,
    SubscriptionUsageResponseModel,
    SystemToolConfig,
    TelephonyProvider,
    TextToSpeechAsStreamRequest,
    TtsConversationalConfig,
    TtsConversationalConfigOverride,
    TtsConversationalConfigOverrideConfig,
    TtsConversationalModel,
    TtsOptimizeStreamingLatency,
    TtsOutputFormat,
    TurnConfig,
    TurnMode,
    UpdateWorkspaceMemberResponseModel,
    UrlAvatar,
    UsageCharactersResponseModel,
    User,
    UserFeedback,
    UserFeedbackScore,
    ValidationError,
    ValidationErrorLocItem,
    VerificationAttemptResponse,
    VerifiedVoiceLanguageResponseModel,
    Voice,
    VoiceGenerationParameterOptionResponse,
    VoiceGenerationParameterResponse,
    VoicePreviewResponseModel,
    VoicePreviewsResponseModel,
    VoiceResponseModelCategory,
    VoiceResponseModelSafetyControl,
    VoiceSample,
    VoiceSettings,
    VoiceSharingModerationCheckResponseModel,
    VoiceSharingResponse,
    VoiceSharingResponseModelCategory,
    VoiceSharingState,
    VoiceVerificationResponse,
    WebhookToolApiSchemaConfig,
    WebhookToolApiSchemaConfigMethod,
    WebhookToolApiSchemaConfigRequestHeadersValue,
    WebhookToolConfig,
    WidgetConfig,
    WidgetConfigAvatar,
    WidgetConfigAvatar_Image,
    WidgetConfigAvatar_Orb,
    WidgetConfigAvatar_Url,
    WidgetConfigResponseModel,
    WidgetConfigResponseModelAvatar,
    WidgetConfigResponseModelAvatar_Image,
    WidgetConfigResponseModelAvatar_Orb,
    WidgetConfigResponseModelAvatar_Url,
    WidgetExpandable,
    WidgetFeedbackMode,
    WorkspaceGroupByNameResponseModel,
)
from .errors import ForbiddenError, NotFoundError, TooEarlyError, UnprocessableEntityError
from . import (
    audio_isolation,
    audio_native,
    conversational_ai,
    dubbing,
    history,
    models,
    projects,
    pronunciation_dictionary,
    samples,
    speech_to_speech,
    speech_to_text,
    studio,
    text_to_sound_effects,
    text_to_speech,
    text_to_voice,
    usage,
    user,
    voice_generation,
    voices,
    workspace,
)
from .client import AsyncElevenLabs, ElevenLabs
from .dubbing import DubbingGetTranscriptForDubRequestFormatType
from .environment import ElevenLabsEnvironment
from .history import HistoryGetAllRequestSource
from .play import play, save, stream
from .projects import (
    AddProjectV1ProjectsAddPostRequestApplyTextNormalization,
    AddProjectV1ProjectsAddPostRequestFiction,
    AddProjectV1ProjectsAddPostRequestTargetAudience,
    BodyCreatePodcastV1ProjectsPodcastCreatePostDurationScale,
    BodyCreatePodcastV1ProjectsPodcastCreatePostMode,
    BodyCreatePodcastV1ProjectsPodcastCreatePostMode_Bulletin,
    BodyCreatePodcastV1ProjectsPodcastCreatePostMode_Conversation,
    BodyCreatePodcastV1ProjectsPodcastCreatePostQualityPreset,
    BodyCreatePodcastV1ProjectsPodcastCreatePostSource,
    BodyCreatePodcastV1ProjectsPodcastCreatePostSourceItem,
    BodyCreatePodcastV1ProjectsPodcastCreatePostSourceItem_Text,
    BodyCreatePodcastV1ProjectsPodcastCreatePostSourceItem_Url,
)
from .pronunciation_dictionary import (
    PronunciationDictionaryAddFromFileRequestWorkspaceAccess,
    PronunciationDictionaryRule,
    PronunciationDictionaryRule_Alias,
    PronunciationDictionaryRule_Phoneme,
)
from .speech_to_text import SpeechToTextConvertRequestTimestampsGranularity
from .studio import (
    BodyCreatePodcastV1StudioPodcastsPostDurationScale,
    BodyCreatePodcastV1StudioPodcastsPostMode,
    BodyCreatePodcastV1StudioPodcastsPostMode_Bulletin,
    BodyCreatePodcastV1StudioPodcastsPostMode_Conversation,
    BodyCreatePodcastV1StudioPodcastsPostQualityPreset,
    BodyCreatePodcastV1StudioPodcastsPostSource,
    BodyCreatePodcastV1StudioPodcastsPostSourceItem,
    BodyCreatePodcastV1StudioPodcastsPostSourceItem_Text,
    BodyCreatePodcastV1StudioPodcastsPostSourceItem_Url,
)
from .text_to_sound_effects import TextToSoundEffectsConvertRequestOutputFormat
from .text_to_speech import (
    BodyTextToSpeechStreamingV1TextToSpeechVoiceIdStreamPostApplyTextNormalization,
    BodyTextToSpeechStreamingWithTimestampsV1TextToSpeechVoiceIdStreamWithTimestampsPostApplyTextNormalization,
    BodyTextToSpeechV1TextToSpeechVoiceIdPostApplyTextNormalization,
    BodyTextToSpeechWithTimestampsV1TextToSpeechVoiceIdWithTimestampsPostApplyTextNormalization,
)
from .text_to_voice import TextToVoiceCreatePreviewsRequestOutputFormat
from .version import __version__
from .voices import VoicesGetSharedRequestCategory
from .workspace import BodyUpdateMemberV1WorkspaceMembersPostWorkspaceRole

__all__ = [
    "Accent",
    "AddAgentSecretResponseModel",
    "AddChapterResponseModel",
    "AddKnowledgeBaseResponseModel",
    "AddProjectResponseModel",
    "AddProjectV1ProjectsAddPostRequestApplyTextNormalization",
    "AddProjectV1ProjectsAddPostRequestFiction",
    "AddProjectV1ProjectsAddPostRequestTargetAudience",
    "AddPronunciationDictionaryResponseModel",
    "AddPronunciationDictionaryRulesResponseModel",
    "AddSharingVoiceRequest",
    "AddVoiceIvcResponseModel",
    "AddVoiceResponseModel",
    "AddWorkspaceGroupMemberResponseModel",
    "AddWorkspaceInviteResponseModel",
    "Age",
    "AgentBan",
    "AgentCallLimits",
    "AgentConfigApiModel",
    "AgentConfigOverride",
    "AgentConfigOverrideConfig",
    "AgentMetadataResponseModel",
    "AgentPlatformSettingsRequestModel",
    "AgentPlatformSettingsResponseModel",
    "AgentSummaryResponseModel",
    "AllowlistItem",
    "ArrayJsonSchemaProperty",
    "ArrayJsonSchemaPropertyItems",
    "AsrConversationalConfig",
    "AsrInputFormat",
    "AsrProvider",
    "AsrQuality",
    "AsyncElevenLabs",
    "AudioNativeCreateProjectResponseModel",
    "AudioNativeEditContentResponseModel",
    "AudioNativeProjectSettingsResponseModel",
    "AudioWithTimestampsResponseModel",
    "AuthSettings",
    "AuthorizationMethod",
    "BanReasonType",
    "BodyAddToKnowledgeBaseV1ConvaiAddToKnowledgeBasePost",
    "BodyAddToKnowledgeBaseV1ConvaiAgentsAgentIdAddToKnowledgeBasePost",
    "BodyCreatePodcastV1ProjectsPodcastCreatePostDurationScale",
    "BodyCreatePodcastV1ProjectsPodcastCreatePostMode",
    "BodyCreatePodcastV1ProjectsPodcastCreatePostMode_Bulletin",
    "BodyCreatePodcastV1ProjectsPodcastCreatePostMode_Conversation",
    "BodyCreatePodcastV1ProjectsPodcastCreatePostQualityPreset",
    "BodyCreatePodcastV1ProjectsPodcastCreatePostSource",
    "BodyCreatePodcastV1ProjectsPodcastCreatePostSourceItem",
    "BodyCreatePodcastV1ProjectsPodcastCreatePostSourceItem_Text",
    "BodyCreatePodcastV1ProjectsPodcastCreatePostSourceItem_Url",
    "BodyCreatePodcastV1StudioPodcastsPostDurationScale",
    "BodyCreatePodcastV1StudioPodcastsPostMode",
    "BodyCreatePodcastV1StudioPodcastsPostMode_Bulletin",
    "BodyCreatePodcastV1StudioPodcastsPostMode_Conversation",
    "BodyCreatePodcastV1StudioPodcastsPostQualityPreset",
    "BodyCreatePodcastV1StudioPodcastsPostSource",
    "BodyCreatePodcastV1StudioPodcastsPostSourceItem",
    "BodyCreatePodcastV1StudioPodcastsPostSourceItem_Text",
    "BodyCreatePodcastV1StudioPodcastsPostSourceItem_Url",
    "BodyTextToSpeechStreamingV1TextToSpeechVoiceIdStreamPostApplyTextNormalization",
    "BodyTextToSpeechStreamingWithTimestampsV1TextToSpeechVoiceIdStreamWithTimestampsPostApplyTextNormalization",
    "BodyTextToSpeechV1TextToSpeechVoiceIdPostApplyTextNormalization",
    "BodyTextToSpeechWithTimestampsV1TextToSpeechVoiceIdWithTimestampsPostApplyTextNormalization",
    "BodyUpdateMemberV1WorkspaceMembersPostWorkspaceRole",
    "BreakdownTypes",
    "ChapterContentBlockExtendableNodeResponseModel",
    "ChapterContentBlockInputModel",
    "ChapterContentBlockResponseModel",
    "ChapterContentBlockResponseModelNodesItem",
    "ChapterContentBlockResponseModelNodesItem_Other",
    "ChapterContentBlockResponseModelNodesItem_TtsNode",
    "ChapterContentBlockTtsNodeResponseModel",
    "ChapterContentInputModel",
    "ChapterContentParagraphTtsNodeInputModel",
    "ChapterContentResponseModel",
    "ChapterResponse",
    "ChapterSnapshotExtendedResponseModel",
    "ChapterSnapshotResponse",
    "ChapterSnapshotsResponse",
    "ChapterState",
    "ChapterStatisticsResponse",
    "ChapterWithContentResponseModel",
    "ChapterWithContentResponseModelState",
    "CharacterAlignmentModel",
    "CharacterAlignmentResponseModel",
    "ClientEvent",
    "ClientToolConfig",
    "ConvAiSecretLocator",
    "ConvAiStoredSecretDependencies",
    "ConvAiStoredSecretDependenciesAgentToolsItem",
    "ConvAiStoredSecretDependenciesAgentToolsItem_Available",
    "ConvAiStoredSecretDependenciesAgentToolsItem_Unknown",
    "ConvAiStoredSecretDependenciesToolsItem",
    "ConvAiStoredSecretDependenciesToolsItem_Available",
    "ConvAiStoredSecretDependenciesToolsItem_Unknown",
    "ConvAiWebhooks",
    "ConvAiWorkspaceStoredSecretConfig",
    "ConversationChargingCommonModel",
    "ConversationConfig",
    "ConversationConfigClientOverride",
    "ConversationConfigClientOverrideConfig",
    "ConversationDeletionSettings",
    "ConversationHistoryAnalysisCommonModel",
    "ConversationHistoryEvaluationCriteriaResultCommonModel",
    "ConversationHistoryFeedbackCommonModel",
    "ConversationHistoryMetadataCommonModel",
    "ConversationHistoryTranscriptCommonModel",
    "ConversationHistoryTranscriptCommonModelRole",
    "ConversationHistoryTranscriptToolCallCommonModel",
    "ConversationHistoryTranscriptToolResultCommonModel",
    "ConversationInitiationClientData",
    "ConversationInitiationClientDataConfig",
    "ConversationInitiationClientDataDynamicVariablesValue",
    "ConversationInitiationClientDataWebhook",
    "ConversationInitiationClientDataWebhookRequestHeadersValue",
    "ConversationSignedUrlResponseModel",
    "ConversationSummaryResponseModel",
    "ConversationSummaryResponseModelStatus",
    "ConversationTokenDbModel",
    "ConversationTokenPurpose",
    "ConversationalConfigApiModel",
    "ConvertChapterResponseModel",
    "ConvertProjectResponseModel",
    "CreateAgentResponseModel",
    "CreateAudioNativeProjectRequest",
    "CreatePhoneNumberResponseModel",
    "CreatePronunciationDictionaryResponseModel",
    "Currency",
    "CustomLlm",
    "DataCollectionResultCommonModel",
    "DeleteChapterResponseModel",
    "DeleteDubbingResponseModel",
    "DeleteProjectResponseModel",
    "DeleteSampleResponseModel",
    "DeleteVoiceResponseModel",
    "DeleteWorkspaceGroupMemberResponseModel",
    "DeleteWorkspaceInviteResponseModel",
    "DependentAvailableAgentIdentifier",
    "DependentAvailableAgentIdentifierAccessLevel",
    "DependentAvailableAgentToolIdentifier",
    "DependentAvailableAgentToolIdentifierAccessLevel",
    "DependentAvailableToolIdentifier",
    "DependentAvailableToolIdentifierAccessLevel",
    "DependentPhoneNumberIdentifier",
    "DependentUnknownAgentIdentifier",
    "DependentUnknownAgentToolIdentifier",
    "DependentUnknownToolIdentifier",
    "DoDubbingResponse",
    "DocumentUsageModeEnum",
    "DubbedSegment",
    "DubbingGetTranscriptForDubRequestFormatType",
    "DubbingMediaMetadata",
    "DubbingMediaReference",
    "DubbingMetadataResponse",
    "DubbingResource",
    "DynamicVariablesConfig",
    "DynamicVariablesConfigDynamicVariablePlaceholdersValue",
    "EditChapterResponseModel",
    "EditProjectResponseModel",
    "EditVoiceResponseModel",
    "EditVoiceSettingsResponseModel",
    "ElevenLabs",
    "ElevenLabsEnvironment",
    "EmbedVariant",
    "EmbeddingModelEnum",
    "EvaluationSettings",
    "EvaluationSuccessResult",
    "ExtendedSubscriptionResponseModelBillingPeriod",
    "ExtendedSubscriptionResponseModelCharacterRefreshPeriod",
    "ExtendedSubscriptionResponseModelCurrency",
    "FeedbackItem",
    "FineTuningResponse",
    "FineTuningResponseModelStateValue",
    "ForbiddenError",
    "Gender",
    "GetAgentEmbedResponseModel",
    "GetAgentLinkResponseModel",
    "GetAgentResponseModel",
    "GetAgentsPageResponseModel",
    "GetAudioNativeProjectSettingsResponseModel",
    "GetChaptersResponse",
    "GetConvAiSettingsResponseModel",
    "GetConversationResponseModel",
    "GetConversationResponseModelStatus",
    "GetConversationsPageResponseModel",
    "GetKnowledgeBaseDependentAgentsResponseModel",
    "GetKnowledgeBaseDependentAgentsResponseModelAgentsItem",
    "GetKnowledgeBaseDependentAgentsResponseModelAgentsItem_Available",
    "GetKnowledgeBaseDependentAgentsResponseModelAgentsItem_Unknown",
    "GetKnowledgeBaseListResponseModel",
    "GetKnowledgeBaseResponseModel",
    "GetKnowledgeBaseResponseModelAccessLevel",
    "GetKnowledgeBaseResponseModelType",
    "GetKnowledgeBaseSummaryResponseModel",
    "GetKnowledgeBaseSummaryResponseModelAccessLevel",
    "GetKnowledgeBaseSummaryResponseModelDependentAgentsItem",
    "GetKnowledgeBaseSummaryResponseModelDependentAgentsItem_Available",
    "GetKnowledgeBaseSummaryResponseModelDependentAgentsItem_Unknown",
    "GetKnowledgeBaseSummaryResponseModelType",
    "GetLibraryVoicesResponse",
    "GetPhoneNumberResponseModel",
    "GetProjectsResponse",
    "GetPronunciationDictionariesMetadataResponseModel",
    "GetPronunciationDictionaryMetadataResponse",
    "GetSpeechHistoryResponse",
    "GetVoicesResponse",
    "GetWorkspaceSecretsResponseModel",
    "HistoryAlignmentResponseModel",
    "HistoryAlignmentsResponseModel",
    "HistoryGetAllRequestSource",
    "HistoryItem",
    "HttpValidationError",
    "ImageAvatar",
    "Invoice",
    "KnowledgeBaseDocumentMetadataResponseModel",
    "KnowledgeBaseLocator",
    "KnowledgeBaseLocatorType",
    "LanguageAddedResponse",
    "LanguagePreset",
    "LanguagePresetTranslation",
    "LanguageResponse",
    "LibraryVoiceResponse",
    "LibraryVoiceResponseModelCategory",
    "LiteralJsonSchemaProperty",
    "LiteralJsonSchemaPropertyType",
    "Llm",
    "ManualVerificationFileResponse",
    "ManualVerificationResponse",
    "Model",
    "ModelRatesResponseModel",
    "ModelResponseModelConcurrencyGroup",
    "ModerationStatusResponseModel",
    "ModerationStatusResponseModelSafetyStatus",
    "ModerationStatusResponseModelWarningStatus",
    "NotFoundError",
    "ObjectJsonSchemaProperty",
    "ObjectJsonSchemaPropertyPropertiesValue",
    "OrbAvatar",
    "OutputFormat",
    "PhoneNumberAgentInfo",
    "PodcastBulletinMode",
    "PodcastBulletinModeData",
    "PodcastConversationMode",
    "PodcastConversationModeData",
    "PodcastProjectResponseModel",
    "PodcastTextSource",
    "PodcastUrlSource",
    "PostAgentAvatarResponseModel",
    "PostWorkspaceSecretResponseModel",
    "PrivacyConfig",
    "ProfilePageResponseModel",
    "ProjectCreationMetaResponseModel",
    "ProjectCreationMetaResponseModelStatus",
    "ProjectCreationMetaResponseModelType",
    "ProjectExtendedResponseModel",
    "ProjectExtendedResponseModelAccessLevel",
    "ProjectExtendedResponseModelApplyTextNormalization",
    "ProjectExtendedResponseModelFiction",
    "ProjectExtendedResponseModelQualityPreset",
    "ProjectExtendedResponseModelSourceType",
    "ProjectExtendedResponseModelTargetAudience",
    "ProjectResponse",
    "ProjectResponseModelAccessLevel",
    "ProjectResponseModelFiction",
    "ProjectResponseModelSourceType",
    "ProjectResponseModelTargetAudience",
    "ProjectSnapshotExtendedResponseModel",
    "ProjectSnapshotResponse",
    "ProjectSnapshotUploadResponseModel",
    "ProjectSnapshotUploadResponseModelStatus",
    "ProjectSnapshotsResponse",
    "ProjectState",
    "PromptAgent",
    "PromptAgentOverride",
    "PromptAgentOverrideConfig",
    "PromptAgentToolsItem",
    "PromptAgentToolsItem_Client",
    "PromptAgentToolsItem_System",
    "PromptAgentToolsItem_Webhook",
    "PromptEvaluationCriteria",
    "PronunciationDictionaryAddFromFileRequestWorkspaceAccess",
    "PronunciationDictionaryAliasRuleRequestModel",
    "PronunciationDictionaryPhonemeRuleRequestModel",
    "PronunciationDictionaryRule",
    "PronunciationDictionaryRule_Alias",
    "PronunciationDictionaryRule_Phoneme",
    "PronunciationDictionaryVersionLocator",
    "PronunciationDictionaryVersionResponseModel",
    "PydanticPronunciationDictionaryVersionLocator",
    "QueryParamsJsonSchema",
    "RagConfig",
    "RagIndexResponseModel",
    "RagIndexStatus",
    "ReaderResourceResponseModel",
    "ReaderResourceResponseModelResourceType",
    "RecordingResponse",
    "RemovePronunciationDictionaryRulesResponseModel",
    "ResourceAccessInfo",
    "ResourceAccessInfoRole",
    "ReviewStatus",
    "SafetyCommonModel",
    "SafetyEvaluation",
    "SafetyResponseModel",
    "SafetyRule",
    "SecretDependencyType",
    "SegmentCreateResponse",
    "SegmentDeleteResponse",
    "SegmentDubResponse",
    "SegmentTranscriptionResponse",
    "SegmentTranslationResponse",
    "SegmentUpdateResponse",
    "SpeakerSegment",
    "SpeakerTrack",
    "SpeechHistoryItemResponse",
    "SpeechHistoryItemResponseModelSource",
    "SpeechHistoryItemResponseModelVoiceCategory",
    "SpeechToTextCharacterResponseModel",
    "SpeechToTextChunkResponseModel",
    "SpeechToTextConvertRequestTimestampsGranularity",
    "SpeechToTextWordResponseModel",
    "SpeechToTextWordResponseModelType",
    "StreamingAudioChunkWithTimestampsResponseModel",
    "Subscription",
    "SubscriptionResponse",
    "SubscriptionResponseModelBillingPeriod",
    "SubscriptionResponseModelCharacterRefreshPeriod",
    "SubscriptionResponseModelCurrency",
    "SubscriptionStatus",
    "SubscriptionUsageResponseModel",
    "SystemToolConfig",
    "TelephonyProvider",
    "TextToSoundEffectsConvertRequestOutputFormat",
    "TextToSpeechAsStreamRequest",
    "TextToVoiceCreatePreviewsRequestOutputFormat",
    "TooEarlyError",
    "TtsConversationalConfig",
    "TtsConversationalConfigOverride",
    "TtsConversationalConfigOverrideConfig",
    "TtsConversationalModel",
    "TtsOptimizeStreamingLatency",
    "TtsOutputFormat",
    "TurnConfig",
    "TurnMode",
    "UnprocessableEntityError",
    "UpdateWorkspaceMemberResponseModel",
    "UrlAvatar",
    "UsageCharactersResponseModel",
    "User",
    "UserFeedback",
    "UserFeedbackScore",
    "ValidationError",
    "ValidationErrorLocItem",
    "VerificationAttemptResponse",
    "VerifiedVoiceLanguageResponseModel",
    "Voice",
    "VoiceGenerationParameterOptionResponse",
    "VoiceGenerationParameterResponse",
    "VoicePreviewResponseModel",
    "VoicePreviewsResponseModel",
    "VoiceResponseModelCategory",
    "VoiceResponseModelSafetyControl",
    "VoiceSample",
    "VoiceSettings",
    "VoiceSharingModerationCheckResponseModel",
    "VoiceSharingResponse",
    "VoiceSharingResponseModelCategory",
    "VoiceSharingState",
    "VoiceVerificationResponse",
    "VoicesGetSharedRequestCategory",
    "WebhookToolApiSchemaConfig",
    "WebhookToolApiSchemaConfigMethod",
    "WebhookToolApiSchemaConfigRequestHeadersValue",
    "WebhookToolConfig",
    "WidgetConfig",
    "WidgetConfigAvatar",
    "WidgetConfigAvatar_Image",
    "WidgetConfigAvatar_Orb",
    "WidgetConfigAvatar_Url",
    "WidgetConfigResponseModel",
    "WidgetConfigResponseModelAvatar",
    "WidgetConfigResponseModelAvatar_Image",
    "WidgetConfigResponseModelAvatar_Orb",
    "WidgetConfigResponseModelAvatar_Url",
    "WidgetExpandable",
    "WidgetFeedbackMode",
    "WorkspaceGroupByNameResponseModel",
    "__version__",
    "audio_isolation",
    "audio_native",
    "conversational_ai",
    "dubbing",
    "history",
    "models",
    "play",
    "projects",
    "pronunciation_dictionary",
    "samples",
    "save",
    "speech_to_speech",
    "speech_to_text",
    "stream",
    "studio",
    "text_to_sound_effects",
    "text_to_speech",
    "text_to_voice",
    "usage",
    "user",
    "voice_generation",
    "voices",
    "workspace",
]
