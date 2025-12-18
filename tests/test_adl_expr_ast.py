import dataclasses

from openehr_am.adl.expr_ast import (
    BinaryOp,
    ExprBinary,
    ExprBoolean,
    ExprCall,
    ExprInteger,
    ExprName,
    ExprNull,
    ExprString,
    ExprUnary,
    UnaryOp,
)
from openehr_am.antlr.span import SourceSpan


def test_expr_ops_are_string_enums() -> None:
    assert str(UnaryOp.NOT) == "not"
    assert str(BinaryOp.AND) == "and"
    assert str(BinaryOp.EQ) == "="
    assert str(BinaryOp.ADD) == "+"


def test_expr_nodes_capture_spans() -> None:
    name_span = SourceSpan(
        file="x.adl", start_line=10, start_col=5, end_line=10, end_col=7
    )
    lit_span = SourceSpan(
        file="x.adl", start_line=10, start_col=11, end_line=10, end_col=12
    )
    op_span = SourceSpan(
        file="x.adl", start_line=10, start_col=8, end_line=10, end_col=10
    )

    left = ExprName(name="a", span=name_span)
    right = ExprInteger(value=1, span=lit_span)

    expr = ExprBinary(
        left=left, op=BinaryOp.ADD, right=right, span=None, op_span=op_span
    )

    assert expr.left is left
    assert expr.right is right
    assert expr.op is BinaryOp.ADD
    assert expr.op_span == op_span


def test_expr_nodes_are_frozen() -> None:
    n = ExprName(name="x")

    try:
        n.name = "y"  # type: ignore[misc]
    except dataclasses.FrozenInstanceError:
        pass
    else:
        raise AssertionError("Expected dataclasses.FrozenInstanceError")


def test_expr_call_default_args_is_empty_tuple() -> None:
    call = ExprCall(callee=ExprName(name="f"))
    assert call.args == ()


def test_expr_unary_and_null_smoke() -> None:
    expr = ExprUnary(op=UnaryOp.MINUS, operand=ExprInteger(value=2), op_span=None)
    assert expr.op is UnaryOp.MINUS

    null = ExprNull(span=None)
    assert null.span is None


def test_expr_string_and_boolean_smoke() -> None:
    s = ExprString(value="hello")
    b = ExprBoolean(value=True)
    assert s.value == "hello"
    assert b.value is True
