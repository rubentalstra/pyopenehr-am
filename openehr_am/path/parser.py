"""openEHR path parser (MVP).

Public entrypoint: :func:`parse_path`.

This is a parsing-layer module: it must never raise for invalid path input.
Instead it returns `Issue` objects.

Implementation note:
    This parser is implemented using an ANTLR4-generated lexer+parser targeting
    Python.

# Spec: https://specifications.openehr.org/releases/BASE/latest/architecture_overview.html#_paths
"""

import importlib
from dataclasses import replace
from typing import Protocol

from openehr_am.antlr.runtime import construct_lexer_parser
from openehr_am.antlr.span import SourceSpan
from openehr_am.path.ast import Path, PathPredicate, PathSegment
from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.issue_collector import IssueCollector


class _TokenLike(Protocol):
    line: int
    column: int
    text: str | None


def _span_from_tokens(
    start: _TokenLike,
    stop: _TokenLike,
    *,
    filename: str | None,
) -> SourceSpan:
    # ANTLR: line is 1-based, column is 0-based.
    start_line = int(getattr(start, "line", 1))
    start_col = int(getattr(start, "column", 0)) + 1
    end_line = int(getattr(stop, "line", start_line))
    stop_col0 = int(getattr(stop, "column", 0))
    stop_text = getattr(stop, "text", "") or ""
    end_col = stop_col0 + len(stop_text) + 1
    return SourceSpan(
        file=filename,
        start_line=start_line,
        start_col=start_col,
        end_line=end_line,
        end_col=end_col,
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

    issues = IssueCollector()
    try:
        lexer_mod = importlib.import_module("openehr_am._generated.OpenEHRPathLexer")
        parser_mod = importlib.import_module("openehr_am._generated.OpenEHRPathParser")
        OpenEHRPathLexer = getattr(lexer_mod, "OpenEHRPathLexer")
        OpenEHRPathParser = getattr(parser_mod, "OpenEHRPathParser")
    except Exception as exc:  # pragma: no cover
        # Programmer/deployment error (generated code missing). Surface as a
        # programmer error rather than misclassifying as invalid user input.
        raise RuntimeError(
            "Missing generated ANTLR parser for openEHR paths. "
            "Run scripts/generate_parsers.py and commit openehr_am/_generated outputs."
        ) from exc

    _lexer, parser = construct_lexer_parser(
        stripped,
        lexer_class=OpenEHRPathLexer,
        parser_class=OpenEHRPathParser,
        issues=issues,
        file=filename,
        issue_code="PATH900",
    )

    tree = parser.path()
    if len(issues) > 0 or parser.getNumberOfSyntaxErrors() > 0:
        # Preserve API contract: invalid input returns Issues, never raises.
        out = [replace(issue, path=raw) for issue in issues.issues]
        if not out:
            out = [
                Issue(
                    code="PATH900",
                    severity=Severity.ERROR,
                    message="Invalid path",
                    file=filename,
                    line=1,
                    col=1,
                    path=raw,
                )
            ]
        # Historically, parse_path emits a single PATH900 for invalid input.
        return None, [out[0]]

    # Build syntax AST.
    segments: list[PathSegment] = []

    for seg_ctx in tree.segment():
        ident = seg_ctx.IDENT().getSymbol()
        name = ident.text

        predicate_ctx = seg_ctx.predicate()
        predicate: PathPredicate | None = None
        if predicate_ctx is not None:
            pred_raw = predicate_ctx.PREDICATE().getSymbol().text
            # PREDICATE includes surrounding brackets.
            pred_text = pred_raw[1:-1]
            predicate = PathPredicate(
                text=pred_text,
                span=_span_from_tokens(
                    predicate_ctx.start,
                    predicate_ctx.stop,
                    filename=filename,
                ),
            )

        segments.append(
            PathSegment(
                name=name,
                predicate=predicate,
                span=_span_from_tokens(seg_ctx.start, seg_ctx.stop, filename=filename),
            )
        )

    # Optional leading '/definition' is not part of the semantic segments.
    if segments and segments[0].name == "definition" and segments[0].predicate is None:
        segments = segments[1:]

    span = _span_from_tokens(tree.start, tree.stop, filename=filename)
    return Path(segments=tuple(segments), span=span), []
