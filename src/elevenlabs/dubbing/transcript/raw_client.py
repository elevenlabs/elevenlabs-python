# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.http_response import AsyncHttpResponse, HttpResponse
from ...core.jsonable_encoder import jsonable_encoder
from ...core.request_options import RequestOptions
from ...core.unchecked_base_model import construct_type
from ...errors.forbidden_error import ForbiddenError
from ...errors.not_found_error import NotFoundError
from ...errors.too_early_error import TooEarlyError
from ...errors.unprocessable_entity_error import UnprocessableEntityError
from ...types.http_validation_error import HttpValidationError
from .types.transcript_get_transcript_for_dub_request_format_type import TranscriptGetTranscriptForDubRequestFormatType


class RawTranscriptClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get_transcript_for_dub(
        self,
        dubbing_id: str,
        language_code: str,
        *,
        format_type: typing.Optional[TranscriptGetTranscriptForDubRequestFormatType] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> HttpResponse[str]:
        """
        Returns transcript for the dub as an SRT or WEBVTT file.

        Parameters
        ----------
        dubbing_id : str
            ID of the dubbing project.

        language_code : str
            ID of the language.

        format_type : typing.Optional[TranscriptGetTranscriptForDubRequestFormatType]
            Format to use for the subtitle file, either 'srt' or 'webvtt'

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[str]
            Successful Response
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/dubbing/{jsonable_encoder(dubbing_id)}/transcript/{jsonable_encoder(language_code)}",
            method="GET",
            params={
                "format_type": format_type,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return HttpResponse(response=_response, data=_response.text)  # type: ignore
            if _response.status_code == 403:
                raise ForbiddenError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
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
            if _response.status_code == 425:
                raise TooEarlyError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)


class AsyncRawTranscriptClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get_transcript_for_dub(
        self,
        dubbing_id: str,
        language_code: str,
        *,
        format_type: typing.Optional[TranscriptGetTranscriptForDubRequestFormatType] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncHttpResponse[str]:
        """
        Returns transcript for the dub as an SRT or WEBVTT file.

        Parameters
        ----------
        dubbing_id : str
            ID of the dubbing project.

        language_code : str
            ID of the language.

        format_type : typing.Optional[TranscriptGetTranscriptForDubRequestFormatType]
            Format to use for the subtitle file, either 'srt' or 'webvtt'

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[str]
            Successful Response
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/dubbing/{jsonable_encoder(dubbing_id)}/transcript/{jsonable_encoder(language_code)}",
            method="GET",
            params={
                "format_type": format_type,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return AsyncHttpResponse(response=_response, data=_response.text)  # type: ignore
            if _response.status_code == 403:
                raise ForbiddenError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
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
            if _response.status_code == 425:
                raise TooEarlyError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        construct_type(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)
