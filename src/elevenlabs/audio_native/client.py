# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from .. import core
from ..core.request_options import RequestOptions
from ..types.audio_native_create_project_response_model import AudioNativeCreateProjectResponseModel
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class AudioNativeClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def create(
        self,
        *,
        name: str,
        image: typing.Optional[str] = OMIT,
        author: typing.Optional[str] = OMIT,
        title: typing.Optional[str] = OMIT,
        small: typing.Optional[bool] = OMIT,
        text_color: typing.Optional[str] = OMIT,
        background_color: typing.Optional[str] = OMIT,
        sessionization: typing.Optional[int] = OMIT,
        voice_id: typing.Optional[str] = OMIT,
        model_id: typing.Optional[str] = OMIT,
        file: typing.Optional[core.File] = OMIT,
        auto_convert: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AudioNativeCreateProjectResponseModel:
        """
        Creates AudioNative enabled project, optionally starts conversion and returns project id and embeddable html snippet.

        Parameters
        ----------
        name : str
            Project name.

        image : typing.Optional[str]
            Image URL used in the player. If not provided, default image set in the Player settings is used.

        author : typing.Optional[str]
            Author used in the player and inserted at the start of the uploaded article. If not provided, the default author set in the Player settings is used.

        title : typing.Optional[str]
            Title used in the player and inserted at the top of the uploaded article. If not provided, the default title set in the Player settings is used.

        small : typing.Optional[bool]
            Whether to use small player or not. If not provided, default value set in the Player settings is used.

        text_color : typing.Optional[str]
            Text color used in the player. If not provided, default text color set in the Player settings is used.

        background_color : typing.Optional[str]
            Background color used in the player. If not provided, default background color set in the Player settings is used.

        sessionization : typing.Optional[int]
            Specifies for how many minutes to persist the session across page reloads. If not provided, default sessionization set in the Player settings is used.

        voice_id : typing.Optional[str]
            Voice ID used to voice the content. If not provided, default voice ID set in the Player settings is used.

        model_id : typing.Optional[str]
            TTS Model ID used in the player. If not provided, default model ID set in the Player settings is used.

        file : typing.Optional[core.File]
            See core.File for more documentation

        auto_convert : typing.Optional[bool]
            Whether to auto convert the project to audio or not.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AudioNativeCreateProjectResponseModel
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.audio_native.create(
            name="name",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/audio-native",
            method="POST",
            data={
                "name": name,
                "image": image,
                "author": author,
                "title": title,
                "small": small,
                "text_color": text_color,
                "background_color": background_color,
                "sessionization": sessionization,
                "voice_id": voice_id,
                "model_id": model_id,
                "auto_convert": auto_convert,
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
                    AudioNativeCreateProjectResponseModel,
                    construct_type(
                        type_=AudioNativeCreateProjectResponseModel,  # type: ignore
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


class AsyncAudioNativeClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def create(
        self,
        *,
        name: str,
        image: typing.Optional[str] = OMIT,
        author: typing.Optional[str] = OMIT,
        title: typing.Optional[str] = OMIT,
        small: typing.Optional[bool] = OMIT,
        text_color: typing.Optional[str] = OMIT,
        background_color: typing.Optional[str] = OMIT,
        sessionization: typing.Optional[int] = OMIT,
        voice_id: typing.Optional[str] = OMIT,
        model_id: typing.Optional[str] = OMIT,
        file: typing.Optional[core.File] = OMIT,
        auto_convert: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AudioNativeCreateProjectResponseModel:
        """
        Creates AudioNative enabled project, optionally starts conversion and returns project id and embeddable html snippet.

        Parameters
        ----------
        name : str
            Project name.

        image : typing.Optional[str]
            Image URL used in the player. If not provided, default image set in the Player settings is used.

        author : typing.Optional[str]
            Author used in the player and inserted at the start of the uploaded article. If not provided, the default author set in the Player settings is used.

        title : typing.Optional[str]
            Title used in the player and inserted at the top of the uploaded article. If not provided, the default title set in the Player settings is used.

        small : typing.Optional[bool]
            Whether to use small player or not. If not provided, default value set in the Player settings is used.

        text_color : typing.Optional[str]
            Text color used in the player. If not provided, default text color set in the Player settings is used.

        background_color : typing.Optional[str]
            Background color used in the player. If not provided, default background color set in the Player settings is used.

        sessionization : typing.Optional[int]
            Specifies for how many minutes to persist the session across page reloads. If not provided, default sessionization set in the Player settings is used.

        voice_id : typing.Optional[str]
            Voice ID used to voice the content. If not provided, default voice ID set in the Player settings is used.

        model_id : typing.Optional[str]
            TTS Model ID used in the player. If not provided, default model ID set in the Player settings is used.

        file : typing.Optional[core.File]
            See core.File for more documentation

        auto_convert : typing.Optional[bool]
            Whether to auto convert the project to audio or not.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AudioNativeCreateProjectResponseModel
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.audio_native.create(
                name="name",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/audio-native",
            method="POST",
            data={
                "name": name,
                "image": image,
                "author": author,
                "title": title,
                "small": small,
                "text_color": text_color,
                "background_color": background_color,
                "sessionization": sessionization,
                "voice_id": voice_id,
                "model_id": model_id,
                "auto_convert": auto_convert,
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
                    AudioNativeCreateProjectResponseModel,
                    construct_type(
                        type_=AudioNativeCreateProjectResponseModel,  # type: ignore
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
