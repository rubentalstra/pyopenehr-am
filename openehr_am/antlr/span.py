"""Source span primitives for parsing-layer ASTs.

Parsing produces syntax-layer AST nodes that carry best-effort source locations.

The shared span format is:
- file, start_line, start_col, end_line, end_col

Line/col are 1-based.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SourceSpan:
    """A best-effort span for syntax-layer nodes."""

    file: str | None
    start_line: int
    start_col: int
    end_line: int
    end_col: int
