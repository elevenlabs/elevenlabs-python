# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from .types.text_to_voice_create_previews_request_output_format import TextToVoiceCreatePreviewsRequestOutputFormat
from ..core.request_options import RequestOptions
from ..types.voice_previews_response_model import VoicePreviewsResponseModel
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..types.voice import Voice
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class TextToVoiceClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def create_previews(
        self,
        *,
        voice_description: str,
        text: str,
        output_format: typing.Optional[TextToVoiceCreatePreviewsRequestOutputFormat] = None,
        auto_generate_text: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> VoicePreviewsResponseModel:
        """
        Generate a custom voice based on voice description. This method returns a list of voice previews. Each preview has a generated_voice_id and a sample of the voice as base64 encoded mp3 audio. If you like the a voice previewand want to create the voice call /v1/text-to-voice/create-voice-from-preview with the generated_voice_id to create the voice.

        Parameters
        ----------
        voice_description : str
            Description to use for the created voice.

        text : str
            Text to generate, text length has to be between 100 and 1000.

        output_format : typing.Optional[TextToVoiceCreatePreviewsRequestOutputFormat]
            Output format of the generated audio. Must be one of:
            mp3_22050_32 - output format, mp3 with 22.05kHz sample rate at 32kbps.
            mp3_44100_32 - output format, mp3 with 44.1kHz sample rate at 32kbps.
            mp3_44100_64 - output format, mp3 with 44.1kHz sample rate at 64kbps.
            mp3_44100_96 - output format, mp3 with 44.1kHz sample rate at 96kbps.
            mp3_44100_128 - default output format, mp3 with 44.1kHz sample rate at 128kbps.
            mp3_44100_192 - output format, mp3 with 44.1kHz sample rate at 192kbps. Requires you to be subscribed to Creator tier or above.
            pcm_16000 - PCM format (S16LE) with 16kHz sample rate.
            pcm_22050 - PCM format (S16LE) with 22.05kHz sample rate.
            pcm_24000 - PCM format (S16LE) with 24kHz sample rate.
            pcm_44100 - PCM format (S16LE) with 44.1kHz sample rate. Requires you to be subscribed to Pro tier or above.
            ulaw_8000 - μ-law format (sometimes written mu-law, often approximated as u-law) with 8kHz sample rate. Note that this format is commonly used for Twilio audio inputs.

        auto_generate_text : typing.Optional[bool]
            Whether to automatically generate a text suitable for the voice description.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        VoicePreviewsResponseModel
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.text_to_voice.create_previews(
            voice_description="A sassy little squeaky mouse",
            text="Every act of kindness, no matter how small, carries value and can make a difference, as no gesture of goodwill is ever wasted.",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/text-to-voice/create-previews",
            method="POST",
            params={
                "output_format": output_format,
            },
            json={
                "voice_description": voice_description,
                "text": text,
                "auto_generate_text": auto_generate_text,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    VoicePreviewsResponseModel,
                    construct_type(
                        type_=VoicePreviewsResponseModel,  # type: ignore
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

    def create_voice_from_preview(
        self,
        *,
        voice_name: str,
        voice_description: str,
        generated_voice_id: str,
        labels: typing.Optional[typing.Dict[str, str]] = OMIT,
        played_not_selected_voice_ids: typing.Optional[typing.Sequence[str]] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Voice:
        """
        Create a voice from previously generated voice preview. This endpoint should be called after you fetched a generated_voice_id using /v1/text-to-voice/create-previews.

        Parameters
        ----------
        voice_name : str
            Name to use for the created voice.

        voice_description : str
            Description to use for the created voice.

        generated_voice_id : str
            The generated_voice_id to create, call POST /v1/voice-generation/generate-voice and fetch the generated_voice_id from the response header if don't have one yet.

        labels : typing.Optional[typing.Dict[str, str]]
            Optional, metadata to add to the created voice. Defaults to None.

        played_not_selected_voice_ids : typing.Optional[typing.Sequence[str]]
            List of voice ids that the user has played but not selected. Used for RLHF.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Voice
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.text_to_voice.create_voice_from_preview(
            voice_name="Little squeaky mouse",
            voice_description="A sassy little squeaky mouse",
            generated_voice_id="37HceQefKmEi3bGovXjL",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/text-to-voice/create-voice-from-preview",
            method="POST",
            json={
                "voice_name": voice_name,
                "voice_description": voice_description,
                "generated_voice_id": generated_voice_id,
                "labels": labels,
                "played_not_selected_voice_ids": played_not_selected_voice_ids,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    Voice,
                    construct_type(
                        type_=Voice,  # type: ignore
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


class AsyncTextToVoiceClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def create_previews(
        self,
        *,
        voice_description: str,
        text: str,
        output_format: typing.Optional[TextToVoiceCreatePreviewsRequestOutputFormat] = None,
        auto_generate_text: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> VoicePreviewsResponseModel:
        """
        Generate a custom voice based on voice description. This method returns a list of voice previews. Each preview has a generated_voice_id and a sample of the voice as base64 encoded mp3 audio. If you like the a voice previewand want to create the voice call /v1/text-to-voice/create-voice-from-preview with the generated_voice_id to create the voice.

        Parameters
        ----------
        voice_description : str
            Description to use for the created voice.

        text : str
            Text to generate, text length has to be between 100 and 1000.

        output_format : typing.Optional[TextToVoiceCreatePreviewsRequestOutputFormat]
            Output format of the generated audio. Must be one of:
            mp3_22050_32 - output format, mp3 with 22.05kHz sample rate at 32kbps.
            mp3_44100_32 - output format, mp3 with 44.1kHz sample rate at 32kbps.
            mp3_44100_64 - output format, mp3 with 44.1kHz sample rate at 64kbps.
            mp3_44100_96 - output format, mp3 with 44.1kHz sample rate at 96kbps.
            mp3_44100_128 - default output format, mp3 with 44.1kHz sample rate at 128kbps.
            mp3_44100_192 - output format, mp3 with 44.1kHz sample rate at 192kbps. Requires you to be subscribed to Creator tier or above.
            pcm_16000 - PCM format (S16LE) with 16kHz sample rate.
            pcm_22050 - PCM format (S16LE) with 22.05kHz sample rate.
            pcm_24000 - PCM format (S16LE) with 24kHz sample rate.
            pcm_44100 - PCM format (S16LE) with 44.1kHz sample rate. Requires you to be subscribed to Pro tier or above.
            ulaw_8000 - μ-law format (sometimes written mu-law, often approximated as u-law) with 8kHz sample rate. Note that this format is commonly used for Twilio audio inputs.

        auto_generate_text : typing.Optional[bool]
            Whether to automatically generate a text suitable for the voice description.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        VoicePreviewsResponseModel
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.text_to_voice.create_previews(
                voice_description="A sassy little squeaky mouse",
                text="Every act of kindness, no matter how small, carries value and can make a difference, as no gesture of goodwill is ever wasted.",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/text-to-voice/create-previews",
            method="POST",
            params={
                "output_format": output_format,
            },
            json={
                "voice_description": voice_description,
                "text": text,
                "auto_generate_text": auto_generate_text,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    VoicePreviewsResponseModel,
                    construct_type(
                        type_=VoicePreviewsResponseModel,  # type: ignore
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

    async def create_voice_from_preview(
        self,
        *,
        voice_name: str,
        voice_description: str,
        generated_voice_id: str,
        labels: typing.Optional[typing.Dict[str, str]] = OMIT,
        played_not_selected_voice_ids: typing.Optional[typing.Sequence[str]] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Voice:
        """
        Create a voice from previously generated voice preview. This endpoint should be called after you fetched a generated_voice_id using /v1/text-to-voice/create-previews.

        Parameters
        ----------
        voice_name : str
            Name to use for the created voice.

        voice_description : str
            Description to use for the created voice.

        generated_voice_id : str
            The generated_voice_id to create, call POST /v1/voice-generation/generate-voice and fetch the generated_voice_id from the response header if don't have one yet.

        labels : typing.Optional[typing.Dict[str, str]]
            Optional, metadata to add to the created voice. Defaults to None.

        played_not_selected_voice_ids : typing.Optional[typing.Sequence[str]]
            List of voice ids that the user has played but not selected. Used for RLHF.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Voice
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.text_to_voice.create_voice_from_preview(
                voice_name="Little squeaky mouse",
                voice_description="A sassy little squeaky mouse",
                generated_voice_id="37HceQefKmEi3bGovXjL",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/text-to-voice/create-voice-from-preview",
            method="POST",
            json={
                "voice_name": voice_name,
                "voice_description": voice_description,
                "generated_voice_id": generated_voice_id,
                "labels": labels,
                "played_not_selected_voice_ids": played_not_selected_voice_ids,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    Voice,
                    construct_type(
                        type_=Voice,  # type: ignore
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
