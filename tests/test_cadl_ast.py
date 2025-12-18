import dataclasses

import pytest

from openehr_am.adl.cadl_ast import (
    CadlAttributeNode,
    CadlBooleanConstraint,
    CadlCardinality,
    CadlIntegerConstraint,
    CadlIntegerInterval,
    CadlObjectNode,
    CadlOccurrences,
    CadlRealConstraint,
    CadlRealInterval,
    CadlStringConstraint,
)
from openehr_am.antlr.span import SourceSpan


def test_nodes_are_frozen_slots_dataclasses() -> None:
    assert dataclasses.is_dataclass(CadlObjectNode)
    node = CadlObjectNode(rm_type_name="OBSERVATION")

    assert not hasattr(node, "__dict__")
    with pytest.raises(dataclasses.FrozenInstanceError):
        node.rm_type_name = "EVALUATION"  # type: ignore[misc]


def test_object_nodes_capture_type_node_id_occurrences_and_attributes() -> None:
    span = SourceSpan(file="x.adl", start_line=1, start_col=1, end_line=1, end_col=10)

    occurrences = CadlOccurrences(lower=0, upper=1, span=span)
    cardinality = CadlCardinality(lower=0, upper=None, upper_unbounded=True, span=span)

    leaf = CadlObjectNode(
        rm_type_name="ELEMENT",
        node_id="at0001",
        occurrences=occurrences,
        attributes=(),
        span=span,
    )

    attribute = CadlAttributeNode(
        rm_attribute_name="items",
        children=(leaf,),
        cardinality=cardinality,
        span=span,
    )

    root = CadlObjectNode(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        attributes=(attribute,),
        span=span,
    )

    assert root.rm_type_name == "OBSERVATION"
    assert root.node_id == "at0000"
    assert root.attributes[0].rm_attribute_name == "items"
    assert root.attributes[0].children[0].rm_type_name == "ELEMENT"
    assert root.attributes[0].children[0].occurrences == occurrences
    assert root.attributes[0].cardinality == cardinality


def test_primitive_constraints_can_be_attached_to_object_nodes() -> None:
    span = SourceSpan(file=None, start_line=1, start_col=1, end_line=1, end_col=1)

    s = CadlStringConstraint(values=("a", "b"), pattern="^[ab]$", span=span)
    i = CadlIntegerConstraint(interval=CadlIntegerInterval(0, 10, span=span), span=span)
    r = CadlRealConstraint(
        values=(0.1, 0.2), interval=CadlRealInterval(0.0, 1.0), span=span
    )
    b = CadlBooleanConstraint(values=(True,), span=span)

    assert s.values == ("a", "b")
    assert i.interval is not None
    assert r.interval is not None
    assert b.values == (True,)

    primitive_object = CadlObjectNode(
        rm_type_name="Integer",
        primitive=i,
        attributes=(),
        span=span,
    )

    assert primitive_object.primitive is i
    assert primitive_object.attributes == ()
