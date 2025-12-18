"""Syntax-layer AST for openEHR paths.

This is intentionally minimal (MVP) and exists primarily to support validation
rules that need to parse paths embedded in archetypes/templates.

# Spec: https://specifications.openehr.org/releases/BASE/latest/architecture_overview.html#_paths
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan


@dataclass(slots=True, frozen=True)
class PathPredicate:
    """A bracket predicate in a path segment.

    Examples:
        - "at0001"
        - "ac0002"
        - "at0001.1"   (specialised node id; validation is done elsewhere)
        - "name/value='foo'" (kept as raw text for now)
    """

    text: str
    span: SourceSpan | None = None

    def to_string(self) -> str:
        return self.text


@dataclass(slots=True, frozen=True)
class PathSegment:
    """A single segment in an openEHR path."""

    name: str
    predicate: PathPredicate | None = None
    span: SourceSpan | None = None

    def to_string(self) -> str:
        if self.predicate is None:
            return self.name
        return f"{self.name}[{self.predicate.to_string()}]"


@dataclass(slots=True, frozen=True)
class Path:
    """A parsed openEHR path."""

    segments: tuple[PathSegment, ...]
    span: SourceSpan | None = None

    def to_string(self) -> str:
        return "/" + "/".join(seg.to_string() for seg in self.segments)

    def __str__(self) -> str:
        return self.to_string()
