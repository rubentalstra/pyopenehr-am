import dataclasses

import pytest

from openehr_am.aom import (
    Archetype,
    ArchetypeTerminology,
    Cardinality,
    CAttribute,
    CComplexObject,
    Interval,
    Template,
    TermBinding,
    TermDefinition,
)


def test_aom_models_are_slots_and_frozen() -> None:
    term = TermDefinition(language="en", code="at0000", text="Problem")

    assert hasattr(term, "__slots__")

    with pytest.raises(dataclasses.FrozenInstanceError):
        term.text = "Changed"  # pyright: ignore[reportAttributeAccessIssue]


def test_archetype_wires_definition_and_terminology() -> None:
    attr = CAttribute(
        rm_attribute_name="items",
        existence=Interval(0, None),
        cardinality=Cardinality(
            occurrences=Interval(0, None), is_ordered=False, is_unique=False
        ),
        children=(),
    )
    definition = CComplexObject(
        rm_type_name="OBSERVATION", node_id="at0000", attributes=(attr,)
    )

    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(TermDefinition(language="en", code="at0000", text="Root"),),
        term_bindings=(
            TermBinding(terminology="SNOMED-CT", code="at0000", target="123456"),
        ),
    )

    arch = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.example.v1",
        concept="at0000",
        original_language="en",
        languages=("en",),
        definition=definition,
        terminology=terminology,
    )

    assert arch.definition is definition
    assert arch.terminology is terminology
    assert arch.definition is not None
    assert arch.definition.attributes[0].rm_attribute_name == "items"


def test_template_minimal_construction() -> None:
    template = Template(template_id="example_template.v1")
    assert template.template_id == "example_template.v1"
