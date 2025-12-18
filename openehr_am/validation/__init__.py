"""Validation framework and rule checks.

This package provides infrastructure and checks that emit structured `Issue`
objects rather than raising exceptions for recoverable problems.

Note:
    Keep this module lightweight: importing submodules like
    `openehr_am.validation.issue` must not trigger heavy imports or introduce
    cycles with parsing/loading modules.
"""

__all__ = []
