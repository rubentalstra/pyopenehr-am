from pathlib import Path

from tests.repo_root import repo_root
from tests.support.issue_snapshot import format_issues

from openehr_am.validation.issue import Issue, Severity


def test_format_issues_normalizes_paths_and_sorts() -> None:
    root = repo_root()

    issues = [
        Issue(
            code="ADL010",
            severity=Severity.ERROR,
            message="Second",
            file=str(root / "b.adl"),
            line=2,
            col=1,
        ),
        Issue(
            code="ADL009",
            severity=Severity.ERROR,
            message="First",
            file=str(root / "a.adl"),
            line=1,
            col=5,
        ),
        Issue(
            code="ADL011",
            severity=Severity.WARN,
            message="No file",
        ),
    ]

    out = format_issues(issues, root=root)
    assert out == (
        "a.adl:1:5: ERROR ADL009: First\n"
        "b.adl:2:1: ERROR ADL010: Second\n"
        "WARN ADL011: No file\n"
    )


def test_format_issues_keeps_non_repo_paths() -> None:
    root = repo_root()
    external = str(Path("/tmp/outside.adl"))

    out = format_issues(
        [
            Issue(
                code="ADL001",
                severity=Severity.ERROR,
                message="Boom",
                file=external,
                line=1,
                col=1,
            )
        ],
        root=root,
    )

    assert out == f"{external}:1:1: ERROR ADL001: Boom\n"
