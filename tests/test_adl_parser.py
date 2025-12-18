from openehr_am.adl import ArtefactKind, parse_adl
from openehr_am.adl.ast import AdlRulesSection
from openehr_am.adl.cadl_ast import (
    CadlIntegerConstraint,
    CadlObjectNode,
    CadlRealConstraint,
    CadlStringConstraint,
)
from openehr_am.validation.issue import Severity
from tests.fixture_loader import load_fixture_text


def test_parse_adl_minimal_archetype_extracts_sections_and_spans() -> None:
    text = load_fixture_text("adl", "minimal_archetype.adl")

    artefact, issues = parse_adl(text, filename="test.adl")

    assert issues == []
    assert artefact is not None
    assert artefact.kind is ArtefactKind.ARCHETYPE
    assert artefact.artefact_id == "openEHR-EHR-OBSERVATION.test.v1"

    assert artefact.original_language == "en"
    assert artefact.language == "en"

    assert artefact.description is not None
    assert artefact.terminology is not None

    # Spans should be shifted to file coordinates, not section-local line 1.
    assert artefact.description.span is not None
    assert artefact.description.span.start_line == 9

    assert artefact.terminology.span is not None
    assert artefact.terminology.span.start_line == 12

    assert artefact.definition is not None
    assert artefact.definition.span is not None
    assert artefact.definition.span.start_line == 14


def test_parse_adl_minimal_template_extracts_id_and_odins() -> None:
    text = load_fixture_text("adl", "minimal_template.adl")

    artefact, issues = parse_adl(text, filename="template.adl")

    assert issues == []
    assert artefact is not None
    assert artefact.kind is ArtefactKind.TEMPLATE
    assert artefact.artefact_id == "openEHR-EHR-COMPOSITION.test_template.v1"


def test_parse_adl_captures_rules_section_with_statement_spans() -> None:
    text = load_fixture_text("adl", "minimal_archetype_with_rules.adl")

    artefact, issues = parse_adl(text, filename="rules.adl")

    assert issues == []
    assert artefact is not None
    assert artefact.kind is ArtefactKind.ARCHETYPE
    assert artefact.artefact_id == "openEHR-EHR-OBSERVATION.test_with_rules.v1"

    assert isinstance(artefact.rules, AdlRulesSection)
    assert artefact.rules.header_span is not None
    assert artefact.rules.header_span.start_line == 14

    # Content starts on the line after the header.
    assert artefact.rules.span is not None
    assert artefact.rules.span.start_line == 15

    # Statements: ignore comment/blank lines and keep best-effort spans.
    assert [s.text for s in artefact.rules.statements] == [
        "valid_rule_line_1",
        "valid_rule_line_2_with_indent",
    ]
    assert artefact.rules.statements[0].span is not None
    assert artefact.rules.statements[0].span.start_line == 16
    assert artefact.rules.statements[1].span is not None
    assert artefact.rules.statements[1].span.start_line == 17


def test_parse_adl_invalid_missing_id_returns_issue() -> None:
    text = load_fixture_text("adl", "invalid_missing_id.adl")

    artefact, issues = parse_adl(text, filename="invalid.adl")

    assert artefact is None
    assert issues
    assert issues[0].code == "ADL001"
    assert issues[0].severity is Severity.ERROR


def test_parse_adl_invalid_odin_in_description_shifts_issue_line() -> None:
    text = load_fixture_text("adl", "invalid_bad_odin_description.adl")

    artefact, issues = parse_adl(text, filename="bad_odin.adl")

    assert artefact is not None
    assert issues
    # The embedded ODIN parser emits ODN100; ADL shifts it to file coordinates.
    assert issues[0].code == "ODN100"
    assert issues[0].file == "bad_odin.adl"
    assert issues[0].line == 8


def test_parse_adl_parses_minimal_definition_subset_into_cadl_ast() -> None:
    text = load_fixture_text("adl", "minimal_cadl_definition.adl")

    artefact, issues = parse_adl(text, filename="cadl.adl")

    assert issues == []
    assert artefact is not None

    assert isinstance(artefact.definition, CadlObjectNode)
    assert artefact.definition.rm_type_name == "OBSERVATION"
    assert artefact.definition.node_id == "at0000"

    # data matches { HISTORY[at0001] matches { occurrences matches {0..1} } }
    data_attr = next(
        a for a in artefact.definition.attributes if a.rm_attribute_name == "data"
    )
    assert data_attr.children[0].rm_type_name == "HISTORY"
    assert data_attr.children[0].node_id == "at0001"
    assert data_attr.children[0].occurrences is not None
    assert data_attr.children[0].occurrences.lower == 0
    assert data_attr.children[0].occurrences.upper == 1

    # items matches { cardinality matches {0..*; ordered; unique} ELEMENT[at0002] }
    items_attr = next(
        a for a in artefact.definition.attributes if a.rm_attribute_name == "items"
    )
    assert items_attr.cardinality is not None
    assert items_attr.cardinality.lower == 0
    assert items_attr.cardinality.upper is None
    assert items_attr.cardinality.upper_unbounded is True
    assert items_attr.cardinality.is_ordered is True
    assert items_attr.cardinality.is_unique is True
    assert items_attr.children[0].rm_type_name == "ELEMENT"
    assert items_attr.children[0].node_id == "at0002"

    # count matches { Integer matches {0..10} }
    count_attr = next(
        a for a in artefact.definition.attributes if a.rm_attribute_name == "count"
    )
    integer_obj = count_attr.children[0]
    assert integer_obj.rm_type_name == "Integer"
    assert isinstance(integer_obj.primitive, CadlIntegerConstraint)
    assert integer_obj.primitive.interval is not None
    assert integer_obj.primitive.interval.lower == 0
    assert integer_obj.primitive.interval.upper == 10


def test_parse_adl_parses_primitive_enums_intervals_and_regex() -> None:
    text = load_fixture_text("adl", "minimal_cadl_primitives.adl")

    artefact, issues = parse_adl(text, filename="cadl_primitives.adl")

    assert issues == []
    assert artefact is not None
    assert isinstance(artefact.definition, CadlObjectNode)

    name_attr = next(
        a for a in artefact.definition.attributes if a.rm_attribute_name == "name"
    )
    string_obj = name_attr.children[0]
    assert string_obj.rm_type_name == "String"
    assert isinstance(string_obj.primitive, CadlStringConstraint)
    assert string_obj.primitive.pattern == "[A-Z][a-z]+"
    assert string_obj.primitive.values is None

    code_attr = next(
        a for a in artefact.definition.attributes if a.rm_attribute_name == "code"
    )
    code_obj = code_attr.children[0]
    assert isinstance(code_obj.primitive, CadlStringConstraint)
    assert code_obj.primitive.values == ("at0001", "at0002")
    assert code_obj.primitive.pattern is None

    qty_attr = next(
        a for a in artefact.definition.attributes if a.rm_attribute_name == "qty"
    )
    qty_obj = qty_attr.children[0]
    assert isinstance(qty_obj.primitive, CadlIntegerConstraint)
    assert qty_obj.primitive.interval is not None
    assert qty_obj.primitive.interval.lower == 0
    assert qty_obj.primitive.interval.upper == 10
    assert qty_obj.primitive.values == (99,)

    ratio_attr = next(
        a for a in artefact.definition.attributes if a.rm_attribute_name == "ratio"
    )
    ratio_obj = ratio_attr.children[0]
    assert isinstance(ratio_obj.primitive, CadlRealConstraint)
    assert ratio_obj.primitive.interval is not None
    assert ratio_obj.primitive.interval.lower == 0.0
    assert ratio_obj.primitive.interval.upper == 1.0
    assert ratio_obj.primitive.values == (2.5,)


def test_parse_adl_definition_invalid_occurrences_and_cardinality_emits_adl030() -> (
    None
):
    text = load_fixture_text("adl", "invalid_cadl_occurrences_cardinality.adl")

    artefact, issues = parse_adl(text, filename="invalid_cadl.adl")

    assert artefact is not None
    assert issues

    codes = [i.code for i in issues]
    assert "ADL030" in codes
