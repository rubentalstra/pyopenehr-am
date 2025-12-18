"""OPT compilation (MVP).

This module contains a minimal `compile_opt` implementation.

Current supported features:
    - Load archetypes from an `.adl` repository directory.
    - Resolve specialisation-parent dependencies.
    - Emit `OPT700` when a referenced parent archetype is missing.
    - Produce deterministic `OperationalTemplate` output.

Future compilation steps (not yet implemented):
    - Resolve template includes and slot filling.
    - Flatten constraints into OPT form.

# Spec: https://specifications.openehr.org/releases/AM/latest/OPT2.html
"""

import re
from pathlib import Path

from openehr_am.aom.archetype import Template
from openehr_am.aom.constraints import CArchetypeSlot, CComplexObject, CObject
from openehr_am.aom.repository import ArchetypeRepository
from openehr_am.opt.dependencies import dependency_order_for_archetypes
from openehr_am.opt.flattening import (
    aom_definition_to_opt,
    flatten_specialisation_definition,
)
from openehr_am.opt.model import OperationalTemplate
from openehr_am.validation.issue import Issue, Severity


def compile_opt(
    template: Template,
    *,
    archetype_dir: str | Path,
) -> tuple[OperationalTemplate | None, list[Issue]]:
    """Compile an ADL Template into an OPT (subset).

    Args:
        template: AOM Template object.
        archetype_dir: Directory containing `.adl` archetype files.

    Returns:
        `(opt, issues)` where `opt` is `None` if compilation cannot proceed.
    """

    repo, issues = ArchetypeRepository.load_from_dir(archetype_dir)

    selected_ids: tuple[str, ...] = ()
    slot_issues: list[Issue] = []
    if template.definition is not None:
        selected_ids, slot_issues = _fill_slots(template.definition, repo)
        issues.extend(slot_issues)

    if any(i.severity is Severity.ERROR for i in issues):
        return None, issues

    # Decide compilation scope.
    # - When slots are present and successfully resolved: compile only the
    #   selected archetypes plus their specialisation dependencies.
    # - Otherwise (MVP behavior): compile all archetypes in the directory.
    archetypes = repo.archetypes
    if selected_ids:
        needed_ids = _dependency_closure_for_ids(repo, selected_ids)
        archetypes = tuple(a for a in repo.archetypes if a.archetype_id in needed_ids)

    # Missing parent dependencies.
    for a in archetypes:
        parent = a.parent_archetype_id
        if parent is None:
            continue
        if repo.get(parent) is not None:
            continue

        span = a.span
        issues.append(
            Issue(
                code="OPT700",
                severity=Severity.ERROR,
                message=(
                    f"Cannot resolve archetype dependency: missing parent {parent!r} "
                    f"referenced by {a.archetype_id!r}"
                ),
                file=span.file if span else None,
                line=span.start_line if span else None,
                col=span.start_col if span else None,
                end_line=span.end_line if span else None,
                end_col=span.end_col if span else None,
                node_id=a.concept,
            )
        )

    if any(i.severity is Severity.ERROR for i in issues):
        return None, issues

    order, dep_issues = dependency_order_for_archetypes(archetypes)
    issues.extend(dep_issues)

    if any(i.severity is Severity.ERROR for i in issues):
        return None, issues

    # Best-effort root: the most dependent archetype (last in dependency order).
    root_archetype_id = order[-1] if order else None

    definition = None
    if root_archetype_id is not None:
        root = repo.get(root_archetype_id)
        if root is not None and root.definition is not None:
            flattened, flat_issues = flatten_specialisation_definition(root, repo)
            issues.extend(flat_issues)
            if any(i.severity is Severity.ERROR for i in issues):
                return None, issues
            if flattened is not None:
                definition = aom_definition_to_opt(
                    flattened,
                    root_path="/",
                    source_archetype_id=root_archetype_id,
                )

    opt = OperationalTemplate(
        template_id=template.template_id,
        concept=template.concept,
        original_language=template.original_language,
        language=template.languages[0] if template.languages else None,
        root_archetype_id=root_archetype_id,
        component_archetype_ids=order,
        definition=definition,
        span=template.span,
    )

    return opt, issues


def _dependency_closure_for_ids(
    repo: ArchetypeRepository, seed_ids: tuple[str, ...]
) -> set[str]:
    index = {a.archetype_id: a for a in repo.archetypes}
    needed: set[str] = set()
    stack = list(seed_ids)

    while stack:
        current = stack.pop()
        if current in needed:
            continue
        needed.add(current)

        a = index.get(current)
        if a is None:
            continue
        parent = a.parent_archetype_id
        if parent is not None and parent not in needed:
            stack.append(parent)

    return needed


def _iter_cobjects(node: CObject) -> tuple[CObject, ...]:
    if isinstance(node, CComplexObject):
        out: list[CObject] = [node]
        for attr in node.attributes:
            for child in attr.children:
                out.extend(_iter_cobjects(child))
        return tuple(out)

    return (node,)


def _fill_slots(
    definition: CComplexObject,
    repo: ArchetypeRepository,
) -> tuple[tuple[str, ...], list[Issue]]:
    issues: list[Issue] = []
    selected: list[str] = []

    for node in _iter_cobjects(definition):
        if not isinstance(node, CArchetypeSlot):
            continue

        matches = [
            a.archetype_id
            for a in repo.archetypes
            if _slot_matches(a.archetype_id, node)
        ]

        if not matches:
            span = node.span
            includes = ", ".join(p.value for p in node.includes) or "<none>"
            excludes = ", ".join(p.value for p in node.excludes) or "<none>"
            issues.append(
                Issue(
                    code="OPT720",
                    severity=Severity.ERROR,
                    message=(
                        "Slot filling failed: no matching archetype. "
                        f"include={includes}; exclude={excludes}"
                    ),
                    file=span.file if span else None,
                    line=span.start_line if span else None,
                    col=span.start_col if span else None,
                    end_line=span.end_line if span else None,
                    end_col=span.end_col if span else None,
                    node_id=node.node_id,
                )
            )
            continue

        chosen = sorted(matches)[0]
        selected.append(chosen)

    # De-dup deterministically.
    return tuple(sorted(set(selected))), issues


def _slot_matches(archetype_id: str, slot: CArchetypeSlot) -> bool:
    if slot.includes and not any(
        _pattern_matches(archetype_id, p.kind, p.value) for p in slot.includes
    ):
        return False
    if slot.excludes and any(
        _pattern_matches(archetype_id, p.kind, p.value) for p in slot.excludes
    ):
        return False
    return True


def _pattern_matches(value: str, kind: str, pattern: str) -> bool:
    if kind == "exact":
        return value == pattern
    if kind == "regex":
        try:
            return re.fullmatch(pattern, value) is not None
        except re.error:
            # Invalid regex patterns are treated as non-matching at compile time.
            return False
    return False


__all__ = ["compile_opt"]
