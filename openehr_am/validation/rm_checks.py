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


def _iter_cobjects(root: CObject) -> Iterable[CObject]:
    yield root
    if isinstance(root, CComplexObject):
        for attr in root.attributes:
            for child in attr.children:
                yield from _iter_cobjects(child)


def _iter_attributes(root: CObject) -> Iterable[tuple[CObject, CAttribute]]:
    if isinstance(root, CComplexObject):
        for attr in root.attributes:
            yield root, attr
            for child in attr.children:
                yield from _iter_attributes(child)


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
    for node in _iter_cobjects(root):
        rm_type = node.rm_type_name
        if _is_builtin_rm_type(rm_type):
            continue
        if ctx.rm_repo.get_class(rm_type) is not None:
            continue

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
    return tuple(issues)


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
    for parent, attr in _iter_attributes(root):
        _check_attribute_exists(parent, attr, ctx.rm_repo, issues)
    return tuple(issues)


register_rm_check(check_rm_attributes_exist, name="rm_attributes_exist")


def _bounds_from_aom_attribute(attr: CAttribute) -> tuple[int, int | None] | None:
    if attr.cardinality is not None:
        occ = attr.cardinality.occurrences
        lower = occ.lower
        upper = occ.upper
        if lower is not None and not isinstance(lower, int):
            return None
        if upper is not None and not isinstance(upper, int):
            return None
        return (lower or 0, upper)

    if attr.existence is not None:
        ex = attr.existence
        lower = ex.lower
        upper = ex.upper
        if lower is not None and not isinstance(lower, int):
            return None
        if upper is not None and not isinstance(upper, int):
            return None
        # Existence defaults to 0..1.
        return (lower or 0, upper if upper is not None else 1)

    return None


def _upper_exceeds(aom_upper: int | None, rm_upper: int | None) -> bool:
    if rm_upper is None:
        return False
    if aom_upper is None:
        return True
    return aom_upper > rm_upper


def check_rm_multiplicity_within_rm(ctx: ValidationContext) -> Iterable[Issue]:
    """Ensure AOM attribute multiplicity stays within RM multiplicity (subset).

    Subset:
        - Uses `CAttribute.cardinality.occurrences` when present
        - Otherwise uses `CAttribute.existence` (defaults 0..1)
        - If neither is present, no multiplicity constraint is checked

    Emits:
        - BMM520: Multiplicity mismatch

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
    for parent, attr in _iter_attributes(root):
        rm_type = parent.rm_type_name
        if _is_builtin_rm_type(rm_type) or ctx.rm_repo.get_class(rm_type) is None:
            continue

        rm_prop = ctx.rm_repo.get_property_inherited(rm_type, attr.rm_attribute_name)
        if rm_prop is None:
            # BMM510 handles unknown attributes.
            continue

        aom_bounds = _bounds_from_aom_attribute(attr)
        if aom_bounds is None:
            continue

        aom_lower, aom_upper = aom_bounds
        rm_lower = rm_prop.multiplicity.lower
        rm_upper = rm_prop.multiplicity.upper

        if aom_lower < rm_lower or _upper_exceeds(aom_upper, rm_upper):
            span = attr.span
            issues.append(
                Issue(
                    code="BMM520",
                    severity=Severity.ERROR,
                    message=(
                        "Multiplicity mismatch for RM attribute "
                        f"{attr.rm_attribute_name!r} on type {rm_type!r}: "
                        f"AOM allows {aom_lower}..{aom_upper if aom_upper is not None else '*'}, "
                        f"RM allows {rm_lower}..{rm_upper if rm_upper is not None else '*'}"
                    ),
                    file=span.file if span else None,
                    line=span.start_line if span else None,
                    col=span.start_col if span else None,
                    end_line=span.end_line if span else None,
                    end_col=span.end_col if span else None,
                    node_id=parent.node_id,
                )
            )

    return tuple(issues)


register_rm_check(check_rm_multiplicity_within_rm, name="rm_multiplicity_within_rm")
