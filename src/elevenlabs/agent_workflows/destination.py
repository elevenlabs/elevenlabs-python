from __future__ import annotations

import typing

from ._wire import WireDict, deep_copy


class Destination:
    """Where a `transfer()` node hands the conversation off to."""

    def __init__(self, model: WireDict) -> None:
        # Use the static constructors. The model is the node fields the destination sets, in wire format.
        self._model = model

    @staticmethod
    def phone(phone_number: str) -> Destination:
        """A phone number in E.164 format."""
        return Destination(
            {"type": "phone_number", "transfer_destination": {"type": "phone", "phone_number": phone_number}}
        )

    @staticmethod
    def phone_variable(variable_name: str) -> Destination:
        """A phone number read from a dynamic variable at transfer time."""
        return Destination(
            {
                "type": "phone_number",
                "transfer_destination": {"type": "phone_dynamic_variable", "phone_number": variable_name},
            }
        )

    @staticmethod
    def sip(sip_uri: str) -> Destination:
        """A SIP URI."""
        return Destination({"type": "phone_number", "transfer_destination": {"type": "sip_uri", "sip_uri": sip_uri}})

    @staticmethod
    def sip_variable(variable_name: str) -> Destination:
        """A SIP URI read from a dynamic variable at transfer time."""
        return Destination(
            {
                "type": "phone_number",
                "transfer_destination": {"type": "sip_uri_dynamic_variable", "sip_uri": variable_name},
            }
        )

    @staticmethod
    def agent(agent_id: str, *, node_id: typing.Optional[str] = None) -> Destination:
        """Another ElevenLabs agent. `node_id` is the node in its workflow to start from."""
        model: WireDict = {"type": "standalone_agent", "agent_id": agent_id}
        if node_id is not None:
            model["node_id"] = node_id
        return Destination(model)

    def to_wire(self) -> WireDict:
        """The node fields this destination sets, in API wire format."""
        return typing.cast(WireDict, deep_copy(self._model))

    def __repr__(self) -> str:
        return f"Destination({self._model!r})"
