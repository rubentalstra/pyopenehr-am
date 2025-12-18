"""AOM (Archetype Object Model) domain objects.

This package defines *semantic-layer* data structures used after parsing.

Notes:
    - These are intentionally small, typed dataclasses.
    - Validation of user artefacts belongs in `openehr_am/validation/` and should
      emit `Issue` objects.
"""

from openehr_am.aom.archetype import Archetype, Template
from openehr_am.aom.constraints import (
    CAttribute,
    CComplexObject,
    CObject,
    CPrimitiveObject,
    Cardinality,
    Interval,
)
from openehr_am.aom.terminology import ArchetypeTerminology, TermBinding, TermDefinition

__all__ = [
    "Archetype",
    "Template",
    "ArchetypeTerminology",
    "TermBinding",
    "TermDefinition",
    "Interval",
    "Cardinality",
    "CObject",
    "CPrimitiveObject",
    "CAttribute",
    "CComplexObject",
]
