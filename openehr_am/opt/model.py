"""OPT2 operational template model (subset).

This module defines a minimal, semantic representation of an Operational
Template (OPT) and a subset of *flattened* constraint nodes.

Design goals:
    - Pure Python dataclasses, small surface area.
    - Deterministic `to_dict()` output for JSON export.
    - No parser internals embedded (only primitive spans when helpful).

# Spec: https://specifications.openehr.org/releases/AM/latest/OPT2.html
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan
from openehr_am.opt.debug_dict import opt_to_dict
from openehr_am.opt.json import opt_to_json


@dataclass(slots=True, frozen=True)
class OptInterval:
    """A basic interval used in flattened constraints.

    Notes:
        - `upper=None` represents an unbounded upper.
        - Inclusivity flags are carried for structural completeness; detailed
          validation rules live elsewhere.
    """

    lower: int | float | None
    upper: int | float | None
    lower_included: bool = True
    upper_included: bool = True
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OptCardinality:
    """Cardinality constraint for container attributes."""

    occurrences: OptInterval
    is_ordered: bool = False
    is_unique: bool = False
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OptStringConstraint:
    values: tuple[str, ...] | None = None
    pattern: str | None = None
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OptIntegerConstraint:
    values: tuple[int, ...] | None = None
    interval: OptInterval | None = None
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OptRealConstraint:
    values: tuple[float, ...] | None = None
    interval: OptInterval | None = None
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OptBooleanConstraint:
    values: tuple[bool, ...] | None = None
    span: SourceSpan | None = None


type OptPrimitiveConstraint = (
    OptStringConstraint
    | OptIntegerConstraint
    | OptRealConstraint
    | OptBooleanConstraint
)


@dataclass(slots=True, frozen=True)
class OptCObject:
    """Base class for flattened constraint objects."""

    rm_type_name: str
    node_id: str | None = None

    # Flattened location.
    path: str | None = None

    # Basic constraints.
    occurrences: OptInterval | None = None

    # Provenance.
    source_archetype_id: str | None = None

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OptCAttribute:
    """Flattened attribute constraint."""

    rm_attribute_name: str
    children: tuple[OptCObject, ...] = ()

    existence: OptInterval | None = None
    cardinality: OptCardinality | None = None

    path: str | None = None
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OptCComplexObject(OptCObject):
    attributes: tuple[OptCAttribute, ...] = ()


@dataclass(slots=True, frozen=True)
class OptCPrimitiveObject(OptCObject):
    constraint: OptPrimitiveConstraint | None = None


@dataclass(slots=True, frozen=True)
class OperationalTemplate:
    """A minimal Operational Template (OPT2) representation."""

    template_id: str

    concept: str | None = None
    original_language: str | None = None
    language: str | None = None

    # The root archetype for this OPT (if known).
    root_archetype_id: str | None = None

    # Archetypes included in this OPT (in dependency order when available).
    component_archetype_ids: tuple[str, ...] = ()

    # Flattened constraint tree.
    definition: OptCComplexObject | None = None

    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return opt_to_dict(self)

    def to_json(self, *, indent: int | None = None) -> str:
        return opt_to_json(self, indent=indent)


__all__ = [
    "OptInterval",
    "OptCardinality",
    "OptStringConstraint",
    "OptIntegerConstraint",
    "OptRealConstraint",
    "OptBooleanConstraint",
    "OptPrimitiveConstraint",
    "OptCObject",
    "OptCAttribute",
    "OptCComplexObject",
    "OptCPrimitiveObject",
    "OperationalTemplate",
]
