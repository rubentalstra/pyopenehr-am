"""Default semantic validation checks.

Checks in this module are registered into the semantic DEFAULT_REGISTRY on
import.

# Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html#_archetype_terminology_class
"""

from collections.abc import Iterable, Iterator

from openehr_am.antlr.span import SourceSpan
from openehr_am.aom.archetype import Archetype, Template
from openehr_am.aom.constraints import (
    CAttribute,
    CComplexObject,
    CObject,
    CPrimitiveObject,
    Interval,
    PrimitiveIntegerConstraint,
    PrimitiveRealConstraint,
)
from openehr_am.aom.ids import try_parse_node_id
from openehr_am.aom.terminology import ArchetypeTerminology
from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.semantic import register_semantic_check


def _span_key(span: SourceSpan | None) -> tuple[object, ...]:
    # Mirror IssueCollector ordering as closely as possible.
    if span is None:
        return (True, "", True, 0, True, 0)
    return (
        span.file is None,
        span.file or "",
        False,
        span.start_line,
        False,
        span.start_col,
    )


def _iter_cobject_tree(root: CObject) -> Iterator[CObject]:
    yield root
    if isinstance(root, CComplexObject):
        for attr in root.attributes:
            yield from _iter_cattribute(attr)


def _iter_cattribute(attr: CAttribute) -> Iterator[CObject]:
    for child in attr.children:
        yield from _iter_cobject_tree(child)


def _iter_referenced_node_ids(
    *,
    artefact: Archetype | Template,
) -> Iterator[tuple[str, SourceSpan | None]]:
    if artefact.concept is not None and _is_node_id_like(artefact.concept):
        yield artefact.concept, artefact.span

    if artefact.definition is None:
        return

    for obj in _iter_cobject_tree(artefact.definition):
        if obj.node_id is None:
            continue
        if _is_node_id_like(obj.node_id):
            yield obj.node_id, obj.span


def _try_parse_specialised_node_id(value: str) -> tuple[str, int] | None:
    """Parse `atNNNN(.n)*` / `acNNNN(.n)*`.

    Returns:
        (base_code, depth) where depth is the number of suffix segments.
        Returns None if the format is invalid.

    Notes:
        - Suffix segments must be positive integers (>= 1).
        - This is a permissive parser used for validation rules; it must not raise.
    """

    if not value:
        return None

    parts = value.split(".")
    if not parts:
        return None

    base = parts[0]
    if try_parse_node_id(base) is None:
        return None

    if len(parts) == 1:
        return base, 0

    for seg in parts[1:]:
        if not seg or not seg.isdigit():
            return None
        # Basic safety: specialisation suffix segments start at 1.
        if int(seg) < 1:
            return None

    return base, len(parts) - 1


def _is_node_id_like(value: str) -> bool:
    return _try_parse_specialised_node_id(value) is not None


def _specialisation_depth(value: str) -> int | None:
    parsed = _try_parse_specialised_node_id(value)
    if parsed is None:
        return None
    _base, depth = parsed
    return depth


def _defined_codes(term: ArchetypeTerminology | None) -> set[str]:
    if term is None:
        return set()
    return {td.code for td in term.term_definitions}


def check_referenced_terminology_codes_exist(ctx: ValidationContext) -> Iterable[Issue]:
    """AOM200: every referenced `atNNNN`/`acNNNN` exists in terminology."""

    artefact = ctx.artefact
    if not isinstance(artefact, (Archetype, Template)):
        return ()

    defined = _defined_codes(artefact.terminology)

    referenced: list[tuple[str, SourceSpan | None]] = list(
        _iter_referenced_node_ids(artefact=artefact)
    )

    # Term bindings reference internal codes too.
    if artefact.terminology is not None:
        for b in artefact.terminology.term_bindings:
            if _is_node_id_like(b.code):
                referenced.append((b.code, b.span))

    referenced.sort(key=lambda item: (_span_key(item[1]), item[0]))

    issues: list[Issue] = []
    for code, span in referenced:
        if code in defined:
            continue
        issues.append(
            Issue(
                code="AOM200",
                severity=Severity.ERROR,
                message=f"Terminology code '{code}' referenced but not defined",
                file=span.file if span else None,
                line=span.start_line if span else None,
                col=span.start_col if span else None,
                end_line=span.end_line if span else None,
                end_col=span.end_col if span else None,
                node_id=code,
            )
        )

    return tuple(issues)


def check_node_id_format(ctx: ValidationContext) -> Iterable[Issue]:
    """AOM210: node ids must match expected patterns.

    Accepts the basic AOM2 node-id forms `atNNNN` / `acNNNN` and their
    specialised variants with dot-separated suffixes (e.g. `at0001.1`).

    # Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
    """

    artefact = ctx.artefact
    if not isinstance(artefact, (Archetype, Template)):
        return ()

    issues: list[Issue] = []

    def maybe_emit(value: str, span: SourceSpan | None) -> None:
        if _is_node_id_like(value):
            return
        issues.append(
            Issue(
                code="AOM210",
                severity=Severity.ERROR,
                message=f"Invalid node id format: '{value}'",
                file=span.file if span else None,
                line=span.start_line if span else None,
                col=span.start_col if span else None,
                end_line=span.end_line if span else None,
                end_col=span.end_col if span else None,
                node_id=value,
            )
        )

    if artefact.concept is not None:
        maybe_emit(artefact.concept, artefact.span)

    if artefact.definition is not None:
        for obj in _iter_cobject_tree(artefact.definition):
            if obj.node_id is None:
                continue
            maybe_emit(obj.node_id, obj.span)

    if artefact.terminology is not None:
        for td in artefact.terminology.term_definitions:
            maybe_emit(td.code, td.span)
        for b in artefact.terminology.term_bindings:
            maybe_emit(b.code, b.span)

    return tuple(issues)


def check_specialisation_depth_mismatch(ctx: ValidationContext) -> Iterable[Issue]:
    """AOM230: specialisation level mismatch (basic).

    Basic rule: a node id's specialisation depth must not exceed the artefact's
    concept node-id depth.

    # Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
    """

    artefact = ctx.artefact
    if not isinstance(artefact, (Archetype, Template)):
        return ()

    if artefact.concept is None:
        return ()

    artefact_depth = _specialisation_depth(artefact.concept)
    if artefact_depth is None:
        # Let AOM210 report the invalid concept node id.
        return ()

    issues: list[Issue] = []

    def check_depth(value: str, span: SourceSpan | None) -> None:
        depth = _specialisation_depth(value)
        if depth is None:
            return
        if depth <= artefact_depth:
            return
        issues.append(
            Issue(
                code="AOM230",
                severity=Severity.ERROR,
                message=(
                    "Specialisation level mismatch: "
                    f"'{value}' depth {depth} exceeds archetype depth {artefact_depth}"
                ),
                file=span.file if span else None,
                line=span.start_line if span else None,
                col=span.start_col if span else None,
                end_line=span.end_line if span else None,
                end_col=span.end_col if span else None,
                node_id=value,
            )
        )

    if artefact.definition is not None:
        for obj in _iter_cobject_tree(artefact.definition):
            if obj.node_id is None:
                continue
            check_depth(obj.node_id, obj.span)

    return tuple(issues)


def check_duplicates_in_scopes(ctx: ValidationContext) -> Iterable[Issue]:
    """AOM240: detect duplicates in basic scopes.

    Implemented (basic) checks:
    - Duplicate attribute names within the same `CComplexObject`.
    - Duplicate sibling `node_id` values within the same attribute.

    # Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
    """

    artefact = ctx.artefact
    if not isinstance(artefact, (Archetype, Template)):
        return ()

    if artefact.definition is None:
        return ()

    issues: list[Issue] = []

    def walk(obj: CObject, *, path: str) -> None:
        if not isinstance(obj, CComplexObject):
            return

        seen_attr_names: set[str] = set()
        for attr in obj.attributes:
            attr_name = attr.rm_attribute_name
            attr_path = f"{path}/{attr_name}"

            if attr_name in seen_attr_names:
                span = attr.span
                issues.append(
                    Issue(
                        code="AOM240",
                        severity=Severity.ERROR,
                        message=f"Duplicate attribute name '{attr_name}' in scope",
                        file=span.file if span else None,
                        line=span.start_line if span else None,
                        col=span.start_col if span else None,
                        end_line=span.end_line if span else None,
                        end_col=span.end_col if span else None,
                        path=attr_path,
                        node_id=obj.node_id,
                    )
                )
            else:
                seen_attr_names.add(attr_name)

            seen_child_node_ids: set[str] = set()
            for child in attr.children:
                if child.node_id is not None and child.node_id in seen_child_node_ids:
                    span = child.span
                    issues.append(
                        Issue(
                            code="AOM240",
                            severity=Severity.ERROR,
                            message=(
                                f"Duplicate node id '{child.node_id}' within attribute '{attr_name}'"
                            ),
                            file=span.file if span else None,
                            line=span.start_line if span else None,
                            col=span.start_col if span else None,
                            end_line=span.end_line if span else None,
                            end_col=span.end_col if span else None,
                            path=attr_path,
                            node_id=child.node_id,
                        )
                    )
                elif child.node_id is not None:
                    seen_child_node_ids.add(child.node_id)

                walk(child, path=attr_path)

    walk(artefact.definition, path="/definition")
    return tuple(issues)


def check_interval_invariants(ctx: ValidationContext) -> Iterable[Issue]:
    """AOM250: check min<=max and basic invariants.

    Applies to:
    - `CObject.occurrences`
    - `CAttribute.cardinality.occurrences`
    - primitive constraint intervals (integer/real)

    # Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
    """

    artefact = ctx.artefact
    if not isinstance(artefact, (Archetype, Template)):
        return ()

    if artefact.definition is None:
        return ()

    issues: list[Issue] = []

    def emit(
        *,
        message: str,
        span: SourceSpan | None,
        path: str,
        node_id: str | None,
    ) -> None:
        issues.append(
            Issue(
                code="AOM250",
                severity=Severity.ERROR,
                message=message,
                file=span.file if span else None,
                line=span.start_line if span else None,
                col=span.start_col if span else None,
                end_line=span.end_line if span else None,
                end_col=span.end_col if span else None,
                path=path,
                node_id=node_id,
            )
        )

    def check_interval(
        *,
        interval: Interval,
        path: str,
        node_id: str | None,
    ) -> None:
        lo = interval.lower
        hi = interval.upper

        # Invariant: if both bounds exist, lower <= upper.
        if lo is not None and hi is not None and lo > hi:
            emit(
                message=f"Invalid interval: lower bound {lo} exceeds upper bound {hi}",
                span=interval.span,
                path=path,
                node_id=node_id,
            )
            return

        # Invariant: if bounds are equal, interval must not be empty.
        if lo is not None and hi is not None and lo == hi:
            if not interval.lower_included or not interval.upper_included:
                emit(
                    message=(
                        "Invalid interval: empty interval when bounds are equal and one side is excluded"
                    ),
                    span=interval.span,
                    path=path,
                    node_id=node_id,
                )

    def walk(obj: CObject, *, path: str) -> None:
        if obj.occurrences is not None:
            check_interval(
                interval=obj.occurrences,
                path=f"{path}/occurrences",
                node_id=obj.node_id,
            )

        if isinstance(obj, CComplexObject):
            for attr in obj.attributes:
                attr_path = f"{path}/{attr.rm_attribute_name}"

                if attr.cardinality is not None:
                    check_interval(
                        interval=attr.cardinality.occurrences,
                        path=f"{attr_path}/cardinality",
                        node_id=obj.node_id,
                    )

                for child in attr.children:
                    walk(child, path=attr_path)

        if isinstance(obj, CPrimitiveObject):
            c = obj.constraint
            if isinstance(c, PrimitiveIntegerConstraint) and c.interval is not None:
                check_interval(
                    interval=c.interval,
                    path=f"{path}/constraint",
                    node_id=obj.node_id,
                )
            if isinstance(c, PrimitiveRealConstraint) and c.interval is not None:
                check_interval(
                    interval=c.interval,
                    path=f"{path}/constraint",
                    node_id=obj.node_id,
                )

    walk(artefact.definition, path="/definition")
    return tuple(issues)


def check_value_set_integrity(ctx: ValidationContext) -> Iterable[Issue]:
    """AOM260: validate value set references and emptiness rules.

    Rules (basic):
    - A value set must not be empty.
    - Every member code referenced by a value set must exist in terminology.

    # Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html#_archetype_terminology_class
    """

    artefact = ctx.artefact
    if not isinstance(artefact, (Archetype, Template)):
        return ()

    term = artefact.terminology
    if term is None:
        return ()

    defined = _defined_codes(term)
    issues: list[Issue] = []

    def emit(*, message: str, span: SourceSpan | None, path: str, node_id: str | None):
        issues.append(
            Issue(
                code="AOM260",
                severity=Severity.ERROR,
                message=message,
                file=span.file if span else None,
                line=span.start_line if span else None,
                col=span.start_col if span else None,
                end_line=span.end_line if span else None,
                end_col=span.end_col if span else None,
                path=path,
                node_id=node_id,
            )
        )

    for vs in term.value_sets:
        vs_path = f"/terminology/value_sets/{vs.id}"

        if len(vs.members) == 0:
            emit(
                message=f"Value set '{vs.id}' must not be empty",
                span=vs.span,
                path=vs_path,
                node_id=vs.id,
            )
            continue

        for member in vs.members:
            if member in defined:
                continue
            emit(
                message=(
                    f"Value set '{vs.id}' references undefined terminology code '{member}'"
                ),
                span=vs.span,
                path=vs_path,
                node_id=member,
            )

    return tuple(issues)


register_semantic_check(
    check_referenced_terminology_codes_exist,
    name="aom200_referenced_codes_exist_in_terminology",
)

register_semantic_check(
    check_node_id_format,
    name="aom210_node_id_format",
)

register_semantic_check(
    check_specialisation_depth_mismatch,
    name="aom230_specialisation_depth_mismatch",
)

register_semantic_check(
    check_duplicates_in_scopes,
    name="aom240_duplicates_in_scopes_basic",
)

register_semantic_check(
    check_interval_invariants,
    name="aom250_interval_invariants",
)

register_semantic_check(
    check_value_set_integrity,
    name="aom260_value_set_integrity",
)
