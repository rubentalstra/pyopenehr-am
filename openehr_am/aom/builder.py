"""Semantic builder: ADL syntax AST -> AOM objects.

This module converts the supported subset of the syntax-layer AST into the
semantic AOM dataclasses.

Design notes:
- This is *not* validation: it should be permissive and preserve spans.
- It must not raise for malformed user artefacts; it returns `Issue` objects.
"""

from openehr_am.adl.ast import AdlArtefact, AdlRulesSection, ArtefactKind
from openehr_am.adl.cadl_ast import (
    CadlArchetypeSlotPattern,
    CadlAttributeNode,
    CadlBooleanConstraint,
    CadlCardinality,
    CadlIntegerConstraint,
    CadlIntegerInterval,
    CadlObjectNode,
    CadlOccurrences,
    CadlPrimitiveConstraint,
    CadlRealConstraint,
    CadlRealInterval,
    CadlStringConstraint,
)
from openehr_am.aom.archetype import Archetype, RuleStatement, Template
from openehr_am.aom.constraints import (
    ArchetypeSlotPattern,
    CArchetypeSlot,
    Cardinality,
    CAttribute,
    CComplexObject,
    CObject,
    CPrimitiveObject,
    Interval,
    PrimitiveBooleanConstraint,
    PrimitiveConstraint,
    PrimitiveIntegerConstraint,
    PrimitiveRealConstraint,
    PrimitiveStringConstraint,
)
from openehr_am.aom.terminology import ArchetypeTerminology
from openehr_am.validation.issue import Issue, Severity


def build_aom_from_adl(
    artefact: AdlArtefact,
) -> tuple[Archetype | Template | None, list[Issue]]:
    """Build an AOM `Archetype` or `Template` from an ADL syntax AST.

    Returns:
        `(aom, issues)` where `aom` is None if building failed.

    This builder supports only the subset of ADL/cADL currently modelled in the
    syntax-layer AST.
    """

    issues: list[Issue] = []

    try:
        definition = _build_root_definition(artefact, issues)

        terminology = _build_terminology(artefact)

        rules: tuple[RuleStatement, ...] = ()
        if isinstance(artefact.rules, AdlRulesSection):
            rules = tuple(
                RuleStatement(text=s.text, span=s.span)
                for s in artefact.rules.statements
            )

        if artefact.kind is ArtefactKind.ARCHETYPE:
            return (
                Archetype(
                    archetype_id=artefact.artefact_id,
                    parent_archetype_id=artefact.parent_archetype_id,
                    concept=definition.node_id if definition is not None else None,
                    original_language=artefact.original_language,
                    languages=(artefact.language,) if artefact.language else (),
                    definition=definition,
                    terminology=terminology,
                    rules=rules,
                    span=artefact.span,
                ),
                issues,
            )

        if artefact.kind is ArtefactKind.TEMPLATE:
            return (
                Template(
                    template_id=artefact.artefact_id,
                    concept=definition.node_id if definition is not None else None,
                    original_language=artefact.original_language,
                    languages=(artefact.language,) if artefact.language else (),
                    definition=definition,
                    terminology=terminology,
                    rules=rules,
                    span=artefact.span,
                ),
                issues,
            )

        issues.append(
            Issue(
                code="AOM205",
                severity=Severity.ERROR,
                message=f"Unsupported artefact kind for AOM build: {artefact.kind}",
                file=artefact.span.file if artefact.span else None,
                line=artefact.span.start_line if artefact.span else None,
                col=artefact.span.start_col if artefact.span else None,
                end_line=artefact.span.end_line if artefact.span else None,
                end_col=artefact.span.end_col if artefact.span else None,
            )
        )
        return None, issues

    except (AttributeError, TypeError, ValueError, IndexError, KeyError) as e:
        # Builder must not raise for malformed artefacts.
        issues.append(
            Issue(
                code="AOM205",
                severity=Severity.ERROR,
                message=f"AOM build failed: {e}",
                file=artefact.span.file if artefact.span else None,
                line=artefact.span.start_line if artefact.span else None,
                col=artefact.span.start_col if artefact.span else None,
                end_line=artefact.span.end_line if artefact.span else None,
                end_col=artefact.span.end_col if artefact.span else None,
            )
        )
        return None, issues


def _build_terminology(artefact: AdlArtefact) -> ArchetypeTerminology | None:
    # Our fixtures currently use empty <> blocks; for the supported subset we
    # preserve the span and original language.
    if artefact.terminology is None:
        return None

    if artefact.original_language is None:
        return ArchetypeTerminology(
            original_language="",
            term_definitions=(),
            term_bindings=(),
            span=artefact.terminology.span,
        )

    return ArchetypeTerminology(
        original_language=artefact.original_language,
        term_definitions=(),
        term_bindings=(),
        span=artefact.terminology.span,
    )


def _build_root_definition(
    artefact: AdlArtefact, issues: list[Issue]
) -> CComplexObject | None:
    if not isinstance(artefact.definition, CadlObjectNode):
        return None

    obj = _build_cadl_object(artefact.definition)
    if isinstance(obj, CComplexObject):
        return obj

    # Root definition being primitive is not expected for archetypes/templates.
    issues.append(
        Issue(
            code="AOM205",
            severity=Severity.ERROR,
            message="Root definition must be a complex object",
            file=artefact.definition.span.file if artefact.definition.span else None,
            line=artefact.definition.span.start_line
            if artefact.definition.span
            else None,
            col=artefact.definition.span.start_col
            if artefact.definition.span
            else None,
            end_line=artefact.definition.span.end_line
            if artefact.definition.span
            else None,
            end_col=artefact.definition.span.end_col
            if artefact.definition.span
            else None,
        )
    )
    return None


def _build_cadl_object(node: CadlObjectNode) -> CObject:
    occurrences = _build_occurrences(node.occurrences)

    if node.primitive is not None:
        return CPrimitiveObject(
            rm_type_name=node.rm_type_name,
            node_id=node.node_id,
            occurrences=occurrences,
            constraint=_build_primitive_constraint(node.primitive),
            span=node.span,
        )

    if node.slot is not None:
        return CArchetypeSlot(
            rm_type_name=node.rm_type_name,
            node_id=node.node_id,
            occurrences=occurrences,
            includes=tuple(_build_slot_pattern(p) for p in node.slot.includes),
            excludes=tuple(_build_slot_pattern(p) for p in node.slot.excludes),
            span=node.span,
        )

    attributes = tuple(_build_cadl_attribute(a) for a in node.attributes)
    return CComplexObject(
        rm_type_name=node.rm_type_name,
        node_id=node.node_id,
        occurrences=occurrences,
        attributes=attributes,
        span=node.span,
    )


def _build_slot_pattern(node: CadlArchetypeSlotPattern) -> ArchetypeSlotPattern:
    return ArchetypeSlotPattern(kind=node.kind, value=node.value, span=node.span)


def _build_cadl_attribute(node: CadlAttributeNode) -> CAttribute:
    return CAttribute(
        rm_attribute_name=node.rm_attribute_name,
        children=tuple(_build_cadl_object(c) for c in node.children),
        existence=None,
        cardinality=_build_cardinality(node.cardinality),
        span=node.span,
    )


def _build_occurrences(node: CadlOccurrences | None) -> Interval | None:
    if node is None:
        return None

    upper = None if node.upper_unbounded else node.upper
    return Interval(lower=node.lower, upper=upper, span=node.span)


def _build_cardinality(node: CadlCardinality | None) -> Cardinality | None:
    if node is None:
        return None

    upper = None if node.upper_unbounded else node.upper
    interval = Interval(lower=node.lower, upper=upper, span=node.span)

    return Cardinality(
        occurrences=interval,
        is_ordered=bool(node.is_ordered),
        is_unique=bool(node.is_unique),
        span=node.span,
    )


def _build_primitive_constraint(node: CadlPrimitiveConstraint) -> PrimitiveConstraint:
    if isinstance(node, CadlStringConstraint):
        return PrimitiveStringConstraint(
            values=node.values,
            pattern=node.pattern,
            span=node.span,
        )

    if isinstance(node, CadlIntegerConstraint):
        return PrimitiveIntegerConstraint(
            values=node.values,
            interval=_build_int_interval(node.interval),
            span=node.span,
        )

    if isinstance(node, CadlRealConstraint):
        return PrimitiveRealConstraint(
            values=node.values,
            interval=_build_real_interval(node.interval),
            span=node.span,
        )

    if isinstance(node, CadlBooleanConstraint):
        return PrimitiveBooleanConstraint(values=node.values, span=node.span)

    raise TypeError(f"Unsupported primitive constraint: {type(node)!r}")


def _build_int_interval(node: CadlIntegerInterval | None) -> Interval | None:
    if node is None:
        return None

    upper = None if node.upper_unbounded else node.upper
    return Interval(lower=node.lower, upper=upper, span=node.span)


def _build_real_interval(node: CadlRealInterval | None) -> Interval | None:
    if node is None:
        return None

    # Interval is integer-typed; for now we store floats via runtime values.
    # This is a supported-subset compromise; validators/compilers should treat
    # these as best-effort until a dedicated real interval type exists.
    upper = None if node.upper_unbounded else node.upper
    return Interval(lower=node.lower, upper=upper, span=node.span)  # type: ignore[arg-type]


__all__ = ["build_aom_from_adl"]
