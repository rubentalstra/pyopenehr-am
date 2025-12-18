from openehr_am.adl.ast import (
    AdlArtefact,
    AdlRulesSection,
    AdlSectionPlaceholder,
    ArtefactKind,
)
from openehr_am.antlr.span import SourceSpan
from openehr_am.odin.ast import OdinObject


def test_adl_artefact_captures_required_fields_and_spans() -> None:
    root_span = SourceSpan(
        file="test.adl",
        start_line=1,
        start_col=1,
        end_line=20,
        end_col=1,
    )

    desc_span = SourceSpan(
        file="test.adl",
        start_line=5,
        start_col=1,
        end_line=10,
        end_col=1,
    )
    term_span = SourceSpan(
        file="test.adl",
        start_line=11,
        start_col=1,
        end_line=15,
        end_col=1,
    )

    description = OdinObject(items=(), span=desc_span)
    terminology = OdinObject(items=(), span=term_span)

    artefact = AdlArtefact(
        kind=ArtefactKind.ARCHETYPE,
        artefact_id="openEHR-EHR-OBSERVATION.test.v1",
        original_language="en",
        language="en",
        description=description,
        terminology=terminology,
        definition=AdlSectionPlaceholder(name="definition", span=None),
        rules=AdlRulesSection(raw_text="", statements=(), header_span=None, span=None),
        span=root_span,
        artefact_id_span=SourceSpan("test.adl", 1, 1, 1, 40),
        original_language_span=SourceSpan("test.adl", 3, 1, 3, 20),
        language_span=SourceSpan("test.adl", 3, 21, 3, 40),
        description_span=desc_span,
        terminology_span=term_span,
    )

    assert artefact.kind is ArtefactKind.ARCHETYPE
    assert artefact.artefact_id == "openEHR-EHR-OBSERVATION.test.v1"
    assert artefact.original_language == "en"
    assert artefact.language == "en"

    assert artefact.description is description
    assert artefact.terminology is terminology

    assert artefact.span == root_span
    assert artefact.description_span == desc_span
    assert artefact.terminology_span == term_span


def test_artefact_kind_is_string_enum() -> None:
    assert str(ArtefactKind.TEMPLATE) == "template"
