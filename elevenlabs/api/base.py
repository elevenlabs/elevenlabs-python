import json
import os
from typing import Optional

import requests  # type: ignore
from pydantic import BaseModel

api_base_url_v1 = "https://api.elevenlabs.io/v1"


class APIError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class QuotaExceededError(APIError):
    pass


class UnauthenticatedQuotaExceededError(APIError):
    def __init__(self):
        super().__init__(
            "Thanks for trying out our speech synthesis! You have reached the limit of"
            " unauthenticated requests. You can continue, for free, by setting a valid"
            " API key."
        )


class API(BaseModel):
    class Config:
        # Parse enum to strings when converting to dict
        use_enum_values = True
        # Validate fields when setting manually
        validate_assignment = True

    @staticmethod
    def request(url: str, method: str, api_key: Optional[str] = None, **kwargs):
        headers = {"xi-api-key": api_key or os.environ.get("ELEVEN_API_KEY")}

        if method == "get":
            response = requests.get(url, headers=headers, **kwargs)
        elif method == "post":
            response = requests.post(url, headers=headers, **kwargs)
        else:
            raise ValueError(f"Invalid request method {method}")

        if response.status_code == 401:
            message = json.loads(response.text)["detail"]["message"]
            if message.startswith("Thanks for trying out our speech synthesis!"):
                raise UnauthenticatedQuotaExceededError()
            else:
                raise QuotaExceededError(message)

        try:
            response.raise_for_status()
        except Exception as e:
            raise type(e)(response.reason, response.text)
        return response

    @staticmethod
    def get(url: str, *args, **kwargs):
        return API.request(url, method="get", *args, **kwargs)  # type: ignore

    @staticmethod
    def post(url: str, *args, **kwargs):
        return API.request(url, method="post", *args, **kwargs)  # type: ignore
