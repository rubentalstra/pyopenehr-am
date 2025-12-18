"""Validation context.

Validation checks should accept a `ValidationContext` and return an iterable of
`Issue` objects.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ValidationContext:
    """Holds inputs for validation checks.

    Parameters
    ----------
    artefact:
        The artefact being validated (e.g., text, syntax AST, AOM object, OPT).
        The validation layer determines what type is expected.
    rm_repo:
        Optional RM repository (e.g., a loaded BMM repository) required for RM
        conformance checks.
    """

    artefact: object
    rm_repo: object | None = None
