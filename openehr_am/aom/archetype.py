"""AOM roots: Archetype and Template.

These are semantic-layer objects that downstream validation and compilation use.
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan
from openehr_am.aom.constraints import CComplexObject
from openehr_am.aom.terminology import ArchetypeTerminology


@dataclass(slots=True, frozen=True)
class Archetype:
    """Semantic representation of an openEHR archetype."""

    archetype_id: str
    concept: str | None = None

    original_language: str | None = None
    languages: tuple[str, ...] = ()

    definition: CComplexObject | None = None
    terminology: ArchetypeTerminology | None = None

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class Template:
    """Semantic representation of an openEHR template.

    Note:
        Templates in openEHR are also ADL artefacts; for now we model only the
        essentials needed by the compiler pipeline.
    """

    template_id: str
    concept: str | None = None

    original_language: str | None = None
    languages: tuple[str, ...] = ()

    definition: CComplexObject | None = None
    terminology: ArchetypeTerminology | None = None

    span: SourceSpan | None = None


__all__ = [
    "Archetype",
    "Template",
]
