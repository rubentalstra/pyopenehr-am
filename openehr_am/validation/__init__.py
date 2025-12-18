"""Validation framework and rule checks.

This package provides infrastructure and checks that emit structured `Issue`
objects rather than raising exceptions for recoverable problems.
"""

from openehr_am.validation.context import ValidationContext
from openehr_am.validation.registry import ValidationLayer, ValidationRegistry
from openehr_am.validation.syntax import validate_syntax

__all__ = [
    "ValidationContext",
    "ValidationLayer",
    "ValidationRegistry",
    "validate_syntax",
]
