import json
from typing import Dict, Optional

import requests  # type: ignore


class HTTPError:
    status: str
    message: str
    additional_info: Optional[Dict] = None

    def __init__(self, response: requests.Response):
        detail = json.loads(response.text)["detail"]
        self.message = detail["message"]
        self.status = detail["status"]
        self.additional_info = detail.get("additional_info", None)


class APIError(Exception):
    message: Optional[str] = None

    def __init__(self, http_error: HTTPError):
        self.message = self.message or http_error.message
        self.http_error = http_error
        super().__init__(self.message)


class AuthorizationError(APIError):
    message: str = "This endpoint requires a valid API key, but none was found."


class RateLimitError(APIError):
    message: str = (
        "You have reached your subscription limit. Please purchase another plan to continue."
    )



class UnauthenticatedRateLimitError(RateLimitError):
    message: str = (
        "Thanks for trying out our speech synthesis! You have reached the limit of"
        " unauthenticated requests. You can continue, for free, by setting a valid API"
        " key."
    )
