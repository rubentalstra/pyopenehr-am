"""ANTLR integration utilities.

This module provides small adapters around the ANTLR4 Python runtime.

Policy: parsing-layer code must never raise for invalid user input.
Instead, lexer/parser diagnostics are converted into `Issue` objects.
"""

from openehr_am.antlr.span import SourceSpan

__all__ = [
    "SourceSpan",
]
