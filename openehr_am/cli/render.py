"""Rendering helpers for CLI output.

Human output uses Rich tables.
JSON output must be strict JSON (no Rich markup / ANSI).
"""

import json
from collections import defaultdict
from collections.abc import Iterable

from rich.console import Console
from rich.table import Table

from openehr_am.validation.issue import Issue


def render_issues(
    issues: Iterable[Issue],
    *,
    console: Console,
    as_json: bool = False,
) -> None:
    """Render Issues to the given console.

    - `as_json=False`: Rich tables grouped by file.
    - `as_json=True`: strict JSON only.
    """

    issues_list = list(issues)

    if as_json:
        payload = [
            issue.to_dict() for issue in sorted(issues_list, key=_issue_sort_key)
        ]
        text = json.dumps(payload, ensure_ascii=False)
        # Print as plain text (no markup/highlighting) while still going through
        # Rich so record=True captures output for tests.
        # Important: prevent Rich from inserting line wraps, which would break JSON.
        console.print(
            text,
            markup=False,
            highlight=False,
            overflow="ignore",
            crop=False,
        )
        return

    for file, group in _group_by_file(issues_list).items():
        table = Table(title=file, show_header=True, header_style="bold")
        table.add_column("Severity", no_wrap=True)
        table.add_column("Code", no_wrap=True)
        table.add_column("Location", no_wrap=True)
        table.add_column("Message")

        for issue in sorted(group, key=_issue_sort_key):
            table.add_row(
                issue.severity.value,
                issue.code,
                _format_line_col(issue.line, issue.col),
                issue.message,
            )

        console.print(table)


def _group_by_file(issues: list[Issue]) -> dict[str, list[Issue]]:
    grouped: dict[str, list[Issue]] = defaultdict(list)
    for issue in issues:
        key = issue.file if issue.file is not None else "(unknown)"
        grouped[key].append(issue)

    # Deterministic group ordering.
    return dict(sorted(grouped.items(), key=lambda kv: kv[0]))


def _issue_sort_key(issue: Issue) -> tuple[object, ...]:
    return (
        issue.file is None,
        issue.file or "",
        issue.line is None,
        issue.line or 0,
        issue.col is None,
        issue.col or 0,
        issue.code,
        issue.message,
    )


def _format_line_col(line: int | None, col: int | None) -> str:
    if line is None:
        return ""
    if col is None:
        return str(line)
    return f"{line}:{col}"
