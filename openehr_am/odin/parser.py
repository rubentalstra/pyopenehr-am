"""ODIN parser (MVP).

Public entrypoint: :func:`parse_odin`.

This is a parsing-layer module: it must never raise for invalid ODIN input.
Instead, it returns `Issue` objects.

# Spec: https://specifications.openehr.org/releases/LANG/latest/odin.html
"""

from dataclasses import dataclass
from enum import StrEnum

from openehr_am.antlr.span import SourceSpan
from openehr_am.odin.ast import (
    OdinBoolean,
    OdinInteger,
    OdinKeyedList,
    OdinKeyedListItem,
    OdinList,
    OdinNode,
    OdinNull,
    OdinObject,
    OdinObjectItem,
    OdinPrimitive,
    OdinReal,
    OdinString,
)
from openehr_am.validation.issue import Issue, Severity


class _TokKind(StrEnum):
    LT = "<"
    GT = ">"
    LBRACK = "["
    RBRACK = "]"
    LPAREN = "("
    RPAREN = ")"
    EQ = "="
    COMMA = ","
    SEMI = ";"
    IDENT = "IDENT"
    STRING = "STRING"
    NUMBER = "NUMBER"
    EOF = "EOF"


@dataclass(slots=True, frozen=True)
class _Token:
    kind: _TokKind
    text: str
    line: int
    col: int
    end_line: int
    end_col: int

    def span(self, *, filename: str | None) -> SourceSpan:
        return SourceSpan(
            file=filename,
            start_line=self.line,
            start_col=self.col,
            end_line=self.end_line,
            end_col=self.end_col,
        )


@dataclass(slots=True)
class _Cursor:
    text: str
    i: int = 0
    line: int = 1
    col: int = 1

    def eof(self) -> bool:
        return self.i >= len(self.text)

    def peek(self) -> str:
        if self.eof():
            return ""
        return self.text[self.i]

    def advance(self) -> str:
        ch = self.peek()
        if not ch:
            return ""
        self.i += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch


class _ParseError(Exception):
    def __init__(
        self, message: str, *, line: int | None = None, col: int | None = None
    ):
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col


class _Lexer:
    def __init__(self, text: str):
        self._c = _Cursor(text)

    def next_token(self) -> _Token:
        self._skip_ws_and_comments()

        if self._c.eof():
            return _Token(
                kind=_TokKind.EOF,
                text="",
                line=self._c.line,
                col=self._c.col,
                end_line=self._c.line,
                end_col=self._c.col,
            )

        ch = self._c.peek()
        start_line, start_col = self._c.line, self._c.col

        # Single-character punctuation.
        if ch in "<>[]=(),;":
            self._c.advance()
            kind = _TokKind(ch)
            return _Token(
                kind=kind,
                text=ch,
                line=start_line,
                col=start_col,
                end_line=self._c.line,
                end_col=self._c.col - 1,
            )

        if ch == '"':
            return self._lex_string()

        if ch.isalpha() or ch == "_":
            return self._lex_ident()

        if ch.isdigit() or ch in "+-":
            return self._lex_number()

        # Unknown character.
        self._c.advance()
        raise _ParseError(
            f"Unexpected character {ch!r}",
            line=start_line,
            col=start_col,
        )

    def _skip_ws_and_comments(self) -> None:
        while not self._c.eof():
            ch = self._c.peek()
            if ch.isspace():
                self._c.advance()
                continue

            # Comments start with "--" and run to end-of-line.
            if ch == "-" and self._peek2() == "--":
                self._c.advance()
                self._c.advance()
                while not self._c.eof() and self._c.peek() != "\n":
                    self._c.advance()
                continue

            break

    def _peek2(self) -> str:
        if self._c.i + 1 >= len(self._c.text):
            return ""
        return self._c.text[self._c.i : self._c.i + 2]

    def _lex_ident(self) -> _Token:
        start_line, start_col = self._c.line, self._c.col
        buf: list[str] = []
        while not self._c.eof():
            ch = self._c.peek()
            if ch.isalnum() or ch == "_":
                buf.append(self._c.advance())
                continue
            break

        text = "".join(buf)
        return _Token(
            kind=_TokKind.IDENT,
            text=text,
            line=start_line,
            col=start_col,
            end_line=self._c.line,
            end_col=self._c.col - 1,
        )

    def _lex_string(self) -> _Token:
        start_line, start_col = self._c.line, self._c.col
        assert self._c.advance() == '"'

        buf: list[str] = []
        while not self._c.eof():
            ch = self._c.advance()
            if ch == "":
                break
            if ch == '"':
                # End.
                return _Token(
                    kind=_TokKind.STRING,
                    text="".join(buf),
                    line=start_line,
                    col=start_col,
                    end_line=self._c.line,
                    end_col=self._c.col - 1,
                )
            if ch == "\\":
                if self._c.eof():
                    raise _ParseError(
                        "Unterminated escape sequence in string",
                        line=self._c.line,
                        col=self._c.col,
                    )
                esc = self._c.advance()
                match esc:
                    case "n":
                        buf.append("\n")
                    case "r":
                        buf.append("\r")
                    case "t":
                        buf.append("\t")
                    case "\\":
                        buf.append("\\")
                    case '"':
                        buf.append('"')
                    case _:
                        raise _ParseError(
                            f"Illegal escape sequence \\{esc}",
                            line=self._c.line,
                            col=self._c.col - 1,
                        )
            else:
                buf.append(ch)

        raise _ParseError("Unterminated string literal", line=start_line, col=start_col)

    def _lex_number(self) -> _Token:
        start_line, start_col = self._c.line, self._c.col
        buf: list[str] = []

        # Optional leading sign.
        if self._c.peek() in "+-":
            buf.append(self._c.advance())

        saw_digit = False
        saw_dot = False
        saw_exp = False

        while not self._c.eof():
            ch = self._c.peek()
            if ch.isdigit():
                saw_digit = True
                buf.append(self._c.advance())
                continue

            if ch == "." and not saw_dot and not saw_exp:
                saw_dot = True
                buf.append(self._c.advance())
                continue

            if ch in "eE" and saw_digit and not saw_exp:
                saw_exp = True
                buf.append(self._c.advance())
                if self._c.peek() in "+-":
                    buf.append(self._c.advance())
                continue

            break

        if not saw_digit:
            raise _ParseError(
                f"Unexpected character {self._c.peek()!r}",
                line=start_line,
                col=start_col,
            )

        text = "".join(buf)
        return _Token(
            kind=_TokKind.NUMBER,
            text=text,
            line=start_line,
            col=start_col,
            end_line=self._c.line,
            end_col=self._c.col - 1,
        )


class _Parser:
    def __init__(self, text: str, *, filename: str | None):
        self._filename = filename
        self._lex = _Lexer(text)
        self._buf: list[_Token] = []

    def parse(self) -> OdinNode:
        # odin_text : attr_vals | object_value_block | keyed_object+ ;
        if self._peek(0).kind == _TokKind.LT:
            node = self._parse_object_value_block()
            self._expect(_TokKind.EOF)
            return node

        if self._peek(0).kind == _TokKind.LBRACK:
            items: list[OdinKeyedListItem] = []
            while self._peek(0).kind == _TokKind.LBRACK:
                items.append(self._parse_keyed_object_item())
            self._expect(_TokKind.EOF)
            return OdinKeyedList(items=tuple(items))

        # Implicit object document: attr_vals.
        obj = self._parse_attr_vals(until=_TokKind.EOF)
        self._expect(_TokKind.EOF)
        return obj

    def _parse_attr_vals(self, *, until: _TokKind) -> OdinObject:
        items: list[OdinObjectItem] = []

        while self._peek(0).kind != until:
            if self._peek(0).kind == _TokKind.SEMI:
                self._next()
                continue

            if self._peek(0).kind == _TokKind.EOF:
                break

            items.append(self._parse_attr_val())

            if self._peek(0).kind == _TokKind.SEMI:
                self._next()

        return OdinObject(items=tuple(items))

    def _parse_attr_val(self) -> OdinObjectItem:
        key_tok = self._expect(_TokKind.IDENT)
        key = key_tok.text
        self._expect(_TokKind.EQ)

        val = self._parse_object_block()

        return OdinObjectItem(
            key=key,
            value=val,
            key_span=key_tok.span(filename=self._filename),
        )

    def _parse_object_block(self) -> OdinNode:
        # object_block : object_value_block | object_reference_block ;
        # MVP: we only implement object_value_block.
        if self._peek(0).kind != _TokKind.LT:
            tok = self._peek(0)
            raise _ParseError(
                "Expected '<' to start an object block",
                line=tok.line,
                col=tok.col,
            )
        return self._parse_object_value_block()

    def _parse_object_value_block(self) -> OdinNode:
        # object_value_block : ( '(' type_id ')' )? '<' ( primitive_object | attr_vals? | keyed_object* ) '>'
        # MVP: ignore optional typing.
        if self._peek(0).kind == _TokKind.LPAREN:
            self._skip_type_annotation()

        lt = self._expect(_TokKind.LT)

        # Empty object.
        if self._peek(0).kind == _TokKind.GT:
            gt = self._next()
            return OdinObject(
                items=(),
                span=_span_between(lt, gt, filename=self._filename),
            )

        # Keyed list: [key] = <...> ...
        if self._peek(0).kind == _TokKind.LBRACK:
            items: list[OdinKeyedListItem] = []
            while self._peek(0).kind == _TokKind.LBRACK:
                items.append(self._parse_keyed_object_item())
                if self._peek(0).kind == _TokKind.SEMI:
                    self._next()

            gt = self._expect(_TokKind.GT)
            return OdinKeyedList(
                items=tuple(items),
                span=_span_between(lt, gt, filename=self._filename),
            )

        # Object: attr_vals or primitive_object.
        if self._peek(0).kind == _TokKind.IDENT and self._peek(1).kind == _TokKind.EQ:
            # Parse until we hit '>'
            obj = self._parse_attr_vals(until=_TokKind.GT)
            gt = self._expect(_TokKind.GT)
            return OdinObject(
                items=obj.items,
                span=_span_between(lt, gt, filename=self._filename),
            )

        # Primitive value or list of primitive values.
        first = self._parse_primitive_value()
        prims: list[OdinPrimitive] = [first]

        while self._peek(0).kind == _TokKind.COMMA:
            self._next()
            # list continuation '...' is part of full spec, not implemented.
            prims.append(self._parse_primitive_value())

        gt = self._expect(_TokKind.GT)
        if len(prims) == 1:
            # Keep the primitive node; attach the enclosing <> span.
            node = prims[0]
            return _with_span(node, _span_between(lt, gt, filename=self._filename))

        return OdinList(
            items=tuple(prims),
            span=_span_between(lt, gt, filename=self._filename),
        )

    def _parse_keyed_object_item(self) -> OdinKeyedListItem:
        self._expect(_TokKind.LBRACK)
        key = self._parse_primitive_value()
        self._expect(_TokKind.RBRACK)
        self._expect(_TokKind.EQ)
        value = self._parse_object_block()
        return OdinKeyedListItem(key=key, value=value)

    def _parse_primitive_value(self) -> OdinPrimitive:
        tok = self._peek(0)
        if tok.kind == _TokKind.STRING:
            t = self._next()
            return OdinString(value=t.text, span=t.span(filename=self._filename))

        if tok.kind == _TokKind.NUMBER:
            t = self._next()
            return _number_to_node(t, filename=self._filename)

        if tok.kind == _TokKind.IDENT:
            # Boolean literals are case-insensitive in ODIN.
            t = self._next()
            if t.text.casefold() == "true":
                return OdinBoolean(value=True, span=t.span(filename=self._filename))
            if t.text.casefold() == "false":
                return OdinBoolean(value=False, span=t.span(filename=self._filename))
            if t.text.casefold() == "null":
                return OdinNull(span=t.span(filename=self._filename))

            raise _ParseError(
                f"Unexpected identifier {t.text!r} where a primitive value is required",
                line=t.line,
                col=t.col,
            )

        raise _ParseError(
            f"Unexpected token {tok.kind.value!r} where a primitive value is required",
            line=tok.line,
            col=tok.col,
        )

    def _skip_type_annotation(self) -> None:
        # '(' type_id ')' where type_id is a fairly complex grammar.
        # MVP: we skip tokens until the matching ')'.
        self._expect(_TokKind.LPAREN)
        depth = 1
        while depth > 0:
            tok = self._next()
            if tok.kind == _TokKind.EOF:
                raise _ParseError(
                    "Unterminated type annotation",
                    line=tok.line,
                    col=tok.col,
                )
            if tok.kind == _TokKind.LPAREN:
                depth += 1
            elif tok.kind == _TokKind.RPAREN:
                depth -= 1

    def _peek(self, k: int) -> _Token:
        while len(self._buf) <= k:
            self._buf.append(self._lex.next_token())
        return self._buf[k]

    def _next(self) -> _Token:
        tok = self._peek(0)
        self._buf.pop(0)
        return tok

    def _expect(self, kind: _TokKind) -> _Token:
        tok = self._peek(0)
        if tok.kind != kind:
            raise _ParseError(
                f"Expected {kind.value!r} but found {tok.kind.value!r}",
                line=tok.line,
                col=tok.col,
            )
        return self._next()


def _span_between(start: _Token, end: _Token, *, filename: str | None) -> SourceSpan:
    return SourceSpan(
        file=filename,
        start_line=start.line,
        start_col=start.col,
        end_line=end.end_line,
        end_col=end.end_col,
    )


def _with_span(node: OdinPrimitive, span: SourceSpan) -> OdinPrimitive:
    match node:
        case OdinString(value=v):
            return OdinString(value=v, span=span)
        case OdinInteger(value=v):
            return OdinInteger(value=v, span=span)
        case OdinReal(value=v):
            return OdinReal(value=v, span=span)
        case OdinBoolean(value=v):
            return OdinBoolean(value=v, span=span)
        case OdinNull():
            return OdinNull(span=span)
        case _:
            return node


def _number_to_node(tok: _Token, *, filename: str | None) -> OdinPrimitive:
    text = tok.text
    span = tok.span(filename=filename)

    # Integer: digits with optional exponent. Real: contains dot or negative exponent.
    if any(ch in text for ch in "."):
        try:
            return OdinReal(value=float(text), span=span)
        except ValueError as e:
            raise _ParseError(str(e), line=tok.line, col=tok.col) from None

    if "e" in text.casefold():
        mantissa_s, exp_s = text.casefold().split("e", 1)
        mantissa = int(mantissa_s)
        exp = int(exp_s)
        if exp >= 0:
            return OdinInteger(value=mantissa * (10**exp), span=span)
        return OdinReal(value=mantissa * (10.0**exp), span=span)

    try:
        return OdinInteger(value=int(text), span=span)
    except ValueError as e:
        raise _ParseError(str(e), line=tok.line, col=tok.col) from None


def parse_odin(
    text: str, *, filename: str | None = None
) -> tuple[OdinNode | None, list[Issue]]:
    """Parse ODIN text into a syntax AST.

    Args:
        text: ODIN text fragment or document.
        filename: Optional filename used for source spans and Issues.

    Returns:
        (node, issues). On syntax failure, node is None and issues contains at
        least one ERROR Issue with code ODN100.

    Notes:
        - This function never raises for invalid ODIN input.
        - Type annotations, plug-in syntaxes, references, and most leaf types
          (dates, terms, intervals) are not yet implemented.

    # Spec: https://specifications.openehr.org/releases/LANG/latest/odin.html
    """

    if not isinstance(text, str):
        raise TypeError("parse_odin expects 'text' to be str")

    try:
        parser = _Parser(text, filename=filename)
        node = parser.parse()
        return node, []
    except _ParseError as e:
        issue = Issue(
            code="ODN100",
            severity=Severity.ERROR,
            message=e.message,
            file=filename,
            line=e.line,
            col=e.col,
        )
        return None, [issue]
