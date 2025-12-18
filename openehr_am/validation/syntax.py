"""Syntax-level validation entrypoints.

`validate_syntax` is a convenience wrapper that calls the parsing layer and
returns deterministically ordered `Issue` objects.

# Spec: https://specifications.openehr.org/releases/AM/latest/ADL2.html
"""

from pathlib import Path

from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.issue_collector import IssueCollector


def validate_syntax(
    *,
    text: str | None = None,
    path: str | Path | None = None,
    filename: str | None = None,
) -> tuple[Issue, ...]:
    """Validate syntax by parsing ADL text.

    Exactly one of `text` or `path` must be provided.

    Args:
        text: ADL source text.
        path: Filesystem path to an ADL file.
        filename: Optional filename to attach to Issues when validating `text`.

    Returns:
        Tuple of Issues sorted deterministically.
    """

    if (text is None) == (path is None):
        raise TypeError("validate_syntax expects exactly one of 'text' or 'path'")

    if path is not None:
        from openehr_am.adl.parser import parse_adl

        p = Path(path)
        try:
            source = p.read_text(encoding="utf-8")
        except OSError as e:
            collector = IssueCollector(
                [
                    Issue(
                        code="ADL005",
                        severity=Severity.ERROR,
                        message=f"Cannot read input file: {e}",
                        file=str(p),
                        line=1,
                        col=1,
                    )
                ]
            )
            return collector.issues

        _artefact, issues = parse_adl(source, filename=str(p))
        collector = IssueCollector(issues)
        return collector.issues

    assert text is not None
    from openehr_am.adl.parser import parse_adl

    _artefact, issues = parse_adl(text, filename=filename)
    collector = IssueCollector(issues)
    return collector.issues
