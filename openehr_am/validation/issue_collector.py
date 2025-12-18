"""Utilities for collecting and exporting Issues.

This exists to keep output ordering deterministic across all layers.
"""

import json
from collections.abc import Iterable, Iterator

from openehr_am.validation.issue import Issue, Severity


def _issue_sort_key(issue: Issue) -> tuple[object, ...]:
    # Deterministic ordering policy (see validation.instructions.md):
    # sort by file, line, col, code, message.
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


class IssueCollector:
    """Collect Issues with deterministic ordering."""

    def __init__(self, issues: Iterable[Issue] | None = None) -> None:
        self._issues: list[Issue] = []
        if issues is not None:
            self.extend(issues)

    @property
    def issues(self) -> tuple[Issue, ...]:
        return tuple(self._issues)

    def extend(self, issues: Iterable[Issue]) -> None:
        self._issues.extend(issues)
        self._issues.sort(key=_issue_sort_key)

    def has_errors(self) -> bool:
        return any(issue.severity == Severity.ERROR for issue in self._issues)

    def to_json(self) -> str:
        """Serialize issues as strict JSON (no Rich markup)."""

        return json.dumps(
            [issue.to_dict() for issue in self._issues], ensure_ascii=False
        )

    def __iter__(self) -> Iterator[Issue]:
        return iter(self._issues)

    def __len__(self) -> int:
        return len(self._issues)
