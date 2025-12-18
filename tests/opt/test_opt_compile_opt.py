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
