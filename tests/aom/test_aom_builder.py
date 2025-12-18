from openehr_am.adl import parse_adl
from openehr_am.adl.cadl_ast import CadlObjectNode
from openehr_am.aom.archetype import Archetype
from openehr_am.aom.builder import build_aom_from_adl
from openehr_am.aom.constraints import (
    CComplexObject,
    CPrimitiveObject,
    PrimitiveIntegerConstraint,
    PrimitiveRealConstraint,
    PrimitiveStringConstraint,
)
from tests.fixture_loader import load_fixture_text


def test_build_aom_from_adl_builds_archetype_definition_and_preserves_spans() -> None:
    text = load_fixture_text("adl", "minimal_cadl_definition.adl")

    artefact, issues = parse_adl(text, filename="cadl.adl")
    assert issues == []
    assert artefact is not None
    assert isinstance(artefact.definition, CadlObjectNode)

    aom, build_issues = build_aom_from_adl(artefact)
    assert build_issues == []
    assert isinstance(aom, Archetype)

    assert aom.definition is not None
    assert isinstance(aom.definition, CComplexObject)
    assert aom.definition.span == artefact.definition.span

    # Compare nested spans by following the same path in syntax and AOM.
    data_attr_syntax = next(
        a for a in artefact.definition.attributes if a.rm_attribute_name == "data"
    )
    history_syntax = data_attr_syntax.children[0]
    assert history_syntax.occurrences is not None

    data_attr_aom = next(
        a for a in aom.definition.attributes if a.rm_attribute_name == "data"
    )
    history_aom = data_attr_aom.children[0]
    assert history_aom.occurrences is not None

    assert history_aom.occurrences.span == history_syntax.occurrences.span

    items_attr_syntax = next(
        a for a in artefact.definition.attributes if a.rm_attribute_name == "items"
    )
    assert items_attr_syntax.cardinality is not None

    items_attr_aom = next(
        a for a in aom.definition.attributes if a.rm_attribute_name == "items"
    )
    assert items_attr_aom.cardinality is not None

    assert items_attr_aom.cardinality.span == items_attr_syntax.cardinality.span


def test_build_aom_from_adl_converts_primitives_without_leaking_syntax_ast() -> None:
    text = load_fixture_text("adl", "minimal_cadl_primitives.adl")

    artefact, issues = parse_adl(text, filename="cadl_primitives.adl")
    assert issues == []
    assert artefact is not None

    aom, build_issues = build_aom_from_adl(artefact)
    assert build_issues == []
    assert isinstance(aom, Archetype)
    assert aom.definition is not None

    name_attr = next(
        a for a in aom.definition.attributes if a.rm_attribute_name == "name"
    )
    name_obj = name_attr.children[0]
    assert isinstance(name_obj, CPrimitiveObject)
    assert isinstance(name_obj.constraint, PrimitiveStringConstraint)
    assert name_obj.constraint.pattern == "[A-Z][a-z]+"

    qty_attr = next(
        a for a in aom.definition.attributes if a.rm_attribute_name == "qty"
    )
    qty_obj = qty_attr.children[0]
    assert isinstance(qty_obj, CPrimitiveObject)
    assert isinstance(qty_obj.constraint, PrimitiveIntegerConstraint)
    assert qty_obj.constraint.values == (99,)
    assert qty_obj.constraint.interval is not None
    assert qty_obj.constraint.interval.lower == 0
    assert qty_obj.constraint.interval.upper == 10

    ratio_attr = next(
        a for a in aom.definition.attributes if a.rm_attribute_name == "ratio"
    )
    ratio_obj = ratio_attr.children[0]
    assert isinstance(ratio_obj, CPrimitiveObject)
    assert isinstance(ratio_obj.constraint, PrimitiveRealConstraint)
    assert ratio_obj.constraint.values == (2.5,)
    assert ratio_obj.constraint.interval is not None
    assert ratio_obj.constraint.interval.lower == 0.0
    assert ratio_obj.constraint.interval.upper == 1.0


def test_build_aom_from_adl_copies_rules_statements() -> None:
    from openehr_am.aom.archetype import RuleStatement

    text = load_fixture_text("adl", "minimal_archetype_with_rules.adl")

    artefact, issues = parse_adl(text, filename="rules.adl")
    assert issues == []
    assert artefact is not None

    aom, build_issues = build_aom_from_adl(artefact)
    assert build_issues == []
    assert isinstance(aom, Archetype)

    assert aom.rules
    assert all(isinstance(s, RuleStatement) for s in aom.rules)
    assert [s.text for s in aom.rules] == [
        "valid_rule_line_1",
        "valid_rule_line_2_with_indent",
    ]
    assert aom.rules[0].span is not None
    assert aom.rules[0].span.start_line == 16
