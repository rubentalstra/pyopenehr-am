"""ADL2 expression syntax-layer AST nodes.

This module defines a minimal, immutable syntax AST for expressions found in
ADL artefacts (e.g., the `rules` section).

Notes:
    - Syntax-layer only: no parsing, validation, or evaluation.
    - All nodes carry best-effort :class:`~openehr_am.antlr.span.SourceSpan`.

# Spec: https://specifications.openehr.org/releases/AM/latest/ADL2.html
"""

from dataclasses import dataclass
from enum import StrEnum

from openehr_am.antlr.span import SourceSpan


class UnaryOp(StrEnum):
    """Unary operator token (syntax layer)."""

    PLUS = "+"
    MINUS = "-"
    NOT = "not"


class BinaryOp(StrEnum):
    """Binary operator token (syntax layer)."""

    AND = "and"
    OR = "or"

    EQ = "="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="

    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


@dataclass(slots=True, frozen=True)
class ExprName:
    name: str
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class ExprString:
    value: str
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class ExprInteger:
    value: int
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class ExprReal:
    value: float
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class ExprBoolean:
    value: bool
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class ExprNull:
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class ExprUnary:
    op: UnaryOp
    operand: Expr
    span: SourceSpan | None = None
    op_span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class ExprBinary:
    left: Expr
    op: BinaryOp
    right: Expr
    span: SourceSpan | None = None
    op_span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class ExprCall:
    callee: Expr
    args: tuple[Expr, ...] = ()
    span: SourceSpan | None = None
    lpar_span: SourceSpan | None = None
    rpar_span: SourceSpan | None = None


# Union type for convenience in parsing/transform code.
Expr = (
    ExprName
    | ExprString
    | ExprInteger
    | ExprReal
    | ExprBoolean
    | ExprNull
    | ExprUnary
    | ExprBinary
    | ExprCall
)


__all__ = [
    "BinaryOp",
    "Expr",
    "ExprBinary",
    "ExprBoolean",
    "ExprCall",
    "ExprInteger",
    "ExprName",
    "ExprNull",
    "ExprReal",
    "ExprString",
    "ExprUnary",
    "UnaryOp",
]
