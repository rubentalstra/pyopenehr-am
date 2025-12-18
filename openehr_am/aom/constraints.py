"""AOM constraint model (skeleton).

This module provides a minimal subset of the openEHR AOM2 constraint types.
It is intended as the semantic target of builders and validators.

Only a small, pragmatic surface is implemented for now.
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan

type MaybeInt = int | None


@dataclass(slots=True, frozen=True)
class Interval:
    """Closed/open interval for integer cardinalities.

    Notes:
        - Bounds are best-effort; validation belongs in `validation/`.
        - Use `None` for unbounded sides.
    """

    lower: MaybeInt = None
    upper: MaybeInt = None
    lower_included: bool = True
    upper_included: bool = True


@dataclass(slots=True, frozen=True)
class Cardinality:
    """Cardinality for multi-valued attributes."""

    occurrences: Interval
    is_ordered: bool = False
    is_unique: bool = False
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CObject:
    """Base class for constraint objects."""

    rm_type_name: str
    node_id: str | None = None
    occurrences: Interval | None = None
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CAttribute:
    """Constraint over an RM attribute."""

    rm_attribute_name: str
    children: tuple[CObject, ...] = ()
    existence: Interval | None = None
    cardinality: Cardinality | None = None
    span: SourceSpan | None = None


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

    constraint: object | None = None


__all__ = [
    "Interval",
    "Cardinality",
    "CObject",
    "CAttribute",
    "CComplexObject",
    "CPrimitiveObject",
]
