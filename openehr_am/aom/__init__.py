"""AOM (Archetype Object Model) domain objects.

This package defines *semantic-layer* data structures used after parsing.

Notes:
    - These are intentionally small, typed dataclasses.
    - Validation of user artefacts belongs in `openehr_am/validation/` and should
      emit `Issue` objects.
"""

from openehr_am.aom.archetype import Archetype, Template
from openehr_am.aom.constraints import (
    Cardinality,
    CAttribute,
    CComplexObject,
    CObject,
    CPrimitiveObject,
    Interval,
)
from openehr_am.aom.debug_dict import aom_to_dict
from openehr_am.aom.ids import (
    ArchetypeId,
    NodeId,
    NodeIdKind,
    NodeIdPrefix,
    format_node_id,
    is_ac_code,
    is_archetype_id,
    is_at_code,
    is_node_id,
    try_parse_archetype_id,
    try_parse_node_id,
)
from openehr_am.aom.repository import ArchetypeRepository
from openehr_am.aom.terminology import (
    ArchetypeTerminology,
    TermBinding,
    TermDefinition,
    ValueSet,
)

__all__ = [
    "Archetype",
    "Template",
    "ArchetypeRepository",
    "ArchetypeTerminology",
    "TermBinding",
    "TermDefinition",
    "ValueSet",
    "Interval",
    "Cardinality",
    "CObject",
    "CPrimitiveObject",
    "CAttribute",
    "CComplexObject",
    "NodeIdPrefix",
    "NodeIdKind",
    "NodeId",
    "is_node_id",
    "is_at_code",
    "is_ac_code",
    "try_parse_node_id",
    "format_node_id",
    "ArchetypeId",
    "try_parse_archetype_id",
    "is_archetype_id",
    "aom_to_dict",
]
