# This file was auto-generated by Fern from our API Definition.

import typing

from ....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ....core.request_options import RequestOptions
from ....types.embedding_model_enum import EmbeddingModelEnum
from ....types.rag_document_index_response_model import RagDocumentIndexResponseModel
from .raw_client import AsyncRawDocumentClient, RawDocumentClient

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class DocumentClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._raw_client = RawDocumentClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> RawDocumentClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        RawDocumentClient
        """
        return self._raw_client

    def compute_rag_index(
        self,
        documentation_id: str,
        *,
        model: EmbeddingModelEnum,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> RagDocumentIndexResponseModel:
        """
        In case the document is not RAG indexed, it triggers rag indexing task, otherwise it just returns the current status.

        Parameters
        ----------
        documentation_id : str
            The id of a document from the knowledge base. This is returned on document addition.

        model : EmbeddingModelEnum

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        RagDocumentIndexResponseModel
            Successful Response

        Examples
        --------
        from elevenlabs import ElevenLabs

        client = ElevenLabs(
            api_key="YOUR_API_KEY",
        )
        client.conversational_ai.knowledge_base.document.compute_rag_index(
            documentation_id="21m00Tcm4TlvDq8ikWAM",
            model="e5_mistral_7b_instruct",
        )
        """
        _response = self._raw_client.compute_rag_index(documentation_id, model=model, request_options=request_options)
        return _response.data


class AsyncDocumentClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._raw_client = AsyncRawDocumentClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> AsyncRawDocumentClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        AsyncRawDocumentClient
        """
        return self._raw_client

    async def compute_rag_index(
        self,
        documentation_id: str,
        *,
        model: EmbeddingModelEnum,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> RagDocumentIndexResponseModel:
        """
        In case the document is not RAG indexed, it triggers rag indexing task, otherwise it just returns the current status.

        Parameters
        ----------
        documentation_id : str
            The id of a document from the knowledge base. This is returned on document addition.

        model : EmbeddingModelEnum

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        RagDocumentIndexResponseModel
            Successful Response

        Examples
        --------
        import asyncio

        from elevenlabs import AsyncElevenLabs

        client = AsyncElevenLabs(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.conversational_ai.knowledge_base.document.compute_rag_index(
                documentation_id="21m00Tcm4TlvDq8ikWAM",
                model="e5_mistral_7b_instruct",
            )


        asyncio.run(main())
        """
        _response = await self._raw_client.compute_rag_index(
            documentation_id, model=model, request_options=request_options
        )
        return _response.data
