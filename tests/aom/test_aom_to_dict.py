import json

from openehr_am.antlr.span import SourceSpan
from openehr_am.aom import aom_to_dict
from openehr_am.aom.archetype import Archetype
from openehr_am.aom.constraints import (
    CAttribute,
    CComplexObject,
    CPrimitiveObject,
    Interval,
    PrimitiveIntegerConstraint,
)
from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition


def test_aom_to_dict_is_deterministic_and_json_serializable() -> None:
    span = SourceSpan(file="x.adl", start_line=1, start_col=1, end_line=1, end_col=2)

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        occurrences=Interval(0, 1, span=span),
        span=span,
        attributes=(
            CAttribute(
                rm_attribute_name="count",
                children=(
                    CPrimitiveObject(
                        rm_type_name="Integer",
                        constraint=PrimitiveIntegerConstraint(
                            interval=Interval(0, 10, span=span), span=span
                        ),
                        span=span,
                    ),
                ),
                span=span,
            ),
        ),
    )

    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(
            TermDefinition(language="en", code="at0000", text="Root", span=span),
        ),
        span=span,
    )

    archetype = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.example.v1",
        concept="at0000",
        original_language="en",
        languages=("en",),
        definition=definition,
        terminology=terminology,
        span=span,
    )

    d1 = archetype.to_dict()
    d2 = archetype.to_dict()
    assert d1 == d2

    # Key ordering is deterministic (dict preserves insertion order).
    assert list(d1.keys()) == [
        "archetype_id",
        "parent_archetype_id",
        "concept",
        "original_language",
        "languages",
        "definition",
        "terminology",
        "rules",
        "span",
    ]

    def_dict = d1["definition"]
    assert isinstance(def_dict, dict)
    assert list(def_dict.keys()) == [
        "rm_type_name",
        "node_id",
        "occurrences",
        "span",
        "attributes",
    ]

    # Generic helper produces same output.
    assert aom_to_dict(archetype) == d1

    # Must be JSON serializable.
    json.dumps(d1)
