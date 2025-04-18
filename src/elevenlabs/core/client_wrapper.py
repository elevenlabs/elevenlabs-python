# This file was auto-generated by Fern from our API Definition.

import typing
from ..environment import ElevenLabsEnvironment
import httpx
from .http_client import HttpClient
from .http_client import AsyncHttpClient


class BaseClientWrapper:
    def __init__(
        self,
        *,
        api_key: typing.Optional[str] = None,
        environment: ElevenLabsEnvironment,
        timeout: typing.Optional[float] = None,
    ):
        self._api_key = api_key
        self._environment = environment
        self._timeout = timeout

    def get_headers(self) -> typing.Dict[str, str]:
        headers: typing.Dict[str, str] = {
            "X-Fern-Language": "Python",
            "X-Fern-SDK-Name": "elevenlabs",
            "X-Fern-SDK-Version": "1.57.0",
        }
        if self._api_key is not None:
            headers["xi-api-key"] = self._api_key
        return headers

    def get_environment(self) -> ElevenLabsEnvironment:
        return self._environment

    def get_timeout(self) -> typing.Optional[float]:
        return self._timeout


class SyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        api_key: typing.Optional[str] = None,
        environment: ElevenLabsEnvironment,
        timeout: typing.Optional[float] = None,
        httpx_client: httpx.Client,
    ):
        super().__init__(api_key=api_key, environment=environment, timeout=timeout)
        self.httpx_client = HttpClient(
            httpx_client=httpx_client,
            base_headers=self.get_headers,
            base_timeout=self.get_timeout,
        )


class AsyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        api_key: typing.Optional[str] = None,
        environment: ElevenLabsEnvironment,
        timeout: typing.Optional[float] = None,
        httpx_client: httpx.AsyncClient,
    ):
        super().__init__(api_key=api_key, environment=environment, timeout=timeout)
        self.httpx_client = AsyncHttpClient(
            httpx_client=httpx_client,
            base_headers=self.get_headers,
            base_timeout=self.get_timeout,
        )
