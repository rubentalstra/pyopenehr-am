"""Minimal expression parser for ADL rules.

Public entrypoint: :func:`parse_expr`.

This is a parsing-layer module: it must never raise for invalid input.
Instead, it returns `Issue` objects.

Supported subset (syntax only):
- names
- literals: integer, real, string, true/false, null
- unary ops: +, -, not
- binary ops: *, /, +, -, comparisons (=, !=, <, <=, >, >=), and/or
- parentheses
- call expressions: callee(expr, ...)

No evaluation or semantic validation is performed.

# Spec: https://specifications.openehr.org/releases/AM/latest/ADL2.html
"""

from dataclasses import dataclass

from openehr_am.adl.expr_ast import (
    BinaryOp,
    Expr,
    ExprBinary,
    ExprBoolean,
    ExprCall,
    ExprInteger,
    ExprName,
    ExprNull,
    ExprReal,
    ExprString,
    ExprUnary,
    UnaryOp,
)
from openehr_am.antlr.span import SourceSpan
from openehr_am.validation.issue import Issue, Severity


def parse_expr(
    text: str,
    *,
    filename: str | None = None,
    start_line: int = 1,
    start_col: int = 1,
) -> tuple[Expr | None, list[Issue]]:
    """Parse an expression string into an expression syntax AST.

    Args:
        text: Expression text.
        filename: Optional filename for spans and Issues.
        start_line: 1-based starting line of `text` in the source file.
        start_col: 1-based starting column of `text` in the source file.

    Returns:
        (expr, issues). On failure, expr is None.

    Notes:
        Uses Issue code ADL001 for parse failures.

    # Spec: https://specifications.openehr.org/releases/AM/latest/ADL2.html
    """

    if not isinstance(text, str):
        raise TypeError("parse_expr expects 'text' to be str")

    try:
        tokens = _tokenize(
            text, filename=filename, start_line=start_line, start_col=start_col
        )
        parser = _Parser(tokens)
        expr = parser.parse_expression()

        tok = parser.peek()
        if tok.kind != "EOF":
            return None, [_issue_unexpected(tok, expected="end of input")]

        return expr, []
    except _ParseError as e:
        issue = Issue(
            code="ADL001",
            severity=Severity.ERROR,
            message=e.message,
            file=filename,
            line=e.line,
            col=e.col,
        )
        return None, [issue]


# ----------------
# Tokenization
# ----------------


@dataclass(slots=True, frozen=True)
class _Token:
    kind: str
    value: str
    span: SourceSpan


_SIMPLE_TOKENS: dict[str, str] = {
    "(": "LPAR",
    ")": "RPAR",
    ",": "COMMA",
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "=": "EQ",
    "<": "LT",
    ">": "GT",
}


def _tokenize(
    text: str,
    *,
    filename: str | None,
    start_line: int,
    start_col: int,
) -> list[_Token]:
    tokens: list[_Token] = []

    i = 0
    line = start_line
    col = start_col

    def advance(n: int = 1) -> None:
        nonlocal i, line, col
        for _ in range(n):
            if i >= len(text):
                return
            ch = text[i]
            i += 1
            if ch == "\n":
                line += 1
                col = 1
            else:
                col += 1

    def make_span(
        start_line_: int,
        start_col_: int,
        end_line_: int,
        end_col_: int,
    ) -> SourceSpan:
        return SourceSpan(
            file=filename,
            start_line=start_line_,
            start_col=start_col_,
            end_line=end_line_,
            end_col=end_col_,
        )

    while i < len(text):
        ch = text[i]

        # Whitespace
        if ch.isspace():
            advance(1)
            continue

        # Two-char operators
        if text.startswith("!=", i):
            s_line, s_col = line, col
            advance(2)
            tokens.append(_Token("NE", "!=", make_span(s_line, s_col, line, col - 1)))
            continue
        if text.startswith("<=", i):
            s_line, s_col = line, col
            advance(2)
            tokens.append(_Token("LE", "<=", make_span(s_line, s_col, line, col - 1)))
            continue
        if text.startswith(">=", i):
            s_line, s_col = line, col
            advance(2)
            tokens.append(_Token("GE", ">=", make_span(s_line, s_col, line, col - 1)))
            continue

        # Single char punctuation/operators
        kind = _SIMPLE_TOKENS.get(ch)
        if kind is not None:
            s_line, s_col = line, col
            advance(1)
            tokens.append(_Token(kind, ch, make_span(s_line, s_col, line, col - 1)))
            continue

        # String literal: "..." (minimal escapes for \" and \\)
        if ch == '"':
            s_line, s_col = line, col
            advance(1)  # opening quote
            buf: list[str] = []
            while i < len(text):
                c = text[i]
                if c == '"':
                    advance(1)
                    span = make_span(s_line, s_col, line, col - 1)
                    tokens.append(_Token("STRING", "".join(buf), span))
                    break
                if c == "\\":
                    # Escape
                    if i + 1 >= len(text):
                        raise _ParseError(
                            "Unterminated string literal", line=s_line, col=s_col
                        )
                    nxt = text[i + 1]
                    if nxt in {'"', "\\"}:
                        buf.append(nxt)
                        advance(2)
                        continue
                    # Unknown escape: keep literal next char.
                    buf.append(nxt)
                    advance(2)
                    continue

                buf.append(c)
                advance(1)
            else:
                raise _ParseError("Unterminated string literal", line=s_line, col=s_col)
            continue

        # Number: int or real
        if ch.isdigit():
            s_line, s_col = line, col
            start_i = i
            while i < len(text) and text[i].isdigit():
                advance(1)
            is_real = False
            if i < len(text) and text[i] == ".":
                # Real requires at least one digit after '.'
                if i + 1 < len(text) and text[i + 1].isdigit():
                    is_real = True
                    advance(1)  # '.'
                    while i < len(text) and text[i].isdigit():
                        advance(1)
            literal = text[start_i:i]
            span = make_span(s_line, s_col, line, col - 1)
            tokens.append(_Token("REAL" if is_real else "INT", literal, span))
            continue

        # Identifier / keywords
        if ch.isalpha() or ch == "_":
            s_line, s_col = line, col
            start_i = i
            while i < len(text) and (text[i].isalnum() or text[i] == "_"):
                advance(1)
            ident = text[start_i:i]
            span = make_span(s_line, s_col, line, col - 1)
            kw = ident.casefold()
            if kw == "and":
                tokens.append(_Token("AND", ident, span))
            elif kw == "or":
                tokens.append(_Token("OR", ident, span))
            elif kw == "not":
                tokens.append(_Token("NOT", ident, span))
            elif kw == "true":
                tokens.append(_Token("TRUE", ident, span))
            elif kw == "false":
                tokens.append(_Token("FALSE", ident, span))
            elif kw == "null":
                tokens.append(_Token("NULL", ident, span))
            else:
                tokens.append(_Token("IDENT", ident, span))
            continue

        raise _ParseError(f"Unexpected character: {ch!r}", line=line, col=col)

    eof_span = SourceSpan(
        file=filename,
        start_line=line,
        start_col=col,
        end_line=line,
        end_col=col,
    )
    tokens.append(_Token("EOF", "", eof_span))
    return tokens


# ----------------
# Parsing
# ----------------


class _ParseError(Exception):
    def __init__(self, message: str, *, line: int, col: int) -> None:
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col


def _issue_unexpected(tok: _Token, *, expected: str) -> Issue:
    return Issue(
        code="ADL001",
        severity=Severity.ERROR,
        message=f"Unexpected token {tok.kind!r}, expected {expected}",
        file=tok.span.file,
        line=tok.span.start_line,
        col=tok.span.start_col,
    )


class _Parser:
    def __init__(self, tokens: list[_Token]) -> None:
        self._tokens = tokens
        self._i = 0

    def peek(self) -> _Token:
        return self._tokens[self._i]

    def advance(self) -> _Token:
        tok = self._tokens[self._i]
        self._i = min(self._i + 1, len(self._tokens) - 1)
        return tok

    def match(self, *kinds: str) -> _Token | None:
        tok = self.peek()
        if tok.kind in kinds:
            self.advance()
            return tok
        return None

    def expect(self, kind: str) -> _Token:
        tok = self.peek()
        if tok.kind != kind:
            raise _ParseError(
                f"Unexpected token {tok.kind!r}, expected {kind}",
                line=tok.span.start_line,
                col=tok.span.start_col,
            )
        return self.advance()

    def parse_expression(self) -> Expr:
        return self._parse_or()

    def _parse_or(self) -> Expr:
        expr = self._parse_and()
        while (tok := self.match("OR")) is not None:
            right = self._parse_and()
            expr = ExprBinary(
                left=expr,
                op=BinaryOp.OR,
                right=right,
                op_span=tok.span,
                span=_merge_spans(expr, right),
            )
        return expr

    def _parse_and(self) -> Expr:
        expr = self._parse_comparison()
        while (tok := self.match("AND")) is not None:
            right = self._parse_comparison()
            expr = ExprBinary(
                left=expr,
                op=BinaryOp.AND,
                right=right,
                op_span=tok.span,
                span=_merge_spans(expr, right),
            )
        return expr

    def _parse_comparison(self) -> Expr:
        expr = self._parse_additive()
        while True:
            tok = self.match("EQ", "NE", "LT", "LE", "GT", "GE")
            if tok is None:
                break

            op = {
                "EQ": BinaryOp.EQ,
                "NE": BinaryOp.NE,
                "LT": BinaryOp.LT,
                "LE": BinaryOp.LE,
                "GT": BinaryOp.GT,
                "GE": BinaryOp.GE,
            }[tok.kind]
            right = self._parse_additive()
            expr = ExprBinary(
                left=expr,
                op=op,
                right=right,
                op_span=tok.span,
                span=_merge_spans(expr, right),
            )
        return expr

    def _parse_additive(self) -> Expr:
        expr = self._parse_multiplicative()
        while True:
            tok = self.match("PLUS", "MINUS")
            if tok is None:
                break
            op = BinaryOp.ADD if tok.kind == "PLUS" else BinaryOp.SUB
            right = self._parse_multiplicative()
            expr = ExprBinary(
                left=expr,
                op=op,
                right=right,
                op_span=tok.span,
                span=_merge_spans(expr, right),
            )
        return expr

    def _parse_multiplicative(self) -> Expr:
        expr = self._parse_unary()
        while True:
            tok = self.match("STAR", "SLASH")
            if tok is None:
                break
            op = BinaryOp.MUL if tok.kind == "STAR" else BinaryOp.DIV
            right = self._parse_unary()
            expr = ExprBinary(
                left=expr,
                op=op,
                right=right,
                op_span=tok.span,
                span=_merge_spans(expr, right),
            )
        return expr

    def _parse_unary(self) -> Expr:
        tok = self.match("PLUS", "MINUS", "NOT")
        if tok is not None:
            op = {
                "PLUS": UnaryOp.PLUS,
                "MINUS": UnaryOp.MINUS,
                "NOT": UnaryOp.NOT,
            }[tok.kind]
            operand = self._parse_unary()
            return ExprUnary(
                op=op,
                operand=operand,
                op_span=tok.span,
                span=_span_from(tok.span, operand.span),
            )

        return self._parse_call()

    def _parse_call(self) -> Expr:
        expr = self._parse_primary()
        while (lpar := self.match("LPAR")) is not None:
            args: list[Expr] = []
            if self.peek().kind != "RPAR":
                args.append(self.parse_expression())
                while self.match("COMMA") is not None:
                    args.append(self.parse_expression())
            rpar = self.expect("RPAR")

            call_span = _span_from(expr.span, rpar.span)
            expr = ExprCall(
                callee=expr,
                args=tuple(args),
                lpar_span=lpar.span,
                rpar_span=rpar.span,
                span=call_span,
            )

        return expr

    def _parse_primary(self) -> Expr:
        tok = self.peek()

        if tok.kind == "IDENT":
            self.advance()
            return ExprName(name=tok.value, span=tok.span)

        if tok.kind == "STRING":
            self.advance()
            return ExprString(value=tok.value, span=tok.span)

        if tok.kind == "INT":
            self.advance()
            try:
                value = int(tok.value)
            except ValueError as exc:
                raise _ParseError(
                    "Invalid integer literal",
                    line=tok.span.start_line,
                    col=tok.span.start_col,
                ) from exc
            return ExprInteger(value=value, span=tok.span)

        if tok.kind == "REAL":
            self.advance()
            try:
                value = float(tok.value)
            except ValueError as exc:
                raise _ParseError(
                    "Invalid real literal",
                    line=tok.span.start_line,
                    col=tok.span.start_col,
                ) from exc
            return ExprReal(value=value, span=tok.span)

        if tok.kind == "TRUE":
            self.advance()
            return ExprBoolean(value=True, span=tok.span)

        if tok.kind == "FALSE":
            self.advance()
            return ExprBoolean(value=False, span=tok.span)

        if tok.kind == "NULL":
            self.advance()
            return ExprNull(span=tok.span)

        if tok.kind == "LPAR":
            self.advance()
            expr = self.parse_expression()
            self.expect("RPAR")
            return expr

        raise _ParseError(
            f"Unexpected token {tok.kind!r}",
            line=tok.span.start_line,
            col=tok.span.start_col,
        )


def _merge_spans(left: Expr, right: Expr) -> SourceSpan | None:
    if left is None or right is None:
        return None
    if getattr(left, "span", None) is None or getattr(right, "span", None) is None:
        return None
    left_span = left.span
    right_span = right.span
    if left_span is None or right_span is None:
        return None
    return SourceSpan(
        file=left_span.file,
        start_line=left_span.start_line,
        start_col=left_span.start_col,
        end_line=right_span.end_line,
        end_col=right_span.end_col,
    )


def _span_from(start: SourceSpan | None, end: SourceSpan | None) -> SourceSpan | None:
    if start is None or end is None:
        return None
    return SourceSpan(
        file=start.file,
        start_line=start.start_line,
        start_col=start.start_col,
        end_line=end.end_line,
        end_col=end.end_col,
    )


__all__ = ["parse_expr"]
