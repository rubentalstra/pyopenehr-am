"""Validation registry.

This module provides a layered registry for validation checks.

Checks are executed in a deterministic order:
- By layer: syntax -> semantic -> rm -> opt
- Within a layer: priority (desc), name (asc), registration order (asc)

The resulting issues are returned in a deterministic order via IssueCollector.
"""

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum

from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue
from openehr_am.validation.issue_collector import IssueCollector


class ValidationLayer(StrEnum):
    """Validation pipeline layers."""

    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    RM = "rm"
    OPT = "opt"


type ValidationCheck = Callable[[ValidationContext], Iterable[Issue]]


_LAYER_ORDER: tuple[ValidationLayer, ...] = (
    ValidationLayer.SYNTAX,
    ValidationLayer.SEMANTIC,
    ValidationLayer.RM,
    ValidationLayer.OPT,
)


@dataclass(slots=True, frozen=True)
class _Registration:
    layer: ValidationLayer
    name: str
    priority: int
    order: int
    check: ValidationCheck


def _registration_sort_key(reg: _Registration) -> tuple[int, str, int]:
    return (-reg.priority, reg.name, reg.order)


class ValidationRegistry:
    """Register and run validation checks by layer."""

    def __init__(self) -> None:
        self._registrations: dict[ValidationLayer, list[_Registration]] = {
            layer: [] for layer in _LAYER_ORDER
        }
        self._next_order = 0

    def register(
        self,
        layer: ValidationLayer,
        check: ValidationCheck,
        *,
        name: str | None = None,
        priority: int = 0,
    ) -> None:
        """Register a check in the given layer."""

        if layer not in self._registrations:
            # Programmer error: layer must be a known ValidationLayer.
            raise ValueError(f"Unsupported validation layer: {layer!r}")

        check_name = name or getattr(check, "__name__", "<check>")
        reg = _Registration(
            layer=layer,
            name=check_name,
            priority=priority,
            order=self._next_order,
            check=check,
        )
        self._next_order += 1
        self._registrations[layer].append(reg)

    def run(
        self,
        ctx: ValidationContext,
        *,
        layers: Sequence[ValidationLayer] | None = None,
    ) -> tuple[Issue, ...]:
        """Run checks for the given layers and return deterministically-ordered Issues."""

        selected_layers = self._select_layers(layers)

        collector = IssueCollector()
        for layer in selected_layers:
            regs = sorted(self._registrations[layer], key=_registration_sort_key)
            for reg in regs:
                collector.extend(reg.check(ctx))

        return collector.issues

    def _select_layers(
        self, layers: Sequence[ValidationLayer] | None
    ) -> tuple[ValidationLayer, ...]:
        if layers is None:
            return _LAYER_ORDER

        wanted = set(layers)
        return tuple(layer for layer in _LAYER_ORDER if layer in wanted)
