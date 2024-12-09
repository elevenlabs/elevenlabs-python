# This file was auto-generated by Fern from our API Definition.

import typing
from .environment import ElevenLabsEnvironment
import os
import httpx
from .core.client_wrapper import SyncClientWrapper
from .history.client import HistoryClient
from .text_to_sound_effects.client import TextToSoundEffectsClient
from .audio_isolation.client import AudioIsolationClient
from .samples.client import SamplesClient
from .text_to_speech.client import TextToSpeechClient
from .speech_to_speech.client import SpeechToSpeechClient
from .voice_generation.client import VoiceGenerationClient
from .text_to_voice.client import TextToVoiceClient
from .user.client import UserClient
from .voices.client import VoicesClient
from .projects.client import ProjectsClient
from .chapters.client import ChaptersClient
from .dubbing.client import DubbingClient
from .models.client import ModelsClient
from .audio_native.client import AudioNativeClient
from .usage.client import UsageClient
from .pronunciation_dictionary.client import PronunciationDictionaryClient
from .workspace.client import WorkspaceClient
from .profile.client import ProfileClient
from .conversational_ai.client import ConversationalAiClient
from .reader_publisher_profiles.client import ReaderPublisherProfilesClient
from .types.body_manually_review_a_read_admin_6_rnp_7_bvc_2_t_reads_read_id_review_post_review_status import (
    BodyManuallyReviewAReadAdmin6Rnp7Bvc2TReadsReadIdReviewPostReviewStatus,
)
from .core.request_options import RequestOptions
from .core.jsonable_encoder import jsonable_encoder
from .core.unchecked_base_model import construct_type
from .errors.unprocessable_entity_error import UnprocessableEntityError
from .types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from .core.api_error import ApiError
from .core.client_wrapper import AsyncClientWrapper
from .history.client import AsyncHistoryClient
from .text_to_sound_effects.client import AsyncTextToSoundEffectsClient
from .audio_isolation.client import AsyncAudioIsolationClient
from .samples.client import AsyncSamplesClient
from .text_to_speech.client import AsyncTextToSpeechClient
from .speech_to_speech.client import AsyncSpeechToSpeechClient
from .voice_generation.client import AsyncVoiceGenerationClient
from .text_to_voice.client import AsyncTextToVoiceClient
from .user.client import AsyncUserClient
from .voices.client import AsyncVoicesClient
from .projects.client import AsyncProjectsClient
from .chapters.client import AsyncChaptersClient
from .dubbing.client import AsyncDubbingClient
from .models.client import AsyncModelsClient
from .audio_native.client import AsyncAudioNativeClient
from .usage.client import AsyncUsageClient
from .pronunciation_dictionary.client import AsyncPronunciationDictionaryClient
from .workspace.client import AsyncWorkspaceClient
from .profile.client import AsyncProfileClient
from .conversational_ai.client import AsyncConversationalAiClient
from .reader_publisher_profiles.client import AsyncReaderPublisherProfilesClient

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class BaseElevenLabs:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : ElevenLabsEnvironment
        The environment to use for requests from the client. from .environment import ElevenLabsEnvironment



        Defaults to ElevenLabsEnvironment.PRODUCTION



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from elevenlabs import ElevenLabs

    client = ElevenLabs(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ElevenLabsEnvironment = ElevenLabsEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = os.getenv("ELEVEN_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.history = HistoryClient(client_wrapper=self._client_wrapper)
        self.text_to_sound_effects = TextToSoundEffectsClient(client_wrapper=self._client_wrapper)
        self.audio_isolation = AudioIsolationClient(client_wrapper=self._client_wrapper)
        self.samples = SamplesClient(client_wrapper=self._client_wrapper)
        self.text_to_speech = TextToSpeechClient(client_wrapper=self._client_wrapper)
        self.speech_to_speech = SpeechToSpeechClient(client_wrapper=self._client_wrapper)
        self.voice_generation = VoiceGenerationClient(client_wrapper=self._client_wrapper)
        self.text_to_voice = TextToVoiceClient(client_wrapper=self._client_wrapper)
        self.user = UserClient(client_wrapper=self._client_wrapper)
        self.voices = VoicesClient(client_wrapper=self._client_wrapper)
        self.projects = ProjectsClient(client_wrapper=self._client_wrapper)
        self.chapters = ChaptersClient(client_wrapper=self._client_wrapper)
        self.dubbing = DubbingClient(client_wrapper=self._client_wrapper)
        self.models = ModelsClient(client_wrapper=self._client_wrapper)
        self.audio_native = AudioNativeClient(client_wrapper=self._client_wrapper)
        self.usage = UsageClient(client_wrapper=self._client_wrapper)
        self.pronunciation_dictionary = PronunciationDictionaryClient(client_wrapper=self._client_wrapper)
        self.workspace = WorkspaceClient(client_wrapper=self._client_wrapper)
        self.profile = ProfileClient(client_wrapper=self._client_wrapper)
        self.conversational_ai = ConversationalAiClient(client_wrapper=self._client_wrapper)
        self.reader_publisher_profiles = ReaderPublisherProfilesClient(client_wrapper=self._client_wrapper)

    def manually_review_a_read_admin_6_rnp_7_bvc_2_t_reads_read_id_review_post(
        self,
        read_id: str,
        *,
        review_status: BodyManuallyReviewAReadAdmin6Rnp7Bvc2TReadsReadIdReviewPostReviewStatus,
        review_comment: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[typing.Any]:
        """
        Manually review a read

        Parameters
        ----------
        read_id : str
            The ID of the read to get the HTML for.

        review_status : BodyManuallyReviewAReadAdmin6Rnp7Bvc2TReadsReadIdReviewPostReviewStatus
            The review status of the read: 'accepted' or 'rejected'

        review_comment : typing.Optional[str]
            The review comment

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.manually_review_a_read_admin_6_rnp_7_bvc_2_t_reads_read_id_review_post(
            read_id="read_id",
            review_status="approved",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"admin/6rnp7bvc2t/reads/{jsonable_encoder(read_id)}/review",
            method="POST",
            json={
                "review_status": review_status,
                "review_comment": review_comment,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    construct_type(
                        type_=typing.Optional[typing.Any],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncBaseElevenLabs:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : ElevenLabsEnvironment
        The environment to use for requests from the client. from .environment import ElevenLabsEnvironment



        Defaults to ElevenLabsEnvironment.PRODUCTION



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from elevenlabs import AsyncElevenLabs

    client = AsyncElevenLabs(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ElevenLabsEnvironment = ElevenLabsEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = os.getenv("ELEVEN_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.history = AsyncHistoryClient(client_wrapper=self._client_wrapper)
        self.text_to_sound_effects = AsyncTextToSoundEffectsClient(client_wrapper=self._client_wrapper)
        self.audio_isolation = AsyncAudioIsolationClient(client_wrapper=self._client_wrapper)
        self.samples = AsyncSamplesClient(client_wrapper=self._client_wrapper)
        self.text_to_speech = AsyncTextToSpeechClient(client_wrapper=self._client_wrapper)
        self.speech_to_speech = AsyncSpeechToSpeechClient(client_wrapper=self._client_wrapper)
        self.voice_generation = AsyncVoiceGenerationClient(client_wrapper=self._client_wrapper)
        self.text_to_voice = AsyncTextToVoiceClient(client_wrapper=self._client_wrapper)
        self.user = AsyncUserClient(client_wrapper=self._client_wrapper)
        self.voices = AsyncVoicesClient(client_wrapper=self._client_wrapper)
        self.projects = AsyncProjectsClient(client_wrapper=self._client_wrapper)
        self.chapters = AsyncChaptersClient(client_wrapper=self._client_wrapper)
        self.dubbing = AsyncDubbingClient(client_wrapper=self._client_wrapper)
        self.models = AsyncModelsClient(client_wrapper=self._client_wrapper)
        self.audio_native = AsyncAudioNativeClient(client_wrapper=self._client_wrapper)
        self.usage = AsyncUsageClient(client_wrapper=self._client_wrapper)
        self.pronunciation_dictionary = AsyncPronunciationDictionaryClient(client_wrapper=self._client_wrapper)
        self.workspace = AsyncWorkspaceClient(client_wrapper=self._client_wrapper)
        self.profile = AsyncProfileClient(client_wrapper=self._client_wrapper)
        self.conversational_ai = AsyncConversationalAiClient(client_wrapper=self._client_wrapper)
        self.reader_publisher_profiles = AsyncReaderPublisherProfilesClient(client_wrapper=self._client_wrapper)

    async def manually_review_a_read_admin_6_rnp_7_bvc_2_t_reads_read_id_review_post(
        self,
        read_id: str,
        *,
        review_status: BodyManuallyReviewAReadAdmin6Rnp7Bvc2TReadsReadIdReviewPostReviewStatus,
        review_comment: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[typing.Any]:
        """
        Manually review a read

        Parameters
        ----------
        read_id : str
            The ID of the read to get the HTML for.

        review_status : BodyManuallyReviewAReadAdmin6Rnp7Bvc2TReadsReadIdReviewPostReviewStatus
            The review status of the read: 'accepted' or 'rejected'

        review_comment : typing.Optional[str]
            The review comment

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.manually_review_a_read_admin_6_rnp_7_bvc_2_t_reads_read_id_review_post(
                read_id="read_id",
                review_status="approved",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"admin/6rnp7bvc2t/reads/{jsonable_encoder(read_id)}/review",
            method="POST",
            json={
                "review_status": review_status,
                "review_comment": review_comment,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    construct_type(
                        type_=typing.Optional[typing.Any],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: ElevenLabsEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
