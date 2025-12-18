"""AQL parsing utilities.

Public API in this package is intentionally small.

Currently supported:
- Syntax checking using the committed ANTLR4-generated parser.

# Spec: https://specifications.openehr.org/releases/QUERY/Release-1.1.0
"""

from .parser import check_aql_syntax

__all__ = [
    "check_aql_syntax",
]
