# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.remove_none_from_dict import remove_none_from_dict
from ..core.request_options import RequestOptions
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from ..types.voice_generation_parameter_response import VoiceGenerationParameterResponse
from ..types.voice_response import VoiceResponse
from .types.age import Age
from .types.gender import Gender

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class VoiceGenerationClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def voice_generation_parameters(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> VoiceGenerationParameterResponse:
        """
        Get possible parameters for the /v1/voice-generation/generate-voice endpoint.

        Parameters:
            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.voice_generation.voice_generation_parameters()
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "v1/voice-generation/generate-voice/parameters"
            ),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(VoiceGenerationParameterResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def generate_a_random_voice(
        self,
        *,
        gender: Gender,
        accent: str,
        age: Age,
        accent_strength: float,
        text: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[bytes]:
        """
        Generate a random voice based on parameters. This method returns a generated_voice_id in the response header, and a sample of the voice in the body. If you like the generated voice call /v1/voice-generation/create-voice with the generated_voice_id to create the voice.

        Parameters:
            - gender: Gender. Category code corresponding to the gender of the generated voice. Possible values: female, male.

            - accent: str. Category code corresponding to the accent of the generated voice. Possible values: american, british, african, australian, indian.

            - age: Age. Category code corresponding to the age of the generated voice. Possible values: young, middle_aged, old.

            - accent_strength: float. The strength of the accent of the generated voice. Has to be between 0.3 and 2.0.

            - text: str. Text to generate, text length has to be between 100 and 1000.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        """
        with self._client_wrapper.httpx_client.stream(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v1/voice-generation/generate-voice"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(
                {"gender": gender, "accent": accent, "age": age, "accent_strength": accent_strength, "text": text}
            )
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(
                    {"gender": gender, "accent": accent, "age": age, "accent_strength": accent_strength, "text": text}
                ),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        ) as _response:
            if 200 <= _response.status_code < 300:
                for _chunk in _response.iter_bytes():
                    yield _chunk
                return
            _response.read()
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_a_previously_generated_voice(
        self,
        *,
        voice_name: str,
        voice_description: str,
        generated_voice_id: str,
        labels: typing.Optional[typing.Dict[str, str]] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> VoiceResponse:
        """
        Create a previously generated voice. This endpoint should be called after you fetched a generated_voice_id using /v1/voice-generation/generate-voice.

        Parameters:
            - voice_name: str. Name to use for the created voice.

            - voice_description: str. Description to use for the created voice.

            - generated_voice_id: str. The generated_voice_id to create, call POST /v1/voice-generation/generate-voice and fetch the generated_voice_id from the response header if don't have one yet.

            - labels: typing.Optional[typing.Dict[str, str]]. Optional, metadata to add to the created voice. Defaults to None.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.voice_generation.create_a_previously_generated_voice(
            voice_name="voice_name",
            voice_description="voice_description",
            generated_voice_id="generated_voice_id",
        )
        """
        _request: typing.Dict[str, typing.Any] = {
            "voice_name": voice_name,
            "voice_description": voice_description,
            "generated_voice_id": generated_voice_id,
        }
        if labels is not OMIT:
            _request["labels"] = labels
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v1/voice-generation/create-voice"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(VoiceResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncVoiceGenerationClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def voice_generation_parameters(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> VoiceGenerationParameterResponse:
        """
        Get possible parameters for the /v1/voice-generation/generate-voice endpoint.

        Parameters:
            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )
        await client.voice_generation.voice_generation_parameters()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "v1/voice-generation/generate-voice/parameters"
            ),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(VoiceGenerationParameterResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def generate_a_random_voice(
        self,
        *,
        gender: Gender,
        accent: str,
        age: Age,
        accent_strength: float,
        text: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[bytes]:
        """
        Generate a random voice based on parameters. This method returns a generated_voice_id in the response header, and a sample of the voice in the body. If you like the generated voice call /v1/voice-generation/create-voice with the generated_voice_id to create the voice.

        Parameters:
            - gender: Gender. Category code corresponding to the gender of the generated voice. Possible values: female, male.

            - accent: str. Category code corresponding to the accent of the generated voice. Possible values: american, british, african, australian, indian.

            - age: Age. Category code corresponding to the age of the generated voice. Possible values: young, middle_aged, old.

            - accent_strength: float. The strength of the accent of the generated voice. Has to be between 0.3 and 2.0.

            - text: str. Text to generate, text length has to be between 100 and 1000.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        """
        async with self._client_wrapper.httpx_client.stream(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v1/voice-generation/generate-voice"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(
                {"gender": gender, "accent": accent, "age": age, "accent_strength": accent_strength, "text": text}
            )
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(
                    {"gender": gender, "accent": accent, "age": age, "accent_strength": accent_strength, "text": text}
                ),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        ) as _response:
            if 200 <= _response.status_code < 300:
                async for _chunk in _response.aiter_bytes():
                    yield _chunk
                return
            await _response.aread()
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_a_previously_generated_voice(
        self,
        *,
        voice_name: str,
        voice_description: str,
        generated_voice_id: str,
        labels: typing.Optional[typing.Dict[str, str]] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> VoiceResponse:
        """
        Create a previously generated voice. This endpoint should be called after you fetched a generated_voice_id using /v1/voice-generation/generate-voice.

        Parameters:
            - voice_name: str. Name to use for the created voice.

            - voice_description: str. Description to use for the created voice.

            - generated_voice_id: str. The generated_voice_id to create, call POST /v1/voice-generation/generate-voice and fetch the generated_voice_id from the response header if don't have one yet.

            - labels: typing.Optional[typing.Dict[str, str]]. Optional, metadata to add to the created voice. Defaults to None.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )
        await client.voice_generation.create_a_previously_generated_voice(
            voice_name="voice_name",
            voice_description="voice_description",
            generated_voice_id="generated_voice_id",
        )
        """
        _request: typing.Dict[str, typing.Any] = {
            "voice_name": voice_name,
            "voice_description": voice_description,
            "generated_voice_id": generated_voice_id,
        }
        if labels is not OMIT:
            _request["labels"] = labels
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v1/voice-generation/create-voice"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else 60,
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(VoiceResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
