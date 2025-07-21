import typing
import os
import httpx
from functools import wraps

from .base_client import \
  BaseElevenLabs, AsyncBaseElevenLabs
from .environment import ElevenLabsEnvironment
from .realtime_tts import RealtimeTextToSpeechClient
from .webhooks_custom import WebhooksClient, AsyncWebhooksClient


# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


def get_base_url_host(base_url: str) -> str:
    return httpx.URL(base_url).host


class ElevenLabs(BaseElevenLabs):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - base_url: typing.Optional[str]. The base url to use for requests from the client.

        - environment: ElevenLabsEnvironment. The environment to use for requests from the client. from .environment import ElevenLabsEnvironment

        Defaults to ElevenLabsEnvironment.PRODUCTION

        - api_key: typing.Optional[str].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds.

        - httpx_client: typing.Optional[httpx.Client]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from elevenlabs.client import ElevenLabs

    client = ElevenLabs(
        api_key="YOUR_API_KEY",
    )
    """
    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ElevenLabsEnvironment = ElevenLabsEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = os.getenv("ELEVENLABS_API_KEY"),
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        super().__init__(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client
        )
        self.text_to_speech = RealtimeTextToSpeechClient(client_wrapper=self._client_wrapper)
        self.webhooks = WebhooksClient(client_wrapper=self._client_wrapper)


class AsyncElevenLabs(AsyncBaseElevenLabs):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - base_url: typing.Optional[str]. The base url to use for requests from the client.

        - environment: ElevenLabsEnvironment. The environment to use for requests from the client. from .environment import ElevenLabsEnvironment

        Defaults to ElevenLabsEnvironment.PRODUCTION

        - api_key: typing.Optional[str].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds.

        - httpx_client: typing.Optional[httpx.AsyncClient]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from elevenlabs.client import AsyncElevenLabs

    client = AsyncElevenLabs(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ElevenLabsEnvironment = ElevenLabsEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = os.getenv("ELEVENLABS_API_KEY"),
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None
    ):
        super().__init__(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client
        )
        self.webhooks = AsyncWebhooksClient(client_wrapper=self._client_wrapper)
