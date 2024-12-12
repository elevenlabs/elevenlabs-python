# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from ..core.request_options import RequestOptions
from ..types.get_chapters_response import GetChaptersResponse
from ..core.jsonable_encoder import jsonable_encoder
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..types.chapter_response import ChapterResponse
from ..types.add_chapter_response_model import AddChapterResponseModel
from ..types.chapter_snapshots_response import ChapterSnapshotsResponse
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ChaptersClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get_all(
        self, project_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> GetChaptersResponse:
        """
        Returns a list of your chapters for a project together and its metadata.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetChaptersResponse
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.chapters.get_all(
            project_id="21m00Tcm4TlvDq8ikWAM",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    GetChaptersResponse,
                    construct_type(
                        type_=GetChaptersResponse,  # type: ignore
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

    def get(
        self, project_id: str, chapter_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ChapterResponse:
        """
        Returns information about a specific chapter.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ChapterResponse
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.chapters.get(
            project_id="21m00Tcm4TlvDq8ikWAM",
            chapter_id="21m00Tcm4TlvDq8ikWAM",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ChapterResponse,
                    construct_type(
                        type_=ChapterResponse,  # type: ignore
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

    def delete(
        self, project_id: str, chapter_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Optional[typing.Any]:
        """
        Delete a chapter by its chapter_id.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.chapters.delete(
            project_id="21m00Tcm4TlvDq8ikWAM",
            chapter_id="21m00Tcm4TlvDq8ikWAM",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    construct_type(
                        type_=typing.Optional[typing.Any],  # type: ignore
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

    def create(
        self,
        project_id: str,
        *,
        name: str,
        from_url: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AddChapterResponseModel:
        """
        Creates a new chapter either as blank or from a URL.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        name : str
            The name of the chapter, used for identification only.

        from_url : typing.Optional[str]
            An optional URL from which we will extract content to initialize the project. If this is set, 'from_url' must be null. If neither 'from_url' or 'from_document' are provided we will initialize the project as blank.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AddChapterResponseModel
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.chapters.create(
            project_id="21m00Tcm4TlvDq8ikWAM",
            name="name",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/add",
            method="POST",
            json={
                "name": name,
                "from_url": from_url,
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
                    AddChapterResponseModel,
                    construct_type(
                        type_=AddChapterResponseModel,  # type: ignore
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

    def convert(
        self, project_id: str, chapter_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Optional[typing.Any]:
        """
        Starts conversion of a specific chapter.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.chapters.convert(
            project_id="21m00Tcm4TlvDq8ikWAM",
            chapter_id="21m00Tcm4TlvDq8ikWAM",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}/convert",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    construct_type(
                        type_=typing.Optional[typing.Any],  # type: ignore
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

    def get_all_snapshots(
        self, project_id: str, chapter_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ChapterSnapshotsResponse:
        """
        Gets information about all the snapshots of a chapter, each snapshot corresponds can be downloaded as audio. Whenever a chapter is converted a snapshot will be automatically created.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ChapterSnapshotsResponse
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.chapters.get_all_snapshots(
            project_id="21m00Tcm4TlvDq8ikWAM",
            chapter_id="21m00Tcm4TlvDq8ikWAM",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}/snapshots",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ChapterSnapshotsResponse,
                    construct_type(
                        type_=ChapterSnapshotsResponse,  # type: ignore
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

    def stream_snapshot(
        self,
        project_id: str,
        chapter_id: str,
        chapter_snapshot_id: str,
        *,
        convert_to_mpeg: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Stream the audio from a chapter snapshot. Use `GET /v1/projects/{project_id}/chapters/{chapter_id}/snapshots` to return the chapter snapshots of a chapter.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        chapter_snapshot_id : str
            The chapter_snapshot_id of the chapter snapshot. You can query GET /v1/projects/{project_id}/chapters/{chapter_id}/snapshots to the all available snapshots for a chapter.

        convert_to_mpeg : typing.Optional[bool]
            Whether to convert the audio to mpeg format.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.chapters.stream_snapshot(
            project_id="21m00Tcm4TlvDq8ikWAM",
            chapter_id="21m00Tcm4TlvDq8ikWAM",
            chapter_snapshot_id="21m00Tcm4TlvDq8ikWAM",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}/snapshots/{jsonable_encoder(chapter_snapshot_id)}/stream",
            method="POST",
            json={
                "convert_to_mpeg": convert_to_mpeg,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
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


class AsyncChaptersClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get_all(
        self, project_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> GetChaptersResponse:
        """
        Returns a list of your chapters for a project together and its metadata.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetChaptersResponse
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.chapters.get_all(
                project_id="21m00Tcm4TlvDq8ikWAM",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    GetChaptersResponse,
                    construct_type(
                        type_=GetChaptersResponse,  # type: ignore
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

    async def get(
        self, project_id: str, chapter_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ChapterResponse:
        """
        Returns information about a specific chapter.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ChapterResponse
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.chapters.get(
                project_id="21m00Tcm4TlvDq8ikWAM",
                chapter_id="21m00Tcm4TlvDq8ikWAM",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ChapterResponse,
                    construct_type(
                        type_=ChapterResponse,  # type: ignore
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

    async def delete(
        self, project_id: str, chapter_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Optional[typing.Any]:
        """
        Delete a chapter by its chapter_id.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.chapters.delete(
                project_id="21m00Tcm4TlvDq8ikWAM",
                chapter_id="21m00Tcm4TlvDq8ikWAM",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    construct_type(
                        type_=typing.Optional[typing.Any],  # type: ignore
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

    async def create(
        self,
        project_id: str,
        *,
        name: str,
        from_url: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AddChapterResponseModel:
        """
        Creates a new chapter either as blank or from a URL.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        name : str
            The name of the chapter, used for identification only.

        from_url : typing.Optional[str]
            An optional URL from which we will extract content to initialize the project. If this is set, 'from_url' must be null. If neither 'from_url' or 'from_document' are provided we will initialize the project as blank.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AddChapterResponseModel
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.chapters.create(
                project_id="21m00Tcm4TlvDq8ikWAM",
                name="name",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/add",
            method="POST",
            json={
                "name": name,
                "from_url": from_url,
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
                    AddChapterResponseModel,
                    construct_type(
                        type_=AddChapterResponseModel,  # type: ignore
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

    async def convert(
        self, project_id: str, chapter_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Optional[typing.Any]:
        """
        Starts conversion of a specific chapter.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.chapters.convert(
                project_id="21m00Tcm4TlvDq8ikWAM",
                chapter_id="21m00Tcm4TlvDq8ikWAM",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}/convert",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    construct_type(
                        type_=typing.Optional[typing.Any],  # type: ignore
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

    async def get_all_snapshots(
        self, project_id: str, chapter_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ChapterSnapshotsResponse:
        """
        Gets information about all the snapshots of a chapter, each snapshot corresponds can be downloaded as audio. Whenever a chapter is converted a snapshot will be automatically created.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ChapterSnapshotsResponse
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.chapters.get_all_snapshots(
                project_id="21m00Tcm4TlvDq8ikWAM",
                chapter_id="21m00Tcm4TlvDq8ikWAM",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}/snapshots",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ChapterSnapshotsResponse,
                    construct_type(
                        type_=ChapterSnapshotsResponse,  # type: ignore
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

    async def stream_snapshot(
        self,
        project_id: str,
        chapter_id: str,
        chapter_snapshot_id: str,
        *,
        convert_to_mpeg: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Stream the audio from a chapter snapshot. Use `GET /v1/projects/{project_id}/chapters/{chapter_id}/snapshots` to return the chapter snapshots of a chapter.

        Parameters
        ----------
        project_id : str
            The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.

        chapter_id : str
            The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.

        chapter_snapshot_id : str
            The chapter_snapshot_id of the chapter snapshot. You can query GET /v1/projects/{project_id}/chapters/{chapter_id}/snapshots to the all available snapshots for a chapter.

        convert_to_mpeg : typing.Optional[bool]
            Whether to convert the audio to mpeg format.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.chapters.stream_snapshot(
                project_id="21m00Tcm4TlvDq8ikWAM",
                chapter_id="21m00Tcm4TlvDq8ikWAM",
                chapter_snapshot_id="21m00Tcm4TlvDq8ikWAM",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/projects/{jsonable_encoder(project_id)}/chapters/{jsonable_encoder(chapter_id)}/snapshots/{jsonable_encoder(chapter_snapshot_id)}/stream",
            method="POST",
            json={
                "convert_to_mpeg": convert_to_mpeg,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
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
