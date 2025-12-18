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

from pathlib import Path

from openehr_am.aom.archetype import Template
from openehr_am.aom.repository import ArchetypeRepository
from openehr_am.opt.dependencies import dependency_order_for_archetypes
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

    # Missing parent dependencies.
    for a in repo.archetypes:
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

    order, dep_issues = dependency_order_for_archetypes(repo.archetypes)
    issues.extend(dep_issues)

    if any(i.severity is Severity.ERROR for i in issues):
        return None, issues

    # Best-effort root: the most dependent archetype (last in dependency order).
    root_archetype_id = order[-1] if order else None

    opt = OperationalTemplate(
        template_id=template.template_id,
        concept=template.concept,
        original_language=template.original_language,
        language=template.languages[0] if template.languages else None,
        root_archetype_id=root_archetype_id,
        component_archetype_ids=order,
        definition=None,
        span=template.span,
    )

    return opt, issues


__all__ = ["compile_opt"]
