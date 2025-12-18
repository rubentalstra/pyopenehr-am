"""AOM roots: Archetype and Template.

These are semantic-layer objects that downstream validation and compilation use.
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan
from openehr_am.aom.constraints import CComplexObject
from openehr_am.aom.debug_dict import aom_to_dict
from openehr_am.aom.terminology import ArchetypeTerminology


@dataclass(slots=True, frozen=True)
class RuleStatement:
    """A single rule statement captured from the ADL RULES section.

    This is a semantic-layer representation that keeps only the raw statement
    text plus a best-effort source span.
    """

    text: str
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class Archetype:
    """Semantic representation of an openEHR archetype."""

    archetype_id: str
    parent_archetype_id: str | None = None
    concept: str | None = None

    original_language: str | None = None
    languages: tuple[str, ...] = ()

    definition: CComplexObject | None = None
    terminology: ArchetypeTerminology | None = None

    rules: tuple[RuleStatement, ...] = ()

    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


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

    rules: tuple[RuleStatement, ...] = ()

    # Template-specific directives.
    #
    # These are currently modeled as plain openEHR-style paths so validation and
    # compilation can remain independent of any particular parsing strategy.
    excluded_paths: tuple[str, ...] = ()
    overlay_paths: tuple[str, ...] = ()

    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


__all__ = [
    "Archetype",
    "RuleStatement",
    "Template",
]
