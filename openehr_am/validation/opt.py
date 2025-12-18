"""OPT validation entrypoints.

This module provides a small registry for OPT-level checks.

Checks registered here are executed using the shared `ValidationRegistry`
infrastructure, but restricted to the `opt` layer.

# Spec: https://specifications.openehr.org/releases/AM/latest/OPT2.html
"""

from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue
from openehr_am.validation.registry import (
    ValidationCheck,
    ValidationLayer,
    ValidationRegistry,
)

DEFAULT_REGISTRY = ValidationRegistry()


def register_opt_check(
    check: ValidationCheck,
    *,
    name: str | None = None,
    priority: int = 0,
    registry: ValidationRegistry | None = None,
) -> None:
    """Register an OPT validation check."""

    target = registry or DEFAULT_REGISTRY
    target.register(ValidationLayer.OPT, check, name=name, priority=priority)


def validate_opt(
    opt: object,
    *,
    registry: ValidationRegistry | None = None,
) -> tuple[Issue, ...]:
    """Run registered OPT checks.

    Args:
        opt: OPT object (typically an `OperationalTemplate`).
        registry: Optional registry to use (defaults to DEFAULT_REGISTRY).

    Returns:
        Tuple of Issues, deterministically ordered.
    """

    ctx = ValidationContext(artefact=opt)
    runner = registry or DEFAULT_REGISTRY
    return runner.run(ctx, layers=[ValidationLayer.OPT])


# Import default opt checks (registers into DEFAULT_REGISTRY).
import openehr_am.validation.opt_checks as _opt_checks  # noqa: E402

register_opt_check(_opt_checks.check_opt_integrity, name="opt_integrity", priority=0)

del _opt_checks
