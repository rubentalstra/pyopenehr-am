from openehr_am.adl import parse_expr
from openehr_am.adl.expr_ast import (
    BinaryOp,
    ExprBinary,
    ExprBoolean,
    ExprCall,
    ExprInteger,
    ExprName,
    ExprUnary,
    UnaryOp,
)


def test_parse_expr_operator_precedence_mul_over_add() -> None:
    expr, issues = parse_expr("1 + 2 * 3", filename="x.adl")

    assert issues == []
    assert isinstance(expr, ExprBinary)
    assert expr.op is BinaryOp.ADD

    assert isinstance(expr.left, ExprInteger)
    assert expr.left.value == 1

    assert isinstance(expr.right, ExprBinary)
    assert expr.right.op is BinaryOp.MUL
    assert isinstance(expr.right.left, ExprInteger)
    assert expr.right.left.value == 2
    assert isinstance(expr.right.right, ExprInteger)
    assert expr.right.right.value == 3


def test_parse_expr_parentheses_override_precedence() -> None:
    expr, issues = parse_expr("(1 + 2) * 3")

    assert issues == []
    assert isinstance(expr, ExprBinary)
    assert expr.op is BinaryOp.MUL
    assert isinstance(expr.left, ExprBinary)
    assert expr.left.op is BinaryOp.ADD


def test_parse_expr_unary_and_boolean_ops() -> None:
    expr, issues = parse_expr("not true or false")

    assert issues == []
    assert isinstance(expr, ExprBinary)
    assert expr.op is BinaryOp.OR

    assert isinstance(expr.left, ExprUnary)
    assert expr.left.op is UnaryOp.NOT
    assert isinstance(expr.left.operand, ExprBoolean)
    assert expr.left.operand.value is True

    assert isinstance(expr.right, ExprBoolean)
    assert expr.right.value is False


def test_parse_expr_call_with_args() -> None:
    expr, issues = parse_expr("f(1, x)")

    assert issues == []
    assert isinstance(expr, ExprCall)
    assert isinstance(expr.callee, ExprName)
    assert expr.callee.name == "f"

    assert len(expr.args) == 2
    assert isinstance(expr.args[0], ExprInteger)
    assert expr.args[0].value == 1
    assert isinstance(expr.args[1], ExprName)
    assert expr.args[1].name == "x"


def test_parse_expr_tracks_spans_with_offsets() -> None:
    expr, issues = parse_expr("a + 1", filename="x.adl", start_line=10, start_col=5)

    assert issues == []
    assert isinstance(expr, ExprBinary)
    assert expr.op is BinaryOp.ADD

    assert expr.op_span is not None
    assert expr.op_span.start_line == 10
    assert expr.op_span.start_col == 7
    assert expr.op_span.end_col == 7


def test_parse_expr_invalid_input_returns_issue() -> None:
    expr, issues = parse_expr("1 +", filename="bad.adl", start_line=3, start_col=1)

    assert expr is None
    assert issues
    assert issues[0].code == "ADL001"
    assert issues[0].file == "bad.adl"
    assert issues[0].line == 3
    assert issues[0].col is not None
