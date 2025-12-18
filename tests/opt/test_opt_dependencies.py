from pathlib import Path


def test_dependency_order_for_archetypes_is_deterministic() -> None:
    from openehr_am.aom.archetype import Archetype
    from openehr_am.opt.dependencies import dependency_order_for_archetypes

    a = Archetype(archetype_id="openEHR-EHR-OBSERVATION.a.v1")
    b = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.b.v1",
        parent_archetype_id="openEHR-EHR-OBSERVATION.a.v1",
    )

    order, issues = dependency_order_for_archetypes([b, a])
    assert issues == []
    assert order == (
        "openEHR-EHR-OBSERVATION.a.v1",
        "openEHR-EHR-OBSERVATION.b.v1",
    )


def test_dependency_cycle_emits_opt705(tmp_path: Path) -> None:
    from openehr_am.antlr.span import SourceSpan
    from openehr_am.aom.archetype import Archetype
    from openehr_am.opt.dependencies import dependency_order_for_archetypes

    a = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.a.v1",
        parent_archetype_id="openEHR-EHR-OBSERVATION.b.v1",
        span=SourceSpan(
            file=str(tmp_path / "a.adl"),
            start_line=1,
            start_col=1,
            end_line=1,
            end_col=2,
        ),
    )
    b = Archetype(
        archetype_id="openEHR-EHR-OBSERVATION.b.v1",
        parent_archetype_id="openEHR-EHR-OBSERVATION.a.v1",
        span=SourceSpan(
            file=str(tmp_path / "b.adl"),
            start_line=1,
            start_col=1,
            end_line=1,
            end_col=2,
        ),
    )

    order, issues = dependency_order_for_archetypes([a, b])
    assert order == ()
    assert any(i.code == "OPT705" for i in issues)
    assert any("openEHR-EHR-OBSERVATION.a.v1" in i.message for i in issues)
    assert any("openEHR-EHR-OBSERVATION.b.v1" in i.message for i in issues)


def test_parse_specialise_sets_parent_archetype_id() -> None:
    from openehr_am.adl.parser import parse_adl
    from openehr_am.aom.archetype import Archetype
    from openehr_am.aom.builder import build_aom_from_adl

    text = """archetype
openEHR-EHR-OBSERVATION.child.v1

specialise
openEHR-EHR-OBSERVATION.parent.v1

language
original_language = <\"en\">
language = <\"en\">

description
<>

terminology
<>

definition
-- TODO
"""

    artefact, issues = parse_adl(text, filename="child.adl")
    assert artefact is not None
    assert issues == []

    aom_obj, build_issues = build_aom_from_adl(artefact)
    assert build_issues == []
    assert isinstance(aom_obj, Archetype)
    assert aom_obj.parent_archetype_id == "openEHR-EHR-OBSERVATION.parent.v1"
