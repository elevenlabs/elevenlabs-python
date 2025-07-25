# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from .....core.api_error import ApiError
from .....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .....core.http_response import AsyncHttpResponse, HttpResponse
from .....core.jsonable_encoder import jsonable_encoder
from .....core.request_options import RequestOptions
from .....core.unchecked_base_model import construct_type
from .....errors.unprocessable_entity_error import UnprocessableEntityError
from .....types.http_validation_error import HttpValidationError
from .....types.voice_sample_visual_waveform_response_model import VoiceSampleVisualWaveformResponseModel


class RawWaveformClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self, voice_id: str, sample_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[VoiceSampleVisualWaveformResponseModel]:
        """
        Retrieve the visual waveform of a voice sample.

        Parameters
        ----------
        voice_id : str
            Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.

        sample_id : str
            Sample ID to be used

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[VoiceSampleVisualWaveformResponseModel]
            Successful Response
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/voices/pvc/{jsonable_encoder(voice_id)}/samples/{jsonable_encoder(sample_id)}/waveform",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    VoiceSampleVisualWaveformResponseModel,
                    construct_type(
                        type_=VoiceSampleVisualWaveformResponseModel,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)


class AsyncRawWaveformClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get(
        self, voice_id: str, sample_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[VoiceSampleVisualWaveformResponseModel]:
        """
        Retrieve the visual waveform of a voice sample.

        Parameters
        ----------
        voice_id : str
            Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.

        sample_id : str
            Sample ID to be used

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[VoiceSampleVisualWaveformResponseModel]
            Successful Response
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/voices/pvc/{jsonable_encoder(voice_id)}/samples/{jsonable_encoder(sample_id)}/waveform",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    VoiceSampleVisualWaveformResponseModel,
                    construct_type(
                        type_=VoiceSampleVisualWaveformResponseModel,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        HttpValidationError,
                        construct_type(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)
