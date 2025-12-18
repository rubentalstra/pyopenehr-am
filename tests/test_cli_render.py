import json

from rich.console import Console

from openehr_am.cli.render import render_issues
from openehr_am.validation.issue import Issue, Severity


def test_render_issues_rich_groups_by_file_and_sorts_by_line_col() -> None:
    console = Console(record=True, width=120)

    issues = [
        Issue(
            code="AOM200",
            severity=Severity.ERROR,
            message="b",
            file="b.adl",
            line=2,
            col=1,
        ),
        Issue(
            code="AOM200",
            severity=Severity.ERROR,
            message="a",
            file="a.adl",
            line=3,
            col=1,
        ),
        Issue(
            code="AOM210",
            severity=Severity.ERROR,
            message="c",
            file="a.adl",
            line=1,
            col=9,
        ),
    ]

    render_issues(issues, console=console, as_json=False)
    out = console.export_text()

    # Grouping: both file titles present.
    assert "a.adl" in out
    assert "b.adl" in out

    # Sorting within a.adl table: line 1 before line 3.
    assert out.index("AOM210") < out.index("AOM200")


def test_render_issues_json_is_strict_json_no_ansi_or_markup() -> None:
    console = Console(record=True, width=120)

    issues = [
        Issue(code="AOM200", severity=Severity.ERROR, message="b", file="b.adl"),
        Issue(code="AOM200", severity=Severity.ERROR, message="a", file="a.adl"),
    ]

    render_issues(issues, console=console, as_json=True)
    out = console.export_text()

    # No ANSI escapes.
    assert "\x1b[" not in out

    payload = json.loads(out)
    assert [item["file"] for item in payload] == ["a.adl", "b.adl"]
