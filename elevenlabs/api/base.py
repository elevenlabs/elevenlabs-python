import json
import os
from typing import Optional, Sequence

import requests  # type: ignore
from pydantic import BaseModel

from .error import (
    APIError,
    AuthorizationError,
    RateLimitError,
    UnauthenticatedRateLimitError,
)

api_base_url_v1 = os.environ.get("ELEVEN_BASE_URL", "https://api.elevenlabs.io/v1")


class API(BaseModel):
    class ConfigDict:
        # Parse enum to strings when converting to dict
        use_enum_values = True
        # Validate fields when setting manually
        validate_assignment = True
        # Allows having a field called `model_id` in the class
        protected_namespaces = ()

    @staticmethod
    def request(url: str, method: str, api_key: Optional[str] = None, **kwargs):
        api_key = api_key or os.environ.get("ELEVEN_API_KEY")
        headers = {"xi-api-key": api_key}

        if method == "get":
            response = requests.get(url, headers=headers, **kwargs)
        elif method == "post":
            response = requests.post(url, headers=headers, **kwargs)
        elif method == "delete":
            response = requests.delete(url, headers=headers, **kwargs)
        else:
            raise ValueError(f"Invalid request method {method}")

        status_code = response.status_code

        if status_code == 200:
            return response

        # Parse the error message and status
        error = json.loads(response.text)
        message, status = "", ""
        if "detail" in error:
            detail = error["detail"]
            if isinstance(error, dict):
                message = detail.get("message", "")
                status = detail.get("status", "")
        else:
            message = str(error)
            status = str(response.status_code)

        # Raise the appropriate error
        if status_code == 401:
            if status == "quota_exceeded":
                if api_key is None:
                    raise UnauthenticatedRateLimitError(message)
                else:
                    raise RateLimitError(message)
            elif status == "needs_authorization":
                raise AuthorizationError(message)

        raise APIError(message, status)

    @staticmethod
    def get(url: str, *args, **kwargs):
        return API.request(url, method="get", *args, **kwargs)  # type: ignore

    @staticmethod
    def post(url: str, *args, **kwargs):
        return API.request(url, method="post", *args, **kwargs)  # type: ignore

    @staticmethod
    def delete(url: str, *args, **kwargs):
        return API.request(url, method="delete", *args, **kwargs)  # type: ignore


class Listable:
    @property
    def items(self) -> Sequence:
        raise NotImplementedError

    def __getitem__(self, idx: int):
        return self.items[idx]

    def __iter__(self):
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)
