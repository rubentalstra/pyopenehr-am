"""AOM terminology model.

This is a minimal, typed representation of archetype terminology.

It is designed to be:
- immutable (frozen dataclasses)
- safe to construct incrementally by builders
- suitable for validators to check references and bindings
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan


@dataclass(slots=True, frozen=True)
class TermDefinition:
    """A single term definition (e.g. `at0000`)."""

    language: str
    code: str
    text: str
    description: str | None = None
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class TermBinding:
    """A binding of an internal code to an external terminology."""

    terminology: str
    code: str
    target: str
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class ArchetypeTerminology:
    """Terminology bundle for an archetype/template."""

    original_language: str
    term_definitions: tuple[TermDefinition, ...] = ()
    term_bindings: tuple[TermBinding, ...] = ()

    span: SourceSpan | None = None


__all__ = [
    "ArchetypeTerminology",
    "TermBinding",
    "TermDefinition",
]
