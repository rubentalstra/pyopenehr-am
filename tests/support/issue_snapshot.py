from dataclasses import replace
from pathlib import Path

from openehr_am.validation.issue import Issue


def _normalize_file(file: str | None, *, root: Path | None) -> str | None:
    if file is None or root is None:
        return file

    try:
        rel = Path(file).resolve().relative_to(root.resolve())
    except (OSError, RuntimeError, ValueError):
        return file

    return rel.as_posix()


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

    if end_col is None:
        return start

    if end_line is None:
        end_line = line

    if end_line == line:
        return f"{file}:{line}:{col}-{end_col}"

    return f"{file}:{line}:{col}-{end_line}:{end_col}"


def _sort_key(issue: Issue, *, root: Path | None) -> tuple[object, ...]:
    file = _normalize_file(issue.file, root=root)
    return (
        file is None,
        file or "",
        issue.line is None,
        issue.line or 0,
        issue.col is None,
        issue.col or 0,
        issue.code,
        issue.message,
    )


def format_issues(issues: list[Issue] | tuple[Issue, ...], *, root: Path | None) -> str:
    """Format Issues deterministically for snapshot-style assertions.

    - Sorts deterministically (file/line/col/code/message).
    - Normalizes file paths relative to `root` when possible.
    - Uses a stable single-line format per Issue.
    """

    normalized: list[Issue] = []
    for issue in issues:
        file = _normalize_file(issue.file, root=root)
        if file != issue.file:
            normalized.append(replace(issue, file=file))
        else:
            normalized.append(issue)

    normalized.sort(key=lambda i: _sort_key(i, root=root))

    lines: list[str] = []
    for issue in normalized:
        location = _format_location(
            file=issue.file,
            line=issue.line,
            col=issue.col,
            end_line=issue.end_line,
            end_col=issue.end_col,
        )

        main = f"{issue.severity.value} {issue.code}: {issue.message}"

        extras: list[str] = []
        if issue.path is not None:
            extras.append(f"path={issue.path}")
        if issue.node_id is not None:
            extras.append(f"node_id={issue.node_id}")

        if extras:
            main = f"{main} ({', '.join(extras)})"

        if location:
            lines.append(f"{location}: {main}")
        else:
            lines.append(main)

    return "\n".join(lines) + ("\n" if lines else "")
