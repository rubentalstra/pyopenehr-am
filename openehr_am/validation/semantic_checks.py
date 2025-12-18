"""Default semantic validation checks.

Checks in this module are registered into the semantic DEFAULT_REGISTRY on
import.

# Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html#_archetype_terminology_class
"""

from collections.abc import Iterable, Iterator

from openehr_am.antlr.span import SourceSpan
from openehr_am.aom.archetype import Archetype, Template
from openehr_am.aom.constraints import CAttribute, CComplexObject, CObject
from openehr_am.aom.ids import is_ac_code, is_at_code
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
    if artefact.concept is not None and (
        is_at_code(artefact.concept) or is_ac_code(artefact.concept)
    ):
        yield artefact.concept, artefact.span

    if artefact.definition is None:
        return

    for obj in _iter_cobject_tree(artefact.definition):
        if obj.node_id is None:
            continue
        if is_at_code(obj.node_id) or is_ac_code(obj.node_id):
            yield obj.node_id, obj.span


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
            if is_at_code(b.code) or is_ac_code(b.code):
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


register_semantic_check(
    check_referenced_terminology_codes_exist,
    name="aom200_referenced_codes_exist_in_terminology",
)
