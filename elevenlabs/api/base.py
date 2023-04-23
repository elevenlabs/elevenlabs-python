import os
from typing import Optional

import requests  # type: ignore
from pydantic import BaseModel

api_base_url_v1 = "https://api.elevenlabs.io/v1"


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
            raise SystemExit(
                "Your quota is exceeded or your API key is invalid, please set a"
                " valid key: ELEVEN_API_KEY"
            )

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
