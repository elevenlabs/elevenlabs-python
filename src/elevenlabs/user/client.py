# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.request_options import RequestOptions
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from ..types.subscription import Subscription
from ..types.user import User


class UserClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get_subscription(self, *, request_options: typing.Optional[RequestOptions] = None) -> Subscription:
        """
        Gets extended information about the users subscription

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Subscription
            Successful Response

        Examples
        --------
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.user.get_subscription()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/user/subscription", method="GET", request_options=request_options
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(Subscription, construct_type(type_=Subscription, object_=_response.json()))  # type: ignore
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get(self, *, request_options: typing.Optional[RequestOptions] = None) -> User:
        """
        Gets information about the user

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        User
            Successful Response

        Examples
        --------
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.user.get()
        """
        _response = self._client_wrapper.httpx_client.request("v1/user", method="GET", request_options=request_options)
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(User, construct_type(type_=User, object_=_response.json()))  # type: ignore
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncUserClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get_subscription(self, *, request_options: typing.Optional[RequestOptions] = None) -> Subscription:
        """
        Gets extended information about the users subscription

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Subscription
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs.client import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.user.get_subscription()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/user/subscription", method="GET", request_options=request_options
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(Subscription, construct_type(type_=Subscription, object_=_response.json()))  # type: ignore
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get(self, *, request_options: typing.Optional[RequestOptions] = None) -> User:
        """
        Gets information about the user

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        User
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs.client import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.user.get()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/user", method="GET", request_options=request_options
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(User, construct_type(type_=User, object_=_response.json()))  # type: ignore
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
