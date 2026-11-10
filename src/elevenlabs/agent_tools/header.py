from __future__ import annotations

import typing

from ._wire import deep_copy

HeaderWire = typing.Union[str, typing.Dict[str, str]]


class Header:
    """The value of a webhook request header."""

    def __init__(self, model: HeaderWire) -> None:
        # Use the static constructors. The model is the header value in wire format.
        self._model = model

    @staticmethod
    def value(text: str) -> Header:
        """A fixed value."""
        return Header(text)

    @staticmethod
    def secret(secret_id: str) -> Header:
        """A secret from the workspace's secret store, so the value never appears in the config."""
        return Header({"secret_id": secret_id})

    @staticmethod
    def variable(name: str) -> Header:
        """The value of a dynamic variable when the tool runs."""
        return Header({"variable_name": name})

    @staticmethod
    def env_var(label: str) -> Header:
        """A workspace environment variable, by label."""
        return Header({"env_var_label": label})

    def to_wire(self) -> HeaderWire:
        """The header value in API wire format."""
        return typing.cast(HeaderWire, deep_copy(self._model))

    def __repr__(self) -> str:
        return f"Header({self._model!r})"


class AuthConnection:
    """The auth connection a webhook tool authenticates with."""

    def __init__(self, model: typing.Dict[str, str]) -> None:
        # Use the static constructors.
        self._model = model

    @staticmethod
    def id(auth_connection_id: str) -> AuthConnection:
        """An auth connection from the workspace's store, by id."""
        return AuthConnection({"auth_connection_id": auth_connection_id})

    @staticmethod
    def env_var(label: str) -> AuthConnection:
        """An environment variable of type auth connection, by label, resolved for the current environment."""
        return AuthConnection({"env_var_label": label})

    def to_wire(self) -> typing.Dict[str, str]:
        """The auth connection in API wire format."""
        return dict(self._model)

    def __repr__(self) -> str:
        return f"AuthConnection({self._model!r})"
