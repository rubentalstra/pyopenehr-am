from pathlib import Path


def _archetype_adl(archetype_id: str, *, parent_archetype_id: str | None = None) -> str:
    specialise = f"\nspecialise\n{parent_archetype_id}\n" if parent_archetype_id else ""
    return (
        "archetype\n"
        f"{archetype_id}\n"
        f"{specialise}\n"
        "language\n"
        'original_language = <"en">\n'
        'language = <"en">\n\n'
        "description\n<>\n\n"
        "terminology\n<>\n\n"
        "definition\n-- TODO\n"
    )


def _archetype_adl_with_definition(
    archetype_id: str,
    *,
    definition_cadl: str,
    parent_archetype_id: str | None = None,
) -> str:
    specialise = f"\nspecialise\n{parent_archetype_id}\n" if parent_archetype_id else ""
    cadl = definition_cadl.strip("\n") + "\n"
    return (
        "archetype\n"
        f"{archetype_id}\n"
        f"{specialise}\n"
        "language\n"
        'original_language = <"en">\n'
        'language = <"en">\n\n'
        "description\n<>\n\n"
        "terminology\n<>\n\n"
        "definition\n"
        f"{cadl}"
    )


def _template_with_slot_adl(template_id: str, *, include_pattern: str) -> str:
    # Minimal cADL subset supported by the hand-written parser.
    # Slot subset: archetype_slot matches { include matches { <pattern> } }
    return (
        "template\n"
        f"{template_id}\n\n"
        "language\n"
        'original_language = <"en">\n'
        'language = <"en">\n\n'
        "description\n<>\n\n"
        "terminology\n<>\n\n"
        "definition\n"
        "COMPOSITION matches {\n"
        "  content matches {\n"
        "    OBSERVATION matches {\n"
        "      archetype_slot matches {\n"
        f"        include matches {{ {include_pattern} }}\n"
        "      }\n"
        "    }\n"
        "  }\n"
        "}\n"
    )


def _parse_template_from_adl(text: str, *, filename: str):
    from openehr_am.adl import parse_adl
    from openehr_am.aom.archetype import Template as AomTemplate
    from openehr_am.aom.builder import build_aom_from_adl
    from openehr_am.validation.issue import Severity

    artefact, parse_issues = parse_adl(text, filename=filename)
    assert artefact is not None
    assert not any(i.severity is Severity.ERROR for i in parse_issues)

    aom, build_issues = build_aom_from_adl(artefact)
    assert isinstance(aom, AomTemplate)
    assert not any(i.severity is Severity.ERROR for i in build_issues)
    return aom


def test_compile_opt_orders_included_archetypes(tmp_path: Path) -> None:
    from openehr_am.aom.archetype import Template
    from openehr_am.opt.compiler import compile_opt

    parent_id = "openEHR-EHR-OBSERVATION.parent.v1"
    child_id = "openEHR-EHR-OBSERVATION.child.v1"

    (tmp_path / "parent.adl").write_text(_archetype_adl(parent_id), encoding="utf-8")
    (tmp_path / "child.adl").write_text(
        _archetype_adl(child_id, parent_archetype_id=parent_id), encoding="utf-8"
    )

    template = Template(template_id="openEHR-EHR-COMPOSITION.example_template.v1")
    opt, issues = compile_opt(template, archetype_dir=tmp_path)

    assert issues == []
    assert opt is not None
    assert opt.component_archetype_ids == (parent_id, child_id)
    assert opt.root_archetype_id == child_id


def test_compile_opt_missing_dependency_emits_opt700(tmp_path: Path) -> None:
    from openehr_am.aom.archetype import Template
    from openehr_am.opt.compiler import compile_opt

    missing_parent_id = "openEHR-EHR-OBSERVATION.missing_parent.v1"
    child_id = "openEHR-EHR-OBSERVATION.child.v1"

    (tmp_path / "child.adl").write_text(
        _archetype_adl(child_id, parent_archetype_id=missing_parent_id),
        encoding="utf-8",
    )

    template = Template(template_id="openEHR-EHR-COMPOSITION.example_template.v1")
    opt, issues = compile_opt(template, archetype_dir=tmp_path)

    assert opt is None
    assert any(i.code == "OPT700" for i in issues)


def test_compile_opt_slot_filling_no_match_emits_opt720(tmp_path: Path) -> None:
    from openehr_am.opt.compiler import compile_opt

    # Repo has an archetype, but it doesn't match the slot's include.
    (tmp_path / "one.adl").write_text(
        _archetype_adl("openEHR-EHR-OBSERVATION.unrelated.v1"), encoding="utf-8"
    )

    template = _parse_template_from_adl(
        _template_with_slot_adl(
            "openEHR-EHR-COMPOSITION.template_with_slot.v1",
            include_pattern='"openEHR-EHR-OBSERVATION.missing.v1"',
        ),
        filename=str(tmp_path / "template.adl"),
    )

    opt, issues = compile_opt(template, archetype_dir=tmp_path)

    assert opt is None
    assert any(i.code == "OPT720" for i in issues)


def test_compile_opt_slot_filling_match_succeeds(tmp_path: Path) -> None:
    from openehr_am.opt.compiler import compile_opt

    wanted = "openEHR-EHR-OBSERVATION.wanted.v1"
    (tmp_path / "wanted.adl").write_text(_archetype_adl(wanted), encoding="utf-8")

    template = _parse_template_from_adl(
        _template_with_slot_adl(
            "openEHR-EHR-COMPOSITION.template_with_slot.v1",
            include_pattern=f'"{wanted}"',
        ),
        filename=str(tmp_path / "template.adl"),
    )

    opt, issues = compile_opt(template, archetype_dir=tmp_path)

    assert not any(i.code == "OPT720" for i in issues)
    assert opt is not None
    assert wanted in opt.component_archetype_ids


def test_compile_opt_specialisation_flattening_merges_child_over_parent(
    tmp_path: Path,
) -> None:
    from openehr_am.aom.archetype import Template
    from openehr_am.opt.compiler import compile_opt
    from openehr_am.opt.model import OptCComplexObject

    parent_id = "openEHR-EHR-COMPOSITION.parent.v1"
    child_id = "openEHR-EHR-COMPOSITION.child.v1"

    parent_def = (
        "COMPOSITION matches {\n"
        "  content matches {\n"
        "    OBSERVATION[at0001] matches { }\n"
        "  }\n"
        "}\n"
    )
    child_def = (
        "COMPOSITION matches {\n"
        "  content matches {\n"
        "    OBSERVATION[at0001] matches {\n"
        "      data matches { ITEM_TREE matches { } }\n"
        "    }\n"
        "  }\n"
        "}\n"
    )

    (tmp_path / "parent.adl").write_text(
        _archetype_adl_with_definition(parent_id, definition_cadl=parent_def),
        encoding="utf-8",
    )
    (tmp_path / "child.adl").write_text(
        _archetype_adl_with_definition(
            child_id,
            definition_cadl=child_def,
            parent_archetype_id=parent_id,
        ),
        encoding="utf-8",
    )

    template = Template(template_id="openEHR-EHR-COMPOSITION.example_template.v1")
    opt, issues = compile_opt(template, archetype_dir=tmp_path)

    assert opt is not None
    assert issues == []
    assert opt.definition is not None

    root = opt.definition
    content = next(a for a in root.attributes if a.rm_attribute_name == "content")
    obs = next(c for c in content.children if c.node_id == "at0001")
    assert isinstance(obs, OptCComplexObject)
    data = next(a for a in obs.attributes if a.rm_attribute_name == "data")
    assert data.children


def test_compile_opt_specialisation_flattening_conflict_emits_opt730(
    tmp_path: Path,
) -> None:
    from openehr_am.aom.archetype import Template
    from openehr_am.opt.compiler import compile_opt

    parent_id = "openEHR-EHR-COMPOSITION.parent.v1"
    child_id = "openEHR-EHR-COMPOSITION.child.v1"

    parent_def = (
        "COMPOSITION matches {\n"
        "  content matches {\n"
        "    OBSERVATION[at0001] matches { }\n"
        "  }\n"
        "}\n"
    )
    child_def = (
        "COMPOSITION matches {\n"
        "  content matches {\n"
        "    EVALUATION[at0001] matches { }\n"
        "  }\n"
        "}\n"
    )

    (tmp_path / "parent.adl").write_text(
        _archetype_adl_with_definition(parent_id, definition_cadl=parent_def),
        encoding="utf-8",
    )
    (tmp_path / "child.adl").write_text(
        _archetype_adl_with_definition(
            child_id,
            definition_cadl=child_def,
            parent_archetype_id=parent_id,
        ),
        encoding="utf-8",
    )

    template = Template(template_id="openEHR-EHR-COMPOSITION.example_template.v1")
    opt, issues = compile_opt(template, archetype_dir=tmp_path)

    assert opt is None
    assert any(i.code == "OPT730" for i in issues)
