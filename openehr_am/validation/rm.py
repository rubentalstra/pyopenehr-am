"""RM conformance validation entrypoints.

This layer validates AOM constraints against a loaded RM repository (BMM).

# Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
"""

from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue
from openehr_am.validation.registry import (
    ValidationCheck,
    ValidationLayer,
    ValidationRegistry,
)

DEFAULT_REGISTRY = ValidationRegistry()


def register_rm_check(
    check: ValidationCheck,
    *,
    name: str | None = None,
    priority: int = 0,
    registry: ValidationRegistry | None = None,
) -> None:
    """Register an RM conformance check."""

    target = registry or DEFAULT_REGISTRY
    target.register(ValidationLayer.RM, check, name=name, priority=priority)


def validate_rm(
    aom_obj: object,
    *,
    rm_repo: object | None,
    registry: ValidationRegistry | None = None,
) -> tuple[Issue, ...]:
    """Run registered RM checks for an AOM object.

    Args:
        aom_obj: A semantic (AOM) object, typically an `Archetype` or `Template`.
        rm_repo: RM repository (e.g. `ModelRepository`) used for lookups.
        registry: Optional registry to use (defaults to DEFAULT_REGISTRY).

    Returns:
        Tuple of Issues, deterministically ordered.
    """

    ctx = ValidationContext(artefact=aom_obj, rm_repo=rm_repo)
    runner = registry or DEFAULT_REGISTRY
    return runner.run(ctx, layers=[ValidationLayer.RM])


# Import default RM checks (registers into DEFAULT_REGISTRY).
import openehr_am.validation.rm_checks as _rm_checks  # noqa: E402

del _rm_checks


__all__ = [
    "DEFAULT_REGISTRY",
    "register_rm_check",
    "validate_rm",
]
