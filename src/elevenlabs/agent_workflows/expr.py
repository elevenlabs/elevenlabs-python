from __future__ import annotations

import typing

from ..core.unchecked_base_model import construct_type
from ..types.ast_node_input import AstNodeInput
from ._wire import WireDict, deep_copy, to_wire

ExprInput = typing.Union["Expr", str, int, float, bool, None]
"""A value accepted wherever an expression is expected. Plain values become literals."""

LlmValueType = typing.Literal["boolean", "string", "integer", "number"]


class Expr:
    """
    A workflow expression, compiled to the API's expression AST.

    Examples
    --------
    Expr.any_of(Expr.variable("tier").eq("gold"), Expr.variable("orders").gte(10))
    """

    def __init__(self, node: WireDict) -> None:
        # Use the static constructors; the AST is kept in wire format.
        self._node = node

    @staticmethod
    def variable(name: str) -> Expr:
        """The value of a dynamic variable."""
        return Expr({"type": "dynamic_variable", "name": name})

    @staticmethod
    def literal(value: typing.Union[str, int, float, bool, None]) -> Expr:
        """A string, number, boolean or null literal."""
        if value is None:
            return Expr({"type": "null_literal"})
        if isinstance(value, bool):
            return Expr({"type": "boolean_literal", "value": value})
        if isinstance(value, str):
            return Expr({"type": "string_literal", "value": value})
        return Expr({"type": "number_literal", "value": value})

    @staticmethod
    def llm(
        description: str,
        *,
        type: LlmValueType = "boolean",
        enum: typing.Optional[typing.Sequence[str]] = None,
    ) -> Expr:
        """
        A value the LLM extracts from the conversation, described by `description`. `type` defaults to
        `"boolean"`; `enum` lists the allowed values of a `"string"`.

        Examples
        --------
        Expr.llm("How satisfied is the caller, from 1 to 10?", type="number").lt(5)
        """
        schema: WireDict = {"type": type, "description": description}
        if enum is not None:
            schema["enum"] = list(enum)
        return Expr({"type": "llm", "value_schema": schema})

    @staticmethod
    def all_of(*exprs: ExprInput) -> Expr:
        """True when every expression is true."""
        return Expr({"type": "and_operator", "children": [_to_ast(expr) for expr in exprs]})

    @staticmethod
    def any_of(*exprs: ExprInput) -> Expr:
        """True when at least one expression is true."""
        return Expr({"type": "or_operator", "children": [_to_ast(expr) for expr in exprs]})

    @staticmethod
    def if_else(condition: ExprInput, when_true: ExprInput, when_false: ExprInput) -> Expr:
        """`when_true` if `condition` is true, otherwise `when_false`."""
        return Expr(
            {
                "type": "conditional_operator",
                "condition": _to_ast(condition),
                "trueExpression": _to_ast(when_true),
                "falseExpression": _to_ast(when_false),
            }
        )

    @staticmethod
    def from_model(node: typing.Union[AstNodeInput, typing.Mapping[str, typing.Any]]) -> Expr:
        """Wraps an existing AST node: a generated `AstNodeInput` model, or a dict in wire format."""
        return Expr(to_wire(node))

    def eq(self, other: ExprInput) -> Expr:
        return self._binary("eq_operator", other)

    def neq(self, other: ExprInput) -> Expr:
        return self._binary("neq_operator", other)

    def gt(self, other: ExprInput) -> Expr:
        return self._binary("gt_operator", other)

    def gte(self, other: ExprInput) -> Expr:
        return self._binary("gte_operator", other)

    def lt(self, other: ExprInput) -> Expr:
        return self._binary("lt_operator", other)

    def lte(self, other: ExprInput) -> Expr:
        return self._binary("lte_operator", other)

    def add(self, other: ExprInput) -> Expr:
        return self._binary("add_operator", other)

    def sub(self, other: ExprInput) -> Expr:
        return self._binary("sub_operator", other)

    def mul(self, other: ExprInput) -> Expr:
        return self._binary("mul_operator", other)

    def div(self, other: ExprInput) -> Expr:
        return self._binary("div_operator", other)

    def to_model(self) -> AstNodeInput:
        """The expression as the SDK's generated `AstNodeInput` model."""
        return typing.cast(
            AstNodeInput,
            construct_type(type_=AstNodeInput, object_=self.to_wire()),  # type: ignore[arg-type]
        )

    def to_wire(self) -> WireDict:
        """The expression in API wire format."""
        return typing.cast(WireDict, deep_copy(self._node))

    def _binary(self, type: str, other: ExprInput) -> Expr:
        return Expr({"type": type, "left": self.to_wire(), "right": _to_ast(other)})

    def __repr__(self) -> str:
        return f"Expr({self._node!r})"


def _to_ast(value: ExprInput) -> WireDict:
    return value.to_wire() if isinstance(value, Expr) else Expr.literal(value).to_wire()
