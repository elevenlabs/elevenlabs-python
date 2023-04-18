import os
from typing import Optional

import requests  # type: ignore
from pydantic import BaseModel

api_base_url_v1 = "https://api.elevenlabs.io/v1"


class API(BaseModel):
    @staticmethod
    def request(
        url: str,
        method: str,
        data: Optional[dict] = None,
        files=None,
        api_key: Optional[str] = None,
        stream: bool = False,
    ):
        headers = {
            "Accept": "application/json",
            "xi-api-key": api_key or os.environ.get("ELEVEN_API_KEY"),
        }

        if method == "get":
            response = requests.get(
                url, headers=headers, json=data, files=files, stream=stream
            )
        elif method == "post":
            response = requests.post(
                url, headers=headers, json=data, files=files, stream=stream
            )
        else:
            raise ValueError(f"Invalid request method {method}")

        try:
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError:
            if response.status_code == 401:
                raise requests.exceptions.RequestException(
                    "Your quota is exceeded or your API key is invalid, please set a"
                    " valid key: ELEVEN_API_KEY"
                )

    @staticmethod
    def get(url: str, *args, **kwargs):
        return API.request(url, method="get", *args, **kwargs)  # type: ignore

    @staticmethod
    def post(url: str, *args, **kwargs):
        return API.request(url, method="post", *args, **kwargs)  # type: ignore
