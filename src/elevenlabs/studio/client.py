# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from .projects.client import ProjectsClient
from .chapters.client import ChaptersClient
from .types.body_create_podcast_v_1_studio_podcasts_post_mode import (
    BodyCreatePodcastV1StudioPodcastsPostMode,
)
from .types.body_create_podcast_v_1_studio_podcasts_post_source import (
    BodyCreatePodcastV1StudioPodcastsPostSource,
)
from .types.body_create_podcast_v_1_studio_podcasts_post_quality_preset import (
    BodyCreatePodcastV1StudioPodcastsPostQualityPreset,
)
from .types.body_create_podcast_v_1_studio_podcasts_post_duration_scale import (
    BodyCreatePodcastV1StudioPodcastsPostDurationScale,
)
from ..core.request_options import RequestOptions
from ..types.podcast_project_response_model import PodcastProjectResponseModel
from ..core.serialization import convert_and_respect_annotation_metadata
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper
from .projects.client import AsyncProjectsClient
from .chapters.client import AsyncChaptersClient

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class StudioClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper
        self.projects = ProjectsClient(client_wrapper=self._client_wrapper)
        self.chapters = ChaptersClient(client_wrapper=self._client_wrapper)

    def create_podcast(
        self,
        *,
        model_id: str,
        mode: BodyCreatePodcastV1StudioPodcastsPostMode,
        source: BodyCreatePodcastV1StudioPodcastsPostSource,
        quality_preset: typing.Optional[BodyCreatePodcastV1StudioPodcastsPostQualityPreset] = OMIT,
        duration_scale: typing.Optional[BodyCreatePodcastV1StudioPodcastsPostDurationScale] = OMIT,
        language: typing.Optional[str] = OMIT,
        highlights: typing.Optional[typing.Sequence[str]] = OMIT,
        callback_url: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PodcastProjectResponseModel:
        """
        Create and auto-convert a podcast project. Currently, the LLM cost is covered by us but you will still be charged for the audio generation. In the future, you will be charged for both the LLM and audio generation costs.

        Parameters
        ----------
        model_id : str
            The ID of the model to be used for this Studio project, you can query GET /v1/models to list all available models.

        mode : BodyCreatePodcastV1StudioPodcastsPostMode
            The type of podcast to generate. Can be 'conversation', an interaction between two voices, or 'bulletin', a monologue.

        source : BodyCreatePodcastV1StudioPodcastsPostSource
            The source content for the Podcast.

        quality_preset : typing.Optional[BodyCreatePodcastV1StudioPodcastsPostQualityPreset]
            Output quality of the generated audio. Must be one of:
            standard - standard output format, 128kbps with 44.1kHz sample rate.
            high - high quality output format, 192kbps with 44.1kHz sample rate and major improvements on our side. Using this setting increases the credit cost by 20%.
            ultra - ultra quality output format, 192kbps with 44.1kHz sample rate and highest improvements on our side. Using this setting increases the credit cost by 50%.
            ultra lossless - ultra quality output format, 705.6kbps with 44.1kHz sample rate and highest improvements on our side in a fully lossless format. Using this setting increases the credit cost by 100%.

        duration_scale : typing.Optional[BodyCreatePodcastV1StudioPodcastsPostDurationScale]
            Duration of the generated podcast. Must be one of:
            short - produces podcasts shorter than 3 minutes.
            default - produces podcasts roughly between 3-7 minutes.
            long - prodces podcasts longer than 7 minutes.

        language : typing.Optional[str]
            An optional language of the Studio project. Two-letter language code (ISO 639-1).

        highlights : typing.Optional[typing.Sequence[str]]
            A brief summary or highlights of the Studio project's content, providing key points or themes. This should be between 10 and 70 characters.

        callback_url : typing.Optional[str]
            A url that will be called by our service when the Studio project is converted. Request will contain a json blob containing the status of the conversion

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        PodcastProjectResponseModel
            Successful Response

        Examples
        --------
        from elevenlabs import (
            ElevenLabs,
            PodcastConversationModeData,
            PodcastTextSource,
        )
        from elevenlabs.studio import (
            BodyCreatePodcastV1StudioPodcastsPostMode_Conversation,
        )

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.studio.create_podcast(
            model_id="21m00Tcm4TlvDq8ikWAM",
            mode=BodyCreatePodcastV1StudioPodcastsPostMode_Conversation(
                conversation=PodcastConversationModeData(
                    host_voice_id="aw1NgEzBg83R7vgmiJt6",
                    guest_voice_id="aw1NgEzBg83R7vgmiJt7",
                ),
            ),
            source=PodcastTextSource(
                text="This is a test podcast.",
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/studio/podcasts",
            base_url=self._client_wrapper.get_environment().base,
            method="POST",
            json={
                "model_id": model_id,
                "mode": convert_and_respect_annotation_metadata(
                    object_=mode,
                    annotation=BodyCreatePodcastV1StudioPodcastsPostMode,
                    direction="write",
                ),
                "source": convert_and_respect_annotation_metadata(
                    object_=source,
                    annotation=BodyCreatePodcastV1StudioPodcastsPostSource,
                    direction="write",
                ),
                "quality_preset": quality_preset,
                "duration_scale": duration_scale,
                "language": language,
                "highlights": highlights,
                "callback_url": callback_url,
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
                    PodcastProjectResponseModel,
                    construct_type(
                        type_=PodcastProjectResponseModel,  # type: ignore
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


class AsyncStudioClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper
        self.projects = AsyncProjectsClient(client_wrapper=self._client_wrapper)
        self.chapters = AsyncChaptersClient(client_wrapper=self._client_wrapper)

    async def create_podcast(
        self,
        *,
        model_id: str,
        mode: BodyCreatePodcastV1StudioPodcastsPostMode,
        source: BodyCreatePodcastV1StudioPodcastsPostSource,
        quality_preset: typing.Optional[BodyCreatePodcastV1StudioPodcastsPostQualityPreset] = OMIT,
        duration_scale: typing.Optional[BodyCreatePodcastV1StudioPodcastsPostDurationScale] = OMIT,
        language: typing.Optional[str] = OMIT,
        highlights: typing.Optional[typing.Sequence[str]] = OMIT,
        callback_url: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PodcastProjectResponseModel:
        """
        Create and auto-convert a podcast project. Currently, the LLM cost is covered by us but you will still be charged for the audio generation. In the future, you will be charged for both the LLM and audio generation costs.

        Parameters
        ----------
        model_id : str
            The ID of the model to be used for this Studio project, you can query GET /v1/models to list all available models.

        mode : BodyCreatePodcastV1StudioPodcastsPostMode
            The type of podcast to generate. Can be 'conversation', an interaction between two voices, or 'bulletin', a monologue.

        source : BodyCreatePodcastV1StudioPodcastsPostSource
            The source content for the Podcast.

        quality_preset : typing.Optional[BodyCreatePodcastV1StudioPodcastsPostQualityPreset]
            Output quality of the generated audio. Must be one of:
            standard - standard output format, 128kbps with 44.1kHz sample rate.
            high - high quality output format, 192kbps with 44.1kHz sample rate and major improvements on our side. Using this setting increases the credit cost by 20%.
            ultra - ultra quality output format, 192kbps with 44.1kHz sample rate and highest improvements on our side. Using this setting increases the credit cost by 50%.
            ultra lossless - ultra quality output format, 705.6kbps with 44.1kHz sample rate and highest improvements on our side in a fully lossless format. Using this setting increases the credit cost by 100%.

        duration_scale : typing.Optional[BodyCreatePodcastV1StudioPodcastsPostDurationScale]
            Duration of the generated podcast. Must be one of:
            short - produces podcasts shorter than 3 minutes.
            default - produces podcasts roughly between 3-7 minutes.
            long - prodces podcasts longer than 7 minutes.

        language : typing.Optional[str]
            An optional language of the Studio project. Two-letter language code (ISO 639-1).

        highlights : typing.Optional[typing.Sequence[str]]
            A brief summary or highlights of the Studio project's content, providing key points or themes. This should be between 10 and 70 characters.

        callback_url : typing.Optional[str]
            A url that will be called by our service when the Studio project is converted. Request will contain a json blob containing the status of the conversion

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        PodcastProjectResponseModel
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import (
            AsyncElevenLabs,
            PodcastConversationModeData,
            PodcastTextSource,
        )
        from elevenlabs.studio import (
            BodyCreatePodcastV1StudioPodcastsPostMode_Conversation,
        )

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.studio.create_podcast(
                model_id="21m00Tcm4TlvDq8ikWAM",
                mode=BodyCreatePodcastV1StudioPodcastsPostMode_Conversation(
                    conversation=PodcastConversationModeData(
                        host_voice_id="aw1NgEzBg83R7vgmiJt6",
                        guest_voice_id="aw1NgEzBg83R7vgmiJt7",
                    ),
                ),
                source=PodcastTextSource(
                    text="This is a test podcast.",
                ),
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/studio/podcasts",
            base_url=self._client_wrapper.get_environment().base,
            method="POST",
            json={
                "model_id": model_id,
                "mode": convert_and_respect_annotation_metadata(
                    object_=mode,
                    annotation=BodyCreatePodcastV1StudioPodcastsPostMode,
                    direction="write",
                ),
                "source": convert_and_respect_annotation_metadata(
                    object_=source,
                    annotation=BodyCreatePodcastV1StudioPodcastsPostSource,
                    direction="write",
                ),
                "quality_preset": quality_preset,
                "duration_scale": duration_scale,
                "language": language,
                "highlights": highlights,
                "callback_url": callback_url,
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
                    PodcastProjectResponseModel,
                    construct_type(
                        type_=PodcastProjectResponseModel,  # type: ignore
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
