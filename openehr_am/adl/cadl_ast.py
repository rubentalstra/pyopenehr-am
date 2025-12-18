"""cADL syntax-layer AST nodes.

This module models the *constraint* subtree used in ADL2 archetype definitions
(cADL). It intentionally stays at the syntax level:

- Nodes carry best-effort :class:`~openehr_am.antlr.span.SourceSpan` locations.
- No semantic validation belongs here.

The goal is to provide a stable, minimal representation for:
- object constraint nodes (RM type name + optional node id)
- attribute constraint nodes with children
- occurrences and cardinality
- primitive constraints
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan


@dataclass(slots=True, frozen=True)
class CadlOccurrences:
    """An occurrences interval constraint.

    Notes:
        - This is syntax-level: the parser may leave fields as ``None`` when the
          interval is absent or partially specified.
        - Unbounded upper limits are represented with ``upper_unbounded=True``.
    """

    lower: int | None
    upper: int | None
    upper_unbounded: bool = False

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CadlCardinality:
    """A cardinality interval constraint for container attributes."""

    lower: int | None
    upper: int | None
    upper_unbounded: bool = False

    is_ordered: bool | None = None
    is_unique: bool | None = None

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CadlIntegerInterval:
    """Integer interval (e.g. ``0..10`` or ``0..*``)."""

    lower: int | None
    upper: int | None
    upper_unbounded: bool = False

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CadlRealInterval:
    """Real interval (e.g. ``0.0..1.0``)."""

    lower: float | None
    upper: float | None
    upper_unbounded: bool = False

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CadlStringConstraint:
    """String constraint.

    Supports either a set of permitted values and/or a regex pattern.
    """

    values: tuple[str, ...] | None = None
    pattern: str | None = None

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CadlIntegerConstraint:
    """Integer constraint (values and/or interval)."""

    values: tuple[int, ...] | None = None
    interval: CadlIntegerInterval | None = None

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CadlRealConstraint:
    """Real constraint (values and/or interval)."""

    values: tuple[float, ...] | None = None
    interval: CadlRealInterval | None = None

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CadlBooleanConstraint:
    """Boolean constraint as a set of permitted values."""

    values: tuple[bool, ...] | None = None

    span: SourceSpan | None = None


type CadlPrimitiveConstraint = (
    CadlStringConstraint
    | CadlIntegerConstraint
    | CadlRealConstraint
    | CadlBooleanConstraint
)


@dataclass(slots=True, frozen=True)
class CadlObjectNode:
    """Constraint object node.

    Represents both complex and primitive objects.

    - Complex objects have ``attributes`` populated and ``primitive`` set to
      ``None``.
    - Primitive objects carry the constraint in ``primitive`` and typically have
      ``attributes=()``.
    """

    rm_type_name: str
    node_id: str | None = None

    occurrences: CadlOccurrences | None = None

    attributes: CadlAttributes = ()
    primitive: CadlPrimitiveConstraint | None = None

    span: SourceSpan | None = None
    rm_type_name_span: SourceSpan | None = None
    node_id_span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CadlAttributeNode:
    """Constraint for a single RM attribute."""

    rm_attribute_name: str
    children: CadlObjectChildren

    cardinality: CadlCardinality | None = None

    span: SourceSpan | None = None
    rm_attribute_name_span: SourceSpan | None = None


type CadlObjectChildren = tuple[CadlObjectNode, ...]


type CadlAttributes = tuple[CadlAttributeNode, ...]


type CadlNode = CadlObjectNode | CadlAttributeNode | CadlPrimitiveConstraint


__all__ = [
    "CadlAttributeNode",
    "CadlBooleanConstraint",
    "CadlCardinality",
    "CadlIntegerConstraint",
    "CadlIntegerInterval",
    "CadlNode",
    "CadlObjectNode",
    "CadlOccurrences",
    "CadlPrimitiveConstraint",
    "CadlRealConstraint",
    "CadlRealInterval",
    "CadlStringConstraint",
]
