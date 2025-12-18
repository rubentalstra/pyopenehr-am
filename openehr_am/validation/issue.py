"""Diagnostics primitives.

The entire toolkit reports recoverable problems as `Issue` objects.
"""

from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    """Issue severity.

    Values are uppercase strings to keep JSON output stable.
    """

    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


@dataclass(slots=True, frozen=True)
class Issue:
    """A structured diagnostic for recoverable problems."""

    code: str
    severity: Severity
    message: str

    file: str | None = None
    line: int | None = None
    col: int | None = None
    end_line: int | None = None
    end_col: int | None = None

    path: str | None = None
    node_id: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Convert to a JSON-serializable dictionary."""

        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "file": self.file,
            "line": self.line,
            "col": self.col,
            "end_line": self.end_line,
            "end_col": self.end_col,
            "path": self.path,
            "node_id": self.node_id,
        }

    def pretty(self) -> str:
        """Human-readable one-line representation."""

        location = _format_location(
            file=self.file,
            line=self.line,
            col=self.col,
            end_line=self.end_line,
            end_col=self.end_col,
        )

        main = f"{self.severity.value} {self.code}: {self.message}"

        extras: list[str] = []
        if self.path is not None:
            extras.append(f"path={self.path}")
        if self.node_id is not None:
            extras.append(f"node_id={self.node_id}")

        if extras:
            main = f"{main} ({', '.join(extras)})"

        if location:
            return f"{location}: {main}"
        return main

    def __str__(self) -> str:
        return self.pretty()


def _format_location(
    *,
    file: str | None,
    line: int | None,
    col: int | None,
    end_line: int | None,
    end_col: int | None,
) -> str:
    if file is None:
        return ""

    if line is None:
        return file

    if col is None:
        return f"{file}:{line}"

    start = f"{file}:{line}:{col}"

    # Only format an end span when we have an end column.
    if end_col is None:
        return start

    if end_line is None:
        end_line = line

    if end_line == line:
        return f"{file}:{line}:{col}-{end_col}"

    return f"{file}:{line}:{col}-{end_line}:{end_col}"
