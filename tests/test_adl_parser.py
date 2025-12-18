from openehr_am.adl import ArtefactKind, parse_adl


def test_parse_adl_minimal_archetype_extracts_sections_and_spans() -> None:
    text = (
        "archetype\n"
        "openEHR-EHR-OBSERVATION.test.v1\n"
        "\n"
        "language\n"
        'original_language = <"en">\n'
        'language = <"en">\n'
        "\n"
        "description\n"
        "<>\n"
        "\n"
        "terminology\n"
        "<>\n"
        "\n"
        "definition\n"
        "-- TODO\n"
    )

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
    text = (
        "template\n"
        "openEHR-EHR-COMPOSITION.test_template.v1\n"
        "\n"
        "language\n"
        'original_language = <"en">\n'
        "\n"
        "description\n"
        "<>\n"
        "\n"
        "terminology\n"
        "<>\n"
    )

    artefact, issues = parse_adl(text, filename="template.adl")

    assert issues == []
    assert artefact is not None
    assert artefact.kind is ArtefactKind.TEMPLATE
    assert artefact.artefact_id == "openEHR-EHR-COMPOSITION.test_template.v1"
