"""Default RM validation checks.

Each check in this module should be permissive and return `Issue` objects.

# Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
"""

from collections.abc import Iterable

from openehr_am.aom.archetype import Archetype, Template
from openehr_am.aom.constraints import CAttribute, CComplexObject, CObject
from openehr_am.bmm.repository import ModelRepository
from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.rm import register_rm_check


def _is_builtin_rm_type(name: str) -> bool:
    # Minimal set for primitive constraints.
    return name in {"String", "Integer", "Real", "Boolean"}


def check_rm_types_exist(ctx: ValidationContext) -> Iterable[Issue]:
    """Ensure referenced RM types exist in the provided repository.

    Emits:
        - BMM500: Unknown RM type referenced

    # Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
    """

    if ctx.rm_repo is None:
        return ()

    if not isinstance(ctx.rm_repo, ModelRepository):
        raise TypeError("RM validation requires rm_repo to be a ModelRepository")

    root = None
    match ctx.artefact:
        case Archetype(definition=definition):
            root = definition
        case Template(definition=definition):
            root = definition
        case CComplexObject() as definition:
            root = definition
        case _:
            return ()

    if root is None:
        return ()

    issues: list[Issue] = []
    _walk_cobject(root, ctx.rm_repo, issues)
    return tuple(issues)


def _walk_cobject(node: CObject, repo: ModelRepository, issues: list[Issue]) -> None:
    rm_type = node.rm_type_name

    if not _is_builtin_rm_type(rm_type) and repo.get_class(rm_type) is None:
        span = node.span
        issues.append(
            Issue(
                code="BMM500",
                severity=Severity.ERROR,
                message=f"Unknown RM type referenced: {rm_type!r}",
                file=span.file if span else None,
                line=span.start_line if span else None,
                col=span.start_col if span else None,
                end_line=span.end_line if span else None,
                end_col=span.end_col if span else None,
                node_id=node.node_id,
            )
        )

    # Recurse into complex object attributes.
    if isinstance(node, CComplexObject):
        for attr in node.attributes:
            _check_attribute_exists(node, attr, repo, issues)
            _walk_cattribute(attr, repo, issues)


def _walk_cattribute(
    attr: CAttribute, repo: ModelRepository, issues: list[Issue]
) -> None:
    for child in attr.children:
        _walk_cobject(child, repo, issues)


def _check_attribute_exists(
    parent: CObject,
    attr: CAttribute,
    repo: ModelRepository,
    issues: list[Issue],
) -> None:
    rm_type = parent.rm_type_name

    # If the type doesn't exist, BMM500 will already be emitted; don't cascade.
    if _is_builtin_rm_type(rm_type) or repo.get_class(rm_type) is None:
        return

    if repo.get_property_inherited(rm_type, attr.rm_attribute_name) is not None:
        return

    span = attr.span
    issues.append(
        Issue(
            code="BMM510",
            severity=Severity.ERROR,
            message=(
                f"Unknown RM attribute referenced: {attr.rm_attribute_name!r} "
                f"on type {rm_type!r}"
            ),
            file=span.file if span else None,
            line=span.start_line if span else None,
            col=span.start_col if span else None,
            end_line=span.end_line if span else None,
            end_col=span.end_col if span else None,
            node_id=parent.node_id,
        )
    )


register_rm_check(check_rm_types_exist, name="rm_types_exist")


def check_rm_attributes_exist(ctx: ValidationContext) -> Iterable[Issue]:
    """Ensure referenced RM attributes exist on the RM type.

    Emits:
        - BMM510: Unknown RM attribute referenced

    # Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
    """

    if ctx.rm_repo is None:
        return ()

    if not isinstance(ctx.rm_repo, ModelRepository):
        raise TypeError("RM validation requires rm_repo to be a ModelRepository")

    root = None
    match ctx.artefact:
        case Archetype(definition=definition):
            root = definition
        case Template(definition=definition):
            root = definition
        case CComplexObject() as definition:
            root = definition
        case _:
            return ()

    if root is None:
        return ()

    issues: list[Issue] = []
    # We re-walk the tree so this check is independent and composable.
    _walk_cobject(root, ctx.rm_repo, issues)
    return tuple(i for i in issues if i.code == "BMM510")


register_rm_check(check_rm_attributes_exist, name="rm_attributes_exist")
