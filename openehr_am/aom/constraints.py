"""AOM constraint model (skeleton).

This module provides a minimal subset of the openEHR AOM2 constraint types.
It is intended as the semantic target of builders and validators.

Only a small, pragmatic surface is implemented for now.
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan
from openehr_am.aom.debug_dict import aom_to_dict

type MaybeNumber = int | float | None


@dataclass(slots=True, frozen=True)
class Interval:
    """Closed/open interval for integer cardinalities.

    Notes:
        - Bounds are best-effort; validation belongs in `validation/`.
        - Use `None` for unbounded sides.
    """

    lower: MaybeNumber = None
    upper: MaybeNumber = None
    lower_included: bool = True
    upper_included: bool = True
    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


@dataclass(slots=True, frozen=True)
class PrimitiveStringConstraint:
    values: tuple[str, ...] | None = None
    pattern: str | None = None
    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


@dataclass(slots=True, frozen=True)
class PrimitiveIntegerConstraint:
    values: tuple[int, ...] | None = None
    interval: Interval | None = None
    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


@dataclass(slots=True, frozen=True)
class PrimitiveRealConstraint:
    values: tuple[float, ...] | None = None
    interval: Interval | None = None
    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


@dataclass(slots=True, frozen=True)
class PrimitiveBooleanConstraint:
    values: tuple[bool, ...] | None = None
    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


type PrimitiveConstraint = (
    PrimitiveStringConstraint
    | PrimitiveIntegerConstraint
    | PrimitiveRealConstraint
    | PrimitiveBooleanConstraint
)


@dataclass(slots=True, frozen=True)
class Cardinality:
    """Cardinality for multi-valued attributes."""

    occurrences: Interval
    is_ordered: bool = False
    is_unique: bool = False
    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


@dataclass(slots=True, frozen=True)
class CObject:
    """Base class for constraint objects."""

    rm_type_name: str
    node_id: str | None = None
    occurrences: Interval | None = None
    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


@dataclass(slots=True, frozen=True)
class CAttribute:
    """Constraint over an RM attribute."""

    rm_attribute_name: str
    children: tuple[CObject, ...] = ()
    existence: Interval | None = None
    cardinality: Cardinality | None = None
    span: SourceSpan | None = None

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


@dataclass(slots=True, frozen=True)
class CComplexObject(CObject):
    """A complex constraint object with attributes."""

    attributes: tuple[CAttribute, ...] = ()


@dataclass(slots=True, frozen=True)
class CPrimitiveObject(CObject):
    """A primitive constraint object.

    The `constraint` payload is intentionally left opaque for now; it will be
    refined when primitive constraint types are implemented.
    """

    constraint: PrimitiveConstraint | None = None


@dataclass(slots=True, frozen=True)
class ArchetypeSlotPattern:
    """Include/exclude pattern for archetype slot filling (minimal subset)."""

    kind: str  # "exact" | "regex"
    value: str
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CArchetypeSlot(CObject):
    """Archetype slot node.

    Notes:
        This is a minimal representation to support basic slot filling during
        OPT compilation.
    """

    includes: tuple[ArchetypeSlotPattern, ...] = ()
    excludes: tuple[ArchetypeSlotPattern, ...] = ()


__all__ = [
    "PrimitiveConstraint",
    "PrimitiveStringConstraint",
    "PrimitiveIntegerConstraint",
    "PrimitiveRealConstraint",
    "PrimitiveBooleanConstraint",
    "Interval",
    "Cardinality",
    "CObject",
    "CAttribute",
    "CComplexObject",
    "CPrimitiveObject",
    "ArchetypeSlotPattern",
    "CArchetypeSlot",
]
