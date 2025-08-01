# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ....core.api_error import ApiError
from ....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ....core.http_response import AsyncHttpResponse, HttpResponse
from ....core.jsonable_encoder import jsonable_encoder
from ....core.request_options import RequestOptions
from ....core.unchecked_base_model import construct_type
from ....errors.unprocessable_entity_error import UnprocessableEntityError
from ....types.get_agent_link_response_model import GetAgentLinkResponseModel
from ....types.http_validation_error import HttpValidationError


class RawLinkClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self, agent_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[GetAgentLinkResponseModel]:
        """
        Get the current link used to share the agent with others

        Parameters
        ----------
        agent_id : str
            The id of an agent. This is returned on agent creation.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[GetAgentLinkResponseModel]
            Successful Response
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/convai/agents/{jsonable_encoder(agent_id)}/link",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    GetAgentLinkResponseModel,
                    construct_type(
                        type_=GetAgentLinkResponseModel,  # type: ignore
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


class AsyncRawLinkClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get(
        self, agent_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[GetAgentLinkResponseModel]:
        """
        Get the current link used to share the agent with others

        Parameters
        ----------
        agent_id : str
            The id of an agent. This is returned on agent creation.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[GetAgentLinkResponseModel]
            Successful Response
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/convai/agents/{jsonable_encoder(agent_id)}/link",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    GetAgentLinkResponseModel,
                    construct_type(
                        type_=GetAgentLinkResponseModel,  # type: ignore
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
