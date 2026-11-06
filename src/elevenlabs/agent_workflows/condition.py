from __future__ import annotations

import typing

from ..core.unchecked_base_model import construct_type
from ..types.workflow_edge_model_input_forward_condition import WorkflowEdgeModelInputForwardCondition
from ._wire import WireDict, deep_copy
from .expr import Expr


class Condition:
    """
    When an edge may be followed. A plain string passed to `when()` is shorthand for `Condition.llm()`, and an
    `Expr` is shorthand for `Condition.expr()`. `label` is shown on the edge in the workflow editor.
    """

    def __init__(self, model: WireDict) -> None:
        # Use the static constructors; the condition is kept in wire format.
        self._model = model

    @staticmethod
    def llm(condition: str, *, label: typing.Optional[str] = None) -> Condition:
        """Followed when the LLM judges `condition` to be true."""
        return Condition(_labelled({"type": "llm", "condition": condition}, label))

    @staticmethod
    def expr(expression: Expr, *, label: typing.Optional[str] = None) -> Condition:
        """Followed when `expression` evaluates to true."""
        return Condition(_labelled({"type": "expression", "expression": expression.to_wire()}, label))

    @staticmethod
    def always(*, label: typing.Optional[str] = None) -> Condition:
        """Always followed."""
        return Condition(_labelled({"type": "unconditional"}, label))

    @staticmethod
    def success(*, label: typing.Optional[str] = None) -> Condition:
        """Followed when every tool in a tool node succeeded."""
        return Condition(_labelled({"type": "result", "successful": True}, label))

    @staticmethod
    def failure(*, label: typing.Optional[str] = None) -> Condition:
        """Followed when any tool in a tool node failed."""
        return Condition(_labelled({"type": "result", "successful": False}, label))

    def to_model(self) -> WorkflowEdgeModelInputForwardCondition:
        """The condition as the SDK's generated edge condition model."""
        return typing.cast(
            WorkflowEdgeModelInputForwardCondition,
            construct_type(type_=WorkflowEdgeModelInputForwardCondition, object_=self.to_wire()),  # type: ignore[arg-type]
        )

    def to_wire(self) -> WireDict:
        """The condition in API wire format."""
        return typing.cast(WireDict, deep_copy(self._model))

    def __repr__(self) -> str:
        return f"Condition({self._model!r})"


ConditionInput = typing.Union[Condition, Expr, str]
"""A value accepted wherever a condition is expected."""


def to_condition(value: ConditionInput) -> Condition:
    if isinstance(value, Condition):
        return value
    if isinstance(value, Expr):
        return Condition.expr(value)
    return Condition.llm(value)


def _labelled(model: WireDict, label: typing.Optional[str]) -> WireDict:
    if label is not None:
        model["label"] = label
    return model
