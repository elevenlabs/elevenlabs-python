# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from .. import core
from ..core.request_options import RequestOptions
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from ..core.unchecked_base_model import construct_type
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class AudioIsolationClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def audio_isolation(
        self,
        *,
        audio: core.File,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[bytes]:
        """
        Removes background noise from audio

        Parameters
        ----------
        audio : core.File
            See core.File for more documentation

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.

        Yields
        ------
        typing.Iterator[bytes]
            Successful Response
        """
        with self._client_wrapper.httpx_client.stream(
            "v1/audio-isolation",
            base_url=self._client_wrapper.get_environment().base,
            method="POST",
            data={},
            files={
                "audio": audio,
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _chunk_size = request_options.get("chunk_size", 1024) if request_options is not None else 1024
                    for _chunk in _response.iter_bytes(chunk_size=_chunk_size):
                        yield _chunk
                    return
                _response.read()
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

    def audio_isolation_stream(
        self,
        *,
        audio: core.File,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[bytes]:
        """
        Removes background noise from audio and streams the result

        Parameters
        ----------
        audio : core.File
            See core.File for more documentation

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.

        Yields
        ------
        typing.Iterator[bytes]
            Successful Response
        """
        with self._client_wrapper.httpx_client.stream(
            "v1/audio-isolation/stream",
            base_url=self._client_wrapper.get_environment().base,
            method="POST",
            data={},
            files={
                "audio": audio,
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _chunk_size = request_options.get("chunk_size", 1024) if request_options is not None else 1024
                    for _chunk in _response.iter_bytes(chunk_size=_chunk_size):
                        yield _chunk
                    return
                _response.read()
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


class AsyncAudioIsolationClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def audio_isolation(
        self,
        *,
        audio: core.File,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[bytes]:
        """
        Removes background noise from audio

        Parameters
        ----------
        audio : core.File
            See core.File for more documentation

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.

        Yields
        ------
        typing.AsyncIterator[bytes]
            Successful Response
        """
        async with self._client_wrapper.httpx_client.stream(
            "v1/audio-isolation",
            base_url=self._client_wrapper.get_environment().base,
            method="POST",
            data={},
            files={
                "audio": audio,
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _chunk_size = request_options.get("chunk_size", 1024) if request_options is not None else 1024
                    async for _chunk in _response.aiter_bytes(chunk_size=_chunk_size):
                        yield _chunk
                    return
                await _response.aread()
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

    async def audio_isolation_stream(
        self,
        *,
        audio: core.File,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[bytes]:
        """
        Removes background noise from audio and streams the result

        Parameters
        ----------
        audio : core.File
            See core.File for more documentation

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.

        Yields
        ------
        typing.AsyncIterator[bytes]
            Successful Response
        """
        async with self._client_wrapper.httpx_client.stream(
            "v1/audio-isolation/stream",
            base_url=self._client_wrapper.get_environment().base,
            method="POST",
            data={},
            files={
                "audio": audio,
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _chunk_size = request_options.get("chunk_size", 1024) if request_options is not None else 1024
                    async for _chunk in _response.aiter_bytes(chunk_size=_chunk_size):
                        yield _chunk
                    return
                await _response.aread()
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
