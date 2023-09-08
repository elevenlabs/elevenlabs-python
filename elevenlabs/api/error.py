from typing import Optional


class APIError(Exception):
    message: str
    status: str
    display: Optional[str] = None

    def __init__(self, message: str, status: str = ""):
        self.message = message
        self.status = status
        self.display = self.display or message
        super().__init__(self.display)


class AuthorizationError(APIError):
    display: str = "This endpoint requires a valid API key, but none was found."


class RateLimitError(APIError):
    pass


class UnauthenticatedRateLimitError(RateLimitError):
    display: str = (
        "Thanks for trying out our speech synthesis! You have reached the limit of"
        " unauthenticated requests. You can continue, for free, by setting a valid API"
        " key."
    )
