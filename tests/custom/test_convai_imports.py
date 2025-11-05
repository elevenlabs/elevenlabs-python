def test_convai_imports():
    from elevenlabs.conversational_ai.phone_numbers.types import (
        PhoneNumbersCreateRequestBody_Twilio as PhoneNumbersCreateRequestBody,
    )
    from elevenlabs.conversational_ai.phone_numbers.types import (
        PhoneNumbersUpdateResponse,
    )
    from elevenlabs.core.api_error import ApiError as ElevenLabsApiError
    from elevenlabs.core.request_options import RequestOptions
    from elevenlabs.types import (
        AgentCallLimits,
        AgentConfig,
        AgentPlatformSettingsRequestModel,
        AgentWorkspaceOverridesInput,
        ArrayJsonSchemaPropertyOutput,
        ClientEvent,
        ConvAiSecretLocator,
        ConversationalConfig,
        ConversationConfig,
        ConversationInitiationClientDataConfigInput,
        ConversationInitiationClientDataWebhook,
        CreateAgentResponseModel,
        CreatePhoneNumberResponseModel,
        DynamicVariablesConfig,
        DynamicVariablesConfigDynamicVariablePlaceholdersValue,
        GetAgentResponseModel,
        GetAgentsPageResponseModel,
        GetPronunciationDictionariesMetadataResponseModel,
        GetPronunciationDictionaryMetadataResponse,
        Llm,
        PromptAgentApiModelInputToolsItem_System,
        PromptAgentApiModelOutput,
        PromptAgentApiModelOutputToolsItem_System,
        PydanticPronunciationDictionaryVersionLocator,
        SystemToolConfigInputParams_EndCall,
        SystemToolConfigOutputParams_EndCall,
        TtsConversationalConfigOutput,
        TurnConfig,
        TurnMode,
    )
    from pydantic import BaseModel
