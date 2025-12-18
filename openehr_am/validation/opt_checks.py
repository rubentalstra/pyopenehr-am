"""OPT integrity checks.

This module contains checks for the OPT validation layer.

Current scope (MVP): internal consistency checks for `OperationalTemplate`.

# Spec: https://specifications.openehr.org/releases/AM/latest/OPT2.html
"""

from collections.abc import Iterable

from openehr_am.opt.model import (
    OperationalTemplate,
    OptCAttribute,
    OptCComplexObject,
    OptCObject,
)
from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue, Severity


def _opt750(
    *,
    message: str,
    path: str | None = None,
    span,
) -> Issue:
    return Issue(
        code="OPT750",
        severity=Severity.ERROR,
        message=message,
        file=span.file if span else None,
        line=span.start_line if span else None,
        col=span.start_col if span else None,
        end_line=span.end_line if span else None,
        end_col=span.end_col if span else None,
        path=path,
    )


def check_opt_integrity(ctx: ValidationContext) -> Iterable[Issue]:
    """Validate internal consistency of an OPT object.

    Notes:
        This check is intentionally conservative: it reports only structural
        invariants that should hold for any compiled OPT.
    """

    if not isinstance(ctx.artefact, OperationalTemplate):
        return ()

    opt = ctx.artefact
    issues: list[Issue] = []

    # Component archetype ids should be unique.
    seen: set[str] = set()
    dups: list[str] = []
    for a_id in opt.component_archetype_ids:
        if a_id in seen:
            dups.append(a_id)
        seen.add(a_id)

    for a_id in sorted(set(dups)):
        issues.append(
            _opt750(
                message=f"Duplicate archetype id in component_archetype_ids: {a_id!r}",
                span=opt.span,
            )
        )

    # Root archetype id should be part of components when both are present.
    if opt.root_archetype_id is not None and opt.component_archetype_ids:
        if opt.root_archetype_id not in set(opt.component_archetype_ids):
            issues.append(
                _opt750(
                    message=(
                        "root_archetype_id is not included in component_archetype_ids: "
                        f"{opt.root_archetype_id!r}"
                    ),
                    span=opt.span,
                )
            )

    if opt.definition is None:
        return tuple(issues)

    # Root definition should have a path and it should start at '/'.
    if opt.definition.path is None or not opt.definition.path.startswith("/"):
        issues.append(
            _opt750(
                message="OPT definition root has invalid or missing path",
                path=opt.definition.path,
                span=opt.definition.span or opt.span,
            )
        )

    # Walk tree deterministically and check paths + duplicates.
    all_object_paths: list[str] = []
    _check_object(
        opt.definition, parent_path=None, issues=issues, all_paths=all_object_paths
    )

    # Duplicate object paths indicate broken internal references.
    counts: dict[str, int] = {}
    for p in all_object_paths:
        counts[p] = counts.get(p, 0) + 1

    for p in sorted(k for k, v in counts.items() if v > 1):
        issues.append(
            _opt750(
                message=f"Duplicate object path in OPT definition: {p!r}",
                path=p,
                span=opt.definition.span or opt.span,
            )
        )

    return tuple(issues)


def _check_object(
    obj: OptCObject,
    *,
    parent_path: str | None,
    issues: list[Issue],
    all_paths: list[str],
) -> None:
    path = obj.path
    if path is None or not path.startswith("/"):
        issues.append(
            _opt750(
                message="OPT object has invalid or missing path",
                path=path,
                span=obj.span,
            )
        )
        return

    if parent_path is not None and not path.startswith(parent_path):
        issues.append(
            _opt750(
                message=(
                    "OPT object path is not under parent path: "
                    f"parent={parent_path!r}, child={path!r}"
                ),
                path=path,
                span=obj.span,
            )
        )

    if obj.node_id is not None and f"[{obj.node_id}]" not in path:
        issues.append(
            _opt750(
                message="OPT object node_id not reflected in path",
                path=path,
                span=obj.span,
            )
        )

    all_paths.append(path)

    if not isinstance(obj, OptCComplexObject):
        return

    # Attributes should have unique names within an object.
    attr_names = [a.rm_attribute_name for a in obj.attributes]
    for name in sorted({n for n in attr_names if attr_names.count(n) > 1}):
        issues.append(
            _opt750(
                message=f"Duplicate attribute name under object {path!r}: {name!r}",
                path=path,
                span=obj.span,
            )
        )

    for attr in sorted(obj.attributes, key=lambda a: a.rm_attribute_name):
        _check_attribute(attr, parent_object_path=path, issues=issues)
        for child in attr.children:
            _check_object(
                child,
                parent_path=attr.path or path,
                issues=issues,
                all_paths=all_paths,
            )


def _check_attribute(
    attr: OptCAttribute,
    *,
    parent_object_path: str,
    issues: list[Issue],
) -> None:
    if not attr.rm_attribute_name:
        issues.append(
            _opt750(
                message="OPT attribute has empty rm_attribute_name",
                path=attr.path,
                span=attr.span,
            )
        )
        return

    if attr.path is None:
        issues.append(
            _opt750(
                message="OPT attribute has missing path",
                path=None,
                span=attr.span,
            )
        )
        return

    expected_prefix = (
        f"{parent_object_path.rstrip('/')}/{attr.rm_attribute_name}"
        if parent_object_path != "/"
        else f"/{attr.rm_attribute_name}"
    )

    if attr.path != expected_prefix:
        issues.append(
            _opt750(
                message=(
                    "OPT attribute path mismatch: "
                    f"expected={expected_prefix!r}, actual={attr.path!r}"
                ),
                path=attr.path,
                span=attr.span,
            )
        )


__all__ = ["check_opt_integrity"]
