"""AQL syntax checking (ANTLR).

This module provides a narrow, stable API that validates AQL text syntax without
exposing ANTLR parse-tree objects.

# Spec: https://specifications.openehr.org/releases/QUERY/Release-1.1.0
"""

import importlib

from openehr_am.antlr.runtime import construct_lexer_parser
from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.issue_collector import IssueCollector


def check_aql_syntax(text: str, *, filename: str | None = None) -> list[Issue]:
    """Return syntax Issues for an AQL query.

    Args:
        text: AQL query text.
        filename: Optional filename used for Issue locations.

    Returns:
        List of Issues. Empty means the query is syntactically valid.

    Notes:
        - This function never raises for invalid user input.
        - This function does not build an AQL AST yet.

    # Spec: https://specifications.openehr.org/releases/QUERY/Release-1.1.0
    """

    if not isinstance(text, str):
        raise TypeError("check_aql_syntax expects 'text' to be str")

    issues = IssueCollector()

    try:
        lexer_mod = importlib.import_module("openehr_am._generated.AqlLexer")
        parser_mod = importlib.import_module("openehr_am._generated.AqlParser")
        AqlLexer = getattr(lexer_mod, "AqlLexer")
        AqlParser = getattr(parser_mod, "AqlParser")
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Missing generated ANTLR parser for AQL. "
            "Run scripts/generate_parsers.py and commit openehr_am/_generated outputs."
        ) from exc

    _lexer, parser = construct_lexer_parser(
        text,
        lexer_class=AqlLexer,
        parser_class=AqlParser,
        issues=issues,
        file=filename,
        issue_code="AQL100",
    )

    # Root rule per AqlParser.g4.
    parser.selectQuery()

    if len(issues) > 0 or parser.getNumberOfSyntaxErrors() > 0:
        if len(issues) == 0:
            return [
                Issue(
                    code="AQL100",
                    severity=Severity.ERROR,
                    message="Invalid AQL query",
                    file=filename,
                    line=1,
                    col=1,
                )
            ]
        return list(issues.issues)

    return []


__all__ = [
    "check_aql_syntax",
]
