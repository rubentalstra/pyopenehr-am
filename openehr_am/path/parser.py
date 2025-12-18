"""openEHR path parser (MVP).

Public entrypoint: :func:`parse_path`.

This is a parsing-layer module: it must never raise for invalid path input.
Instead it returns `Issue` objects.

# Spec: https://specifications.openehr.org/releases/BASE/latest/architecture_overview.html#_paths
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan
from openehr_am.path.ast import Path, PathPredicate, PathSegment
from openehr_am.validation.issue import Issue, Severity


class _ParseError(Exception):
    def __init__(
        self, message: str, *, line: int | None = None, col: int | None = None
    ):
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col


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


def _is_ident_start(ch: str) -> bool:
    return ch.isalpha() or ch == "_"


def _is_ident_cont(ch: str) -> bool:
    return ch.isalnum() or ch == "_"


class _Parser:
    def __init__(self, text: str, *, filename: str | None):
        self._c = _Cursor(text)
        self._filename = filename

    def _span(
        self,
        *,
        start_line: int,
        start_col: int,
        end_line: int,
        end_col: int,
    ) -> SourceSpan:
        return SourceSpan(
            file=self._filename,
            start_line=start_line,
            start_col=start_col,
            end_line=end_line,
            end_col=end_col,
        )

    def parse(self) -> Path:
        if self._c.eof():
            raise _ParseError("empty path", line=1, col=1)

        if self._c.peek() != "/":
            raise _ParseError(
                "path must start with '/'", line=self._c.line, col=self._c.col
            )

        path_start_line, path_start_col = self._c.line, self._c.col
        self._c.advance()  # '/'

        if self._c.eof():
            # '/' alone is not accepted (use '/definition' for root).
            raise _ParseError(
                "path has no segments", line=self._c.line, col=self._c.col
            )

        segments: list[PathSegment] = []

        while True:
            if self._c.peek() == "/":
                raise _ParseError(
                    "empty path segment", line=self._c.line, col=self._c.col
                )

            seg = self._parse_segment()
            segments.append(seg)

            if self._c.eof():
                break

            if self._c.peek() != "/":
                raise _ParseError(
                    f"unexpected character {self._c.peek()!r}",
                    line=self._c.line,
                    col=self._c.col,
                )

            # Consume '/' and continue; disallow trailing '/'.
            self._c.advance()
            if self._c.eof():
                raise _ParseError(
                    "path must not end with '/'", line=self._c.line, col=self._c.col
                )

        path_end_line, path_end_col = self._c.line, self._c.col

        # Optional leading '/definition' is not part of the semantic segments.
        if (
            segments
            and segments[0].name == "definition"
            and segments[0].predicate is None
        ):
            segments = segments[1:]

        return Path(
            segments=tuple(segments),
            span=self._span(
                start_line=path_start_line,
                start_col=path_start_col,
                end_line=path_end_line,
                end_col=path_end_col,
            ),
        )

    def _parse_segment(self) -> PathSegment:
        start_line, start_col = self._c.line, self._c.col

        name = self._parse_ident()

        predicate: PathPredicate | None = None
        if self._c.peek() == "[":
            predicate = self._parse_predicate()

        end_line, end_col = self._c.line, self._c.col
        return PathSegment(
            name=name,
            predicate=predicate,
            span=self._span(
                start_line=start_line,
                start_col=start_col,
                end_line=end_line,
                end_col=end_col,
            ),
        )

    def _parse_ident(self) -> str:
        ch = self._c.peek()
        if not _is_ident_start(ch):
            raise _ParseError(
                "expected attribute name",
                line=self._c.line,
                col=self._c.col,
            )

        start = self._c.i
        self._c.advance()
        while True:
            ch2 = self._c.peek()
            if not ch2 or not _is_ident_cont(ch2):
                break
            self._c.advance()

        return self._c.text[start : self._c.i]

    def _parse_predicate(self) -> PathPredicate:
        if self._c.peek() != "[":
            raise _ParseError("internal error: expected '['")

        start_line, start_col = self._c.line, self._c.col
        self._c.advance()  # '['

        pred_start_line, pred_start_col = self._c.line, self._c.col

        buf: list[str] = []
        while True:
            if self._c.eof():
                raise _ParseError(
                    "unterminated predicate", line=self._c.line, col=self._c.col
                )

            ch = self._c.peek()
            if ch == "]":
                break
            if ch == "/":
                raise _ParseError(
                    "'/' not allowed inside predicate",
                    line=self._c.line,
                    col=self._c.col,
                )

            buf.append(self._c.advance())

        if not buf:
            raise _ParseError(
                "empty predicate", line=pred_start_line, col=pred_start_col
            )

        # Consume closing ']'.
        self._c.advance()

        end_line, end_col = self._c.line, self._c.col
        pred_text = "".join(buf)
        return PathPredicate(
            text=pred_text,
            span=self._span(
                start_line=start_line,
                start_col=start_col,
                end_line=end_line,
                end_col=end_col,
            ),
        )


def _strip_wrapping_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    return value


def parse_path(
    text: str, *, filename: str | None = None
) -> tuple[Path | None, list[Issue]]:
    """Parse openEHR path text into a syntax AST.

    Args:
        text: A single openEHR path (often starting with `/definition`).
        filename: Optional filename used for source spans and Issues.

    Returns:
        (path, issues). On parse failure, path is None and issues contains at
        least one ERROR Issue with code PATH900.

    Notes:
        - This function never raises for invalid path input.
        - A leading `/definition` segment is stripped from the returned AST.

    # Spec: https://specifications.openehr.org/releases/BASE/latest/architecture_overview.html#_paths
    """

    if not isinstance(text, str):
        raise TypeError("parse_path expects 'text' to be str")

    raw = text
    stripped = _strip_wrapping_quotes(text.strip())

    try:
        parser = _Parser(stripped, filename=filename)
        node = parser.parse()
        return node, []
    except _ParseError as e:
        issue = Issue(
            code="PATH900",
            severity=Severity.ERROR,
            message=e.message,
            file=filename,
            line=e.line,
            col=e.col,
            path=raw,
        )
        return None, [issue]
