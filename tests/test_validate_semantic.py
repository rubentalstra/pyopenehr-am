from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.semantic import register_semantic_check, validate_semantic


def test_validate_semantic_runs_registered_check(monkeypatch) -> None:
    # Use a fresh registry to avoid leaking global registrations across tests.
    from openehr_am.validation import semantic as semantic_module
    from openehr_am.validation.registry import ValidationRegistry

    fresh_registry = ValidationRegistry()
    monkeypatch.setattr(semantic_module, "DEFAULT_REGISTRY", fresh_registry)

    aom_obj = object()
    seen: list[object] = []

    def stub_check(ctx: ValidationContext):
        seen.append(ctx.artefact)
        return [
            Issue(
                code="AOM205",
                severity=Severity.ERROR,
                message="stub semantic failure",
                file="x",
                line=2,
                col=1,
            )
        ]

    register_semantic_check(stub_check)
    issues = validate_semantic(aom_obj)

    assert seen == [aom_obj]
    assert [i.code for i in issues] == ["AOM205"]


def test_validate_semantic_aom200_missing_terminology_codes_emitted_deterministically() -> (
    None
):
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.constraints import CAttribute, CComplexObject
    from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition

    root_span = SourceSpan(
        file="x.adl", start_line=10, start_col=1, end_line=10, end_col=10
    )
    child_span = SourceSpan(
        file="x.adl", start_line=20, start_col=1, end_line=20, end_col=10
    )
    ac_span = SourceSpan(
        file="x.adl", start_line=30, start_col=1, end_line=30, end_col=10
    )

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        span=root_span,
        attributes=(
            CAttribute(
                rm_attribute_name="data",
                children=(
                    CComplexObject(
                        rm_type_name="HISTORY",
                        node_id="at0001",
                        span=child_span,
                    ),
                    CComplexObject(
                        rm_type_name="ELEMENT",
                        node_id="ac0001",
                        span=ac_span,
                    ),
                ),
            ),
        ),
    )

    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(TermDefinition(language="en", code="at0000", text="Root"),),
    )

    aom = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.test.v1",
        concept="at0000",
        definition=definition,
        terminology=terminology,
        span=root_span,
    )

    issues = validate_semantic(aom)

    assert [i.code for i in issues] == ["AOM200", "AOM200"]
    assert [i.node_id for i in issues] == ["at0001", "ac0001"]
    assert [i.line for i in issues] == [20, 30]


def test_validate_semantic_aom200_no_missing_codes_ok() -> None:
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.constraints import CAttribute, CComplexObject
    from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition

    root_span = SourceSpan(
        file="ok.adl", start_line=10, start_col=1, end_line=10, end_col=10
    )
    child_span = SourceSpan(
        file="ok.adl", start_line=20, start_col=1, end_line=20, end_col=10
    )
    ac_span = SourceSpan(
        file="ok.adl", start_line=30, start_col=1, end_line=30, end_col=10
    )

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        span=root_span,
        attributes=(
            CAttribute(
                rm_attribute_name="data",
                children=(
                    CComplexObject(
                        rm_type_name="HISTORY",
                        node_id="at0001",
                        span=child_span,
                    ),
                    CComplexObject(
                        rm_type_name="ELEMENT",
                        node_id="ac0001",
                        span=ac_span,
                    ),
                ),
            ),
        ),
    )

    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(
            TermDefinition(language="en", code="at0000", text="Root"),
            TermDefinition(language="en", code="at0001", text="Child"),
            TermDefinition(language="en", code="ac0001", text="Constraint"),
        ),
    )

    aom = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.ok.v1",
        concept="at0000",
        definition=definition,
        terminology=terminology,
        span=root_span,
    )

    issues = validate_semantic(aom)
    assert issues == ()


def test_validate_semantic_aom210_invalid_node_id_format_emitted() -> None:
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.constraints import CAttribute, CComplexObject
    from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition

    root_span = SourceSpan(
        file="bad.adl", start_line=10, start_col=1, end_line=10, end_col=10
    )
    bad_span = SourceSpan(
        file="bad.adl", start_line=20, start_col=1, end_line=20, end_col=10
    )

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        span=root_span,
        attributes=(
            CAttribute(
                rm_attribute_name="data",
                children=(
                    CComplexObject(
                        rm_type_name="HISTORY",
                        node_id="at01",
                        span=bad_span,
                    ),
                ),
            ),
        ),
    )

    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(TermDefinition(language="en", code="at0000", text="Root"),),
    )

    aom = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.bad.v1",
        concept="at0000",
        definition=definition,
        terminology=terminology,
        span=root_span,
    )

    issues = validate_semantic(aom)
    assert [i.code for i in issues] == ["AOM210"]
    assert issues[0].node_id == "at01"
    assert issues[0].line == 20


def test_validate_semantic_aom230_specialisation_depth_mismatch_emitted() -> None:
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.constraints import CAttribute, CComplexObject
    from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition

    root_span = SourceSpan(
        file="spec.adl", start_line=10, start_col=1, end_line=10, end_col=10
    )
    child_span = SourceSpan(
        file="spec.adl", start_line=20, start_col=1, end_line=20, end_col=10
    )

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        span=root_span,
        attributes=(
            CAttribute(
                rm_attribute_name="data",
                children=(
                    CComplexObject(
                        rm_type_name="HISTORY",
                        node_id="at0001.1",
                        span=child_span,
                    ),
                ),
            ),
        ),
    )

    # Include terminology defs so AOM200 doesn't fire and we isolate AOM230.
    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(
            TermDefinition(language="en", code="at0000", text="Root"),
            TermDefinition(language="en", code="at0001.1", text="Child"),
        ),
    )

    aom = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.spec.v1",
        concept="at0000",
        definition=definition,
        terminology=terminology,
        span=root_span,
    )

    issues = validate_semantic(aom)
    assert [i.code for i in issues] == ["AOM230"]
    assert issues[0].node_id == "at0001.1"
    assert issues[0].line == 20


def test_validate_semantic_aom210_allows_specialised_node_id_pattern() -> None:
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.constraints import CAttribute, CComplexObject
    from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition

    root_span = SourceSpan(
        file="ok2.adl", start_line=10, start_col=1, end_line=10, end_col=10
    )
    child_span = SourceSpan(
        file="ok2.adl", start_line=20, start_col=1, end_line=20, end_col=10
    )

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000.1",
        span=root_span,
        attributes=(
            CAttribute(
                rm_attribute_name="data",
                children=(
                    CComplexObject(
                        rm_type_name="HISTORY",
                        node_id="at0001.1",
                        span=child_span,
                    ),
                ),
            ),
        ),
    )

    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(
            TermDefinition(language="en", code="at0000.1", text="Root"),
            TermDefinition(language="en", code="at0001.1", text="Child"),
        ),
    )

    aom = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.ok2.v1",
        concept="at0000.1",
        definition=definition,
        terminology=terminology,
        span=root_span,
    )

    issues = validate_semantic(aom)
    assert issues == ()


def test_validate_semantic_aom240_duplicate_attribute_name_emitted() -> None:
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.constraints import CAttribute, CComplexObject
    from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition

    root_span = SourceSpan(
        file="dup_attr.adl", start_line=10, start_col=1, end_line=10, end_col=10
    )
    attr1_span = SourceSpan(
        file="dup_attr.adl", start_line=20, start_col=1, end_line=20, end_col=10
    )
    attr2_span = SourceSpan(
        file="dup_attr.adl", start_line=30, start_col=1, end_line=30, end_col=10
    )

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        span=root_span,
        attributes=(
            CAttribute(
                rm_attribute_name="data",
                children=(),
                span=attr1_span,
            ),
            CAttribute(
                rm_attribute_name="data",
                children=(),
                span=attr2_span,
            ),
        ),
    )

    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(TermDefinition(language="en", code="at0000", text="Root"),),
    )

    aom = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.dup_attr.v1",
        concept="at0000",
        definition=definition,
        terminology=terminology,
        span=root_span,
    )

    issues = validate_semantic(aom)
    assert [i.code for i in issues] == ["AOM240"]
    assert issues[0].line == 30
    assert issues[0].path == "/definition/data"


def test_validate_semantic_aom240_duplicate_sibling_node_id_emitted() -> None:
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.constraints import CAttribute, CComplexObject
    from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition

    root_span = SourceSpan(
        file="dup_id.adl", start_line=10, start_col=1, end_line=10, end_col=10
    )
    first_span = SourceSpan(
        file="dup_id.adl", start_line=20, start_col=1, end_line=20, end_col=10
    )
    dup_span = SourceSpan(
        file="dup_id.adl", start_line=30, start_col=1, end_line=30, end_col=10
    )

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        span=root_span,
        attributes=(
            CAttribute(
                rm_attribute_name="items",
                children=(
                    CComplexObject(
                        rm_type_name="ELEMENT",
                        node_id="at0001",
                        span=first_span,
                    ),
                    CComplexObject(
                        rm_type_name="ELEMENT",
                        node_id="at0001",
                        span=dup_span,
                    ),
                ),
            ),
        ),
    )

    # Keep terminology in-sync so AOM200 doesn't fire.
    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(
            TermDefinition(language="en", code="at0000", text="Root"),
            TermDefinition(language="en", code="at0001", text="Child"),
        ),
    )

    aom = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.dup_id.v1",
        concept="at0000",
        definition=definition,
        terminology=terminology,
        span=root_span,
    )

    issues = validate_semantic(aom)
    assert [i.code for i in issues] == ["AOM240"]
    assert issues[0].node_id == "at0001"
    assert issues[0].line == 30
    assert issues[0].path == "/definition/items"


def test_validate_semantic_aom250_invalid_occurrences_interval_emitted() -> None:
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.constraints import CComplexObject, Interval
    from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition

    root_span = SourceSpan(
        file="inv_occ.adl", start_line=10, start_col=1, end_line=10, end_col=10
    )
    occ_span = SourceSpan(
        file="inv_occ.adl", start_line=20, start_col=1, end_line=20, end_col=10
    )

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        span=root_span,
        occurrences=Interval(lower=2, upper=1, span=occ_span),
        attributes=(),
    )

    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(TermDefinition(language="en", code="at0000", text="Root"),),
    )

    aom = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.inv_occ.v1",
        concept="at0000",
        definition=definition,
        terminology=terminology,
        span=root_span,
    )

    issues = validate_semantic(aom)
    assert [i.code for i in issues] == ["AOM250"]
    assert issues[0].line == 20
    assert issues[0].path == "/definition/occurrences"


def test_validate_semantic_aom250_invalid_primitive_interval_emitted() -> None:
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.constraints import (
        CAttribute,
        CComplexObject,
        CPrimitiveObject,
        Interval,
        PrimitiveIntegerConstraint,
    )
    from openehr_am.aom.terminology import ArchetypeTerminology, TermDefinition

    root_span = SourceSpan(
        file="inv_prim.adl", start_line=10, start_col=1, end_line=10, end_col=10
    )
    prim_span = SourceSpan(
        file="inv_prim.adl", start_line=20, start_col=1, end_line=20, end_col=10
    )
    int_span = SourceSpan(
        file="inv_prim.adl", start_line=25, start_col=1, end_line=25, end_col=10
    )

    definition = CComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        span=root_span,
        attributes=(
            CAttribute(
                rm_attribute_name="count",
                children=(
                    CPrimitiveObject(
                        rm_type_name="Integer",
                        node_id="at0001",
                        span=prim_span,
                        constraint=PrimitiveIntegerConstraint(
                            interval=Interval(lower=5, upper=4, span=int_span)
                        ),
                    ),
                ),
            ),
        ),
    )

    terminology = ArchetypeTerminology(
        original_language="en",
        term_definitions=(
            TermDefinition(language="en", code="at0000", text="Root"),
            TermDefinition(language="en", code="at0001", text="Count"),
        ),
    )

    aom = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.inv_prim.v1",
        concept="at0000",
        definition=definition,
        terminology=terminology,
        span=root_span,
    )

    issues = validate_semantic(aom)
    assert [i.code for i in issues] == ["AOM250"]
    assert issues[0].line == 25
    assert issues[0].path == "/definition/count/constraint"
