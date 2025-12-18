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
from openehr_am.validation.issue import Issue, Severity


def _issue_from_span(*, code: str, message: str, span: SourceSpan | None) -> Issue:
    if span is None:
        return Issue(code=code, severity=Severity.ERROR, message=message)

    return Issue(
        code=code,
        severity=Severity.ERROR,
        message=message,
        file=span.file,
        line=span.start_line,
        col=span.start_col,
        end_line=span.end_line,
        end_col=span.end_col,
    )


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

    def validate(self, *, code: str = "ADL030") -> list[Issue]:
        """Validate structural correctness of the interval (syntax-level).

        This intentionally does not do semantic validation.

        # Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
        """

        issues: list[Issue] = []

        if self.upper_unbounded and self.upper is not None:
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Occurrences upper is set but upper_unbounded is True",
                    span=self.span,
                )
            )

        if not self.upper_unbounded and self.upper is None:
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Occurrences upper is missing and is not unbounded",
                    span=self.span,
                )
            )

        if self.lower is not None and self.lower < 0:
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Occurrences lower must be >= 0",
                    span=self.span,
                )
            )
        if self.upper is not None and self.upper < 0:
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Occurrences upper must be >= 0",
                    span=self.span,
                )
            )

        if (
            self.lower is not None
            and self.upper is not None
            and self.lower > self.upper
        ):
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Occurrences lower must be <= upper",
                    span=self.span,
                )
            )

        return issues


@dataclass(slots=True, frozen=True)
class CadlCardinality:
    """A cardinality interval constraint for container attributes."""

    lower: int | None
    upper: int | None
    upper_unbounded: bool = False

    is_ordered: bool | None = None
    is_unique: bool | None = None

    span: SourceSpan | None = None

    def validate(self, *, code: str = "ADL030") -> list[Issue]:
        """Validate structural correctness of the cardinality interval.

        # Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
        """

        issues: list[Issue] = []

        if self.upper_unbounded and self.upper is not None:
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Cardinality upper is set but upper_unbounded is True",
                    span=self.span,
                )
            )

        if not self.upper_unbounded and self.upper is None:
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Cardinality upper is missing and is not unbounded",
                    span=self.span,
                )
            )

        if self.lower is not None and self.lower < 0:
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Cardinality lower must be >= 0",
                    span=self.span,
                )
            )
        if self.upper is not None and self.upper < 0:
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Cardinality upper must be >= 0",
                    span=self.span,
                )
            )

        if (
            self.lower is not None
            and self.upper is not None
            and self.lower > self.upper
        ):
            issues.append(
                _issue_from_span(
                    code=code,
                    message="Cardinality lower must be <= upper",
                    span=self.span,
                )
            )

        return issues


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
class CadlArchetypeSlotPattern:
    """A single include/exclude pattern for archetype slot matching.

    Notes:
        - `kind="exact"` means literal equality match against archetype_id.
        - `kind="regex"` means Python `re` fullmatch against archetype_id.
    """

    kind: str  # "exact" | "regex"
    value: str
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class CadlArchetypeSlot:
    """Archetype slot constraints (minimal subset).

    This is a minimal representation used by basic OPT slot filling.
    """

    includes: tuple[CadlArchetypeSlotPattern, ...] = ()
    excludes: tuple[CadlArchetypeSlotPattern, ...] = ()

    span: SourceSpan | None = None


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

    slot: CadlArchetypeSlot | None = None

    span: SourceSpan | None = None
    rm_type_name_span: SourceSpan | None = None
    node_id_span: SourceSpan | None = None

    def validate(self, *, code: str = "ADL030") -> list[Issue]:
        """Validate structural correctness of this subtree (syntax-level)."""

        issues: list[Issue] = []

        if self.occurrences is not None:
            issues.extend(self.occurrences.validate(code=code))

        for attribute in self.attributes:
            issues.extend(attribute.validate(code=code))

        # Slot blocks are currently validated at compile time.

        return issues


@dataclass(slots=True, frozen=True)
class CadlAttributeNode:
    """Constraint for a single RM attribute."""

    rm_attribute_name: str
    children: CadlObjectChildren

    cardinality: CadlCardinality | None = None

    span: SourceSpan | None = None
    rm_attribute_name_span: SourceSpan | None = None

    def validate(self, *, code: str = "ADL030") -> list[Issue]:
        issues: list[Issue] = []

        if self.cardinality is not None:
            issues.extend(self.cardinality.validate(code=code))

        for child in self.children:
            issues.extend(child.validate(code=code))

        return issues


type CadlObjectChildren = tuple[CadlObjectNode, ...]


type CadlAttributes = tuple[CadlAttributeNode, ...]


type CadlNode = CadlObjectNode | CadlAttributeNode | CadlPrimitiveConstraint


__all__ = [
    "CadlArchetypeSlot",
    "CadlArchetypeSlotPattern",
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
