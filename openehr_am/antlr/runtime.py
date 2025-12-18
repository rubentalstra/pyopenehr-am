"""ANTLR4 runtime helpers.

This file is the narrow integration seam between our parsing layer and the
`antlr4-python3-runtime` package.

Responsibilities:
- Construct lexer/parser instances
- Convert ANTLR diagnostics into `Issue` objects (with best-effort line/col)

No semantic validation belongs here.
"""

import importlib
from typing import Any

from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.issue_collector import IssueCollector


def _extend_one(collector: IssueCollector, issue: Issue) -> None:
    collector.extend([issue])


class IssueCollectingErrorListener:
    """ANTLR error listener that records lexer/parser errors as Issues.

    Note:
        We intentionally avoid importing `antlr4` at module import time so the
        project remains importable/type-checkable in environments that do not
        have optional runtime dependencies installed. The ANTLR Python runtime
        accepts listeners via `addErrorListener()` using duck-typing.
    """

    def __init__(
        self,
        collector: IssueCollector,
        *,
        code: str = "ADL001",
        file: str | None = None,
    ) -> None:
        super().__init__()
        self._collector = collector
        self._code = code
        self._file = file

    def syntaxError(  # noqa: N802 (ANTLR API)
        self,
        recognizer: object,
        offendingSymbol: object | None,
        line: int,
        column: int,
        msg: str,
        e: Exception | None,
    ) -> None:
        del recognizer, offendingSymbol, e

        # ANTLR columns are 0-based; our Issue locations are 1-based.
        issue = Issue(
            code=self._code,
            severity=Severity.ERROR,
            message=msg,
            file=self._file,
            line=line,
            col=column + 1,
        )
        _extend_one(self._collector, issue)


def construct_lexer_parser(
    text: str,
    *,
    lexer_class: type[Any],
    parser_class: type[Any],
    issues: IssueCollector,
    file: str | None = None,
    issue_code: str = "ADL001",
) -> tuple[Any, Any]:
    """Construct lexer and parser and attach Issue-collecting error listeners.

    Args:
        text: Source text to parse.
        lexer_class: Generated ANTLR lexer class.
        parser_class: Generated ANTLR parser class.
        issues: Collector that receives `Issue` objects.
        file: Optional filename to attach to Issues.
        issue_code: Stable Issue code to use for ANTLR syntax errors.

    Returns:
        (lexer, parser)

    Note:
        Callers typically create a parse entrypoint and then inspect `issues`.
    """

    # Import dynamically to avoid a hard dependency at module import time.
    antlr4 = importlib.import_module("antlr4")
    InputStream = getattr(antlr4, "InputStream")
    CommonTokenStream = getattr(antlr4, "CommonTokenStream")

    listener = IssueCollectingErrorListener(issues, code=issue_code, file=file)

    lexer = lexer_class(InputStream(text))
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)

    token_stream = CommonTokenStream(lexer)

    parser = parser_class(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)

    return lexer, parser
