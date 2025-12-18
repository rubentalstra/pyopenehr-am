from openehr_am.adl import ArtefactKind, parse_adl
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
