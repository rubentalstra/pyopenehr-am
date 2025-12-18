"""ADL2 syntax-layer AST nodes.

This module defines a minimal, immutable syntax AST for ADL artefacts.

Parsing code should attach best-effort :class:`~openehr_am.antlr.span.SourceSpan`
instances to nodes and (where useful) to individual fields.

No semantic validation belongs here.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from openehr_am.adl.cadl_ast import CadlObjectNode
from openehr_am.antlr.span import SourceSpan
from openehr_am.odin.ast import OdinNode


class ArtefactKind(StrEnum):
    """Top-level ADL artefact kind.

    Note:
        This is syntax-layer: the parser may set UNKNOWN when it cannot
        confidently classify an artefact.
    """

    ARCHETYPE = "archetype"
    TEMPLATE = "template"
    TEMPLATE_OVERLAY = "template_overlay"
    OPERATIONAL_TEMPLATE = "operational_template"
    UNKNOWN = "unknown"


@dataclass(slots=True, frozen=True)
class AdlSectionPlaceholder:
    """Placeholder node for sections we do not model yet."""

    name: Literal["definition", "rules"]
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class AdlRuleStatement:
    """A single (unparsed) statement line in the ADL `rules` section."""

    text: str
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class AdlRulesSection:
    """Captured ADL `rules` section.

    Notes:
        - This is syntax-layer only. We intentionally do not parse or evaluate
          rule expressions here.
        - `raw_text` is the verbatim section content (between the `rules`
          header and the next section header).
    """

    raw_text: str
    statements: tuple[AdlRuleStatement, ...] = ()

    # Spans
    header_span: SourceSpan | None = None
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class AdlArtefact:
    """Minimal ADL artefact root node.

    Captures only the high-level structure needed to wire ADL parsing into the
    compiler pipeline.
    """

    kind: ArtefactKind
    artefact_id: str

    # Archetype specialisation (dependency).
    #
    # When present, this indicates the parent archetype id declared in the ADL
    # `specialise`/`specialize` section.
    parent_archetype_id: str | None = None

    # Language section
    original_language: str | None = None
    language: str | None = None

    # ODIN subtrees (syntax AST)
    description: OdinNode | None = None
    terminology: OdinNode | None = None

    # Placeholders for sections not modelled yet
    definition: AdlSectionPlaceholder | CadlObjectNode | None = None
    rules: AdlSectionPlaceholder | AdlRulesSection | None = None

    # Spans
    span: SourceSpan | None = None
    kind_span: SourceSpan | None = None
    artefact_id_span: SourceSpan | None = None
    original_language_span: SourceSpan | None = None
    language_span: SourceSpan | None = None
    description_span: SourceSpan | None = None
    terminology_span: SourceSpan | None = None

    parent_archetype_id_span: SourceSpan | None = None


__all__ = [
    "AdlArtefact",
    "AdlRulesSection",
    "AdlRuleStatement",
    "AdlSectionPlaceholder",
    "ArtefactKind",
]
