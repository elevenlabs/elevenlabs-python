# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from .. import core
from .types.speech_to_text_convert_request_timestamps_granularity import (
    SpeechToTextConvertRequestTimestampsGranularity,
)
from ..core.request_options import RequestOptions
from ..types.speech_to_text_chunk_response_model import SpeechToTextChunkResponseModel
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class SpeechToTextClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def convert(
        self,
        *,
        model_id: str,
        file: core.File,
        enable_logging: typing.Optional[bool] = None,
        language_code: typing.Optional[str] = OMIT,
        tag_audio_events: typing.Optional[bool] = OMIT,
        num_speakers: typing.Optional[int] = OMIT,
        timestamps_granularity: typing.Optional[SpeechToTextConvertRequestTimestampsGranularity] = OMIT,
        diarize: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SpeechToTextChunkResponseModel:
        """
        Transcribe an audio or video file.

        Parameters
        ----------
        model_id : str
            The ID of the model to use for transcription, currently only 'scribe_v1' is available.

        file : core.File
            See core.File for more documentation

        enable_logging : typing.Optional[bool]
            When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.

        language_code : typing.Optional[str]
            An ISO-639-1 or ISO-639-3 language_code corresponding to the language of the audio file. Can sometimes improve transcription performance if known beforehand. Defaults to null, in this case the language is predicted automatically.

        tag_audio_events : typing.Optional[bool]
            Whether to tag audio events like (laughter), (footsteps), etc. in the transcription.

        num_speakers : typing.Optional[int]
            The maximum amount of speakers talking in the uploaded file. Can help with predicting who speaks when. The maximum amount of speakers that can be predicted is 32. Defaults to null, in this case the amount of speakers is set to the maximum value the model supports.

        timestamps_granularity : typing.Optional[SpeechToTextConvertRequestTimestampsGranularity]
            The granularity of the timestamps in the transcription. 'word' provides word-level timestamps and 'character' provides character-level timestamps per word.

        diarize : typing.Optional[bool]
            Whether to annotate which speaker is currently talking in the uploaded file.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        SpeechToTextChunkResponseModel
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.speech_to_text.convert(
            model_id="model_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/speech-to-text",
            base_url=self._client_wrapper.get_environment().base,
            method="POST",
            params={
                "enable_logging": enable_logging,
            },
            data={
                "model_id": model_id,
                "language_code": language_code,
                "tag_audio_events": tag_audio_events,
                "num_speakers": num_speakers,
                "timestamps_granularity": timestamps_granularity,
                "diarize": diarize,
            },
            files={
                "file": file,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    SpeechToTextChunkResponseModel,
                    construct_type(
                        type_=SpeechToTextChunkResponseModel,  # type: ignore
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


class AsyncSpeechToTextClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def convert(
        self,
        *,
        model_id: str,
        file: core.File,
        enable_logging: typing.Optional[bool] = None,
        language_code: typing.Optional[str] = OMIT,
        tag_audio_events: typing.Optional[bool] = OMIT,
        num_speakers: typing.Optional[int] = OMIT,
        timestamps_granularity: typing.Optional[SpeechToTextConvertRequestTimestampsGranularity] = OMIT,
        diarize: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SpeechToTextChunkResponseModel:
        """
        Transcribe an audio or video file.

        Parameters
        ----------
        model_id : str
            The ID of the model to use for transcription, currently only 'scribe_v1' is available.

        file : core.File
            See core.File for more documentation

        enable_logging : typing.Optional[bool]
            When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.

        language_code : typing.Optional[str]
            An ISO-639-1 or ISO-639-3 language_code corresponding to the language of the audio file. Can sometimes improve transcription performance if known beforehand. Defaults to null, in this case the language is predicted automatically.

        tag_audio_events : typing.Optional[bool]
            Whether to tag audio events like (laughter), (footsteps), etc. in the transcription.

        num_speakers : typing.Optional[int]
            The maximum amount of speakers talking in the uploaded file. Can help with predicting who speaks when. The maximum amount of speakers that can be predicted is 32. Defaults to null, in this case the amount of speakers is set to the maximum value the model supports.

        timestamps_granularity : typing.Optional[SpeechToTextConvertRequestTimestampsGranularity]
            The granularity of the timestamps in the transcription. 'word' provides word-level timestamps and 'character' provides character-level timestamps per word.

        diarize : typing.Optional[bool]
            Whether to annotate which speaker is currently talking in the uploaded file.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        SpeechToTextChunkResponseModel
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.speech_to_text.convert(
                model_id="model_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/speech-to-text",
            base_url=self._client_wrapper.get_environment().base,
            method="POST",
            params={
                "enable_logging": enable_logging,
            },
            data={
                "model_id": model_id,
                "language_code": language_code,
                "tag_audio_events": tag_audio_events,
                "num_speakers": num_speakers,
                "timestamps_granularity": timestamps_granularity,
                "diarize": diarize,
            },
            files={
                "file": file,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    SpeechToTextChunkResponseModel,
                    construct_type(
                        type_=SpeechToTextChunkResponseModel,  # type: ignore
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
