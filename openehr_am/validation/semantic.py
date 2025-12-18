"""Semantic validation entrypoints.

This module provides a small registry for semantic checks.

Checks registered here are executed using the shared `ValidationRegistry`
infrastructure, but restricted to the `semantic` layer.

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


def register_semantic_check(
    check: ValidationCheck,
    *,
    name: str | None = None,
    priority: int = 0,
    registry: ValidationRegistry | None = None,
) -> None:
    """Register a semantic validation check.

    Args:
        check: Callable that accepts ValidationContext and yields Issues.
        name: Optional stable name used for deterministic ordering.
        priority: Higher runs earlier within the layer.
        registry: Optional registry to register into (defaults to DEFAULT_REGISTRY).
    """

    target = registry or DEFAULT_REGISTRY
    target.register(ValidationLayer.SEMANTIC, check, name=name, priority=priority)


def validate_semantic(
    aom_obj: object,
    *,
    registry: ValidationRegistry | None = None,
) -> tuple[Issue, ...]:
    """Run registered semantic checks for an AOM object.

    Args:
        aom_obj: The semantic (AOM) object to validate.
        registry: Optional registry to use (defaults to DEFAULT_REGISTRY).

    Returns:
        Tuple of Issues, deterministically ordered.
    """

    ctx = ValidationContext(artefact=aom_obj)
    runner = registry or DEFAULT_REGISTRY
    return runner.run(ctx, layers=[ValidationLayer.SEMANTIC])


# Import default semantic checks (registers into DEFAULT_REGISTRY).
#
# This keeps `validate_semantic()` useful out of the box, while still allowing
# tests to monkeypatch DEFAULT_REGISTRY for isolation.
import openehr_am.validation.semantic_checks as _semantic_checks  # noqa: E402

del _semantic_checks
