# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

from .. import core
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.remove_none_from_dict import remove_none_from_dict
from ..core.request_options import RequestOptions
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.add_pronunciation_dictionary_response_model import AddPronunciationDictionaryResponseModel
from ..types.get_pronunciation_dictionary_metadata_response import GetPronunciationDictionaryMetadataResponse
from ..types.http_validation_error import HttpValidationError

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class PronunciationDictionaryClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def add_from_file(
        self,
        *,
        file: typing.Optional[core.File] = None,
        name: str,
        description: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AddPronunciationDictionaryResponseModel:
        """
        Creates a new pronunciation dictionary from a lexicon .PLS file

        Parameters:
            - file: typing.Optional[core.File]. See core.File for more documentation

            - name: str. The name of the pronunciation dictionary, used for identification only.

            - description: typing.Optional[str]. A description of the pronunciation dictionary, used for identification only.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.pronunciation_dictionary.add_from_file()
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "v1/pronunciation-dictionaries/add-from-file"
            ),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            data=jsonable_encoder(remove_none_from_dict({"name": name, "description": description}))
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(remove_none_from_dict({"name": name, "description": description})),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            files=core.convert_file_dict_to_httpx_tuples(remove_none_from_dict({"file": file})),
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
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(AddPronunciationDictionaryResponseModel, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_pls_file_with_a_pronunciation_dictionary_version_rules(
        self, dictionary_id: str, version_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Any:
        """
        Get PLS file with a pronunciation dictionary version rules

        Parameters:
            - dictionary_id: str. The id of the pronunciation dictionary

            - version_id: str. The id of the version of the pronunciation dictionary

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.pronunciation_dictionary.get_pls_file_with_a_pronunciation_dictionary_version_rules(
            dictionary_id="dictionary_id",
            version_id="version_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"v1/pronunciation-dictionaries/{jsonable_encoder(dictionary_id)}/{jsonable_encoder(version_id)}/download",
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
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.Any, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_metadata_for_a_pronunciation_dictionary_v_1_pronunciation_dictionaries_pronunciation_dictionary_id_get(
        self, pronunciation_dictionary_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> GetPronunciationDictionaryMetadataResponse:
        """
        Get metadata for a pronunciation dictionary

        Parameters:
            - pronunciation_dictionary_id: str. The id of the pronunciation dictionary

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.pronunciation_dictionary.get_metadata_for_a_pronunciation_dictionary_v_1_pronunciation_dictionaries_pronunciation_dictionary_id_get(
            pronunciation_dictionary_id="pronunciation_dictionary_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"v1/pronunciation-dictionaries/{jsonable_encoder(pronunciation_dictionary_id)}",
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
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(GetPronunciationDictionaryMetadataResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncPronunciationDictionaryClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def add_from_file(
        self,
        *,
        file: typing.Optional[core.File] = None,
        name: str,
        description: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AddPronunciationDictionaryResponseModel:
        """
        Creates a new pronunciation dictionary from a lexicon .PLS file

        Parameters:
            - file: typing.Optional[core.File]. See core.File for more documentation

            - name: str. The name of the pronunciation dictionary, used for identification only.

            - description: typing.Optional[str]. A description of the pronunciation dictionary, used for identification only.

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )
        await client.pronunciation_dictionary.add_from_file()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "v1/pronunciation-dictionaries/add-from-file"
            ),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            data=jsonable_encoder(remove_none_from_dict({"name": name, "description": description}))
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(remove_none_from_dict({"name": name, "description": description})),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            files=core.convert_file_dict_to_httpx_tuples(remove_none_from_dict({"file": file})),
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
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(AddPronunciationDictionaryResponseModel, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_pls_file_with_a_pronunciation_dictionary_version_rules(
        self, dictionary_id: str, version_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Any:
        """
        Get PLS file with a pronunciation dictionary version rules

        Parameters:
            - dictionary_id: str. The id of the pronunciation dictionary

            - version_id: str. The id of the version of the pronunciation dictionary

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )
        await client.pronunciation_dictionary.get_pls_file_with_a_pronunciation_dictionary_version_rules(
            dictionary_id="dictionary_id",
            version_id="version_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"v1/pronunciation-dictionaries/{jsonable_encoder(dictionary_id)}/{jsonable_encoder(version_id)}/download",
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
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.Any, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_metadata_for_a_pronunciation_dictionary_v_1_pronunciation_dictionaries_pronunciation_dictionary_id_get(
        self, pronunciation_dictionary_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> GetPronunciationDictionaryMetadataResponse:
        """
        Get metadata for a pronunciation dictionary

        Parameters:
            - pronunciation_dictionary_id: str. The id of the pronunciation dictionary

            - request_options: typing.Optional[RequestOptions]. Request-specific configuration.
        ---
        from elevenlabs.client import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )
        await client.pronunciation_dictionary.get_metadata_for_a_pronunciation_dictionary_v_1_pronunciation_dictionaries_pronunciation_dictionary_id_get(
            pronunciation_dictionary_id="pronunciation_dictionary_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"v1/pronunciation-dictionaries/{jsonable_encoder(pronunciation_dictionary_id)}",
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
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(GetPronunciationDictionaryMetadataResponse, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
