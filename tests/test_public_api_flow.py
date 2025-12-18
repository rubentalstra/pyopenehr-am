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


def test_public_api_compile_opt_flow_and_validate_opt(tmp_path: Path) -> None:
    from openehr_am import compile_opt, parse_template, validate

    wanted = "openEHR-EHR-OBSERVATION.wanted.v1"
    (tmp_path / "wanted.adl").write_text(_archetype_adl(wanted), encoding="utf-8")

    template, parse_issues = parse_template(
        text=_template_with_slot_adl(
            "openEHR-EHR-COMPOSITION.template_with_slot.v1",
            include_pattern=f'"{wanted}"',
        ),
        filename=str(tmp_path / "template.adl"),
    )

    assert template is not None
    assert parse_issues == []

    opt, compile_issues = compile_opt(template, archetype_dir=tmp_path, rm=None)

    assert opt is not None
    assert compile_issues == []
    assert wanted in opt.component_archetype_ids

    opt_issues = validate(opt, level="opt")
    assert opt_issues == ()
