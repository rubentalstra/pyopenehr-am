import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from openehr_am.cli.app import app


def _minimal_adl_with_missing_sections() -> str:
    # Missing language/description/terminology should deterministically emit ADL010.
    return "archetype\nopenEHR-EHR-OBSERVATION.missing_sections.v1\n"


def _adl_with_unknown_kind_but_complete_sections() -> str:
    # Unknown kind => ADL020 (WARN), but include required sections to avoid ADL010.
    return (
        "foo\n"
        "openEHR-EHR-OBSERVATION.unknown_kind.v1\n\n"
        "language\n"
        'original_language = <"en">\n'
        'language = <"en">\n\n'
        "description\n<>\n\n"
        "terminology\n<>\n\n"
        "definition\n-- TODO\n"
    )


def _template_with_slot_adl(template_id: str, *, include_pattern: str) -> str:
    # Minimal cADL subset supported by the hand-written parser.
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


def _archetype_adl(archetype_id: str) -> str:
    return (
        "archetype\n"
        f"{archetype_id}\n\n"
        "language\n"
        'original_language = <"en">\n'
        'language = <"en">\n\n'
        "description\n<>\n\n"
        "terminology\n<>\n\n"
        "definition\n-- TODO\n"
    )


@pytest.fixture()
def cli_runner() -> CliRunner:
    return CliRunner()


def test_lint_text_exit_1_and_renders_issues(
    tmp_path: Path, cli_runner: CliRunner
) -> None:
    p = tmp_path / "bad.adl"
    p.write_text(_minimal_adl_with_missing_sections(), encoding="utf-8")

    res = cli_runner.invoke(app, ["--no-color", "lint", str(p)])
    assert res.exit_code == 1
    assert "ADL010" in res.stdout


def test_lint_json_is_valid_json(tmp_path: Path, cli_runner: CliRunner) -> None:
    p = tmp_path / "bad.adl"
    p.write_text(_minimal_adl_with_missing_sections(), encoding="utf-8")

    res = cli_runner.invoke(app, ["lint", str(p), "--json"])
    assert res.exit_code == 1

    payload = json.loads(res.stdout)
    assert isinstance(payload, list)
    assert any(item["code"] == "ADL010" for item in payload)


def test_lint_strict_treats_warn_as_error(
    tmp_path: Path, cli_runner: CliRunner
) -> None:
    p = tmp_path / "warn.adl"
    p.write_text(_adl_with_unknown_kind_but_complete_sections(), encoding="utf-8")

    res = cli_runner.invoke(app, ["lint", str(p)])
    assert res.exit_code == 0

    res_strict = cli_runner.invoke(app, ["lint", str(p), "--strict", "--json"])
    assert res_strict.exit_code == 1
    payload = json.loads(res_strict.stdout)
    assert any(item["code"] == "ADL020" for item in payload)


def test_validate_semantic_ok_exit_0(tmp_path: Path, cli_runner: CliRunner) -> None:
    p = tmp_path / "ok_template.adl"
    p.write_text(
        _template_with_slot_adl(
            "openEHR-EHR-COMPOSITION.ok_template.v1",
            include_pattern='"openEHR-EHR-OBSERVATION.wanted.v1"',
        ),
        encoding="utf-8",
    )

    res = cli_runner.invoke(app, ["validate", str(p), "--json"])
    assert res.exit_code == 0
    assert json.loads(res.stdout) == []


def test_validate_with_rm_emits_bmm500(tmp_path: Path, cli_runner: CliRunner) -> None:
    tmpl = tmp_path / "template.adl"
    tmpl.write_text(
        _template_with_slot_adl(
            "openEHR-EHR-COMPOSITION.template_with_rm.v1",
            include_pattern='"openEHR-EHR-OBSERVATION.wanted.v1"',
        ),
        encoding="utf-8",
    )

    # Minimal RM repo that only defines COMPOSITION, not OBSERVATION,
    # so RM type existence check emits BMM500.
    rm_dir = tmp_path / "rm"
    rm_dir.mkdir()
    (rm_dir / "rm.bmm").write_text(
        (
            "<\n"
            '  model_name = <"RM">\n'
            "  packages = <\n"
            '    ["rm"] = <\n'
            "      classes = <\n"
            '        ["COMPOSITION"] = <\n'
            "        >\n"
            "      >\n"
            "    >\n"
            "  >\n"
            ">\n"
        ),
        encoding="utf-8",
    )

    res = cli_runner.invoke(app, ["validate", str(tmpl), "--rm", str(rm_dir), "--json"])
    assert res.exit_code == 1
    payload = json.loads(res.stdout)
    assert any(item["code"] == "BMM500" for item in payload)


def test_compile_opt_writes_json_file(tmp_path: Path, cli_runner: CliRunner) -> None:
    wanted = "openEHR-EHR-OBSERVATION.wanted.v1"
    (tmp_path / "wanted.adl").write_text(_archetype_adl(wanted), encoding="utf-8")

    template_path = tmp_path / "template.adl"
    template_path.write_text(
        _template_with_slot_adl(
            "openEHR-EHR-COMPOSITION.template_with_slot.v1",
            include_pattern=f'"{wanted}"',
        ),
        encoding="utf-8",
    )

    out = tmp_path / "out.opt.json"

    res = cli_runner.invoke(
        app,
        [
            "compile-opt",
            str(template_path),
            "--repo",
            str(tmp_path),
            "--out",
            str(out),
            "--json",
        ],
    )
    assert res.exit_code == 0
    assert json.loads(res.stdout) == []

    data = json.loads(out.read_text(encoding="utf-8"))
    assert wanted in data["component_archetype_ids"]


def test_compile_opt_invalid_repo_is_exit_2(
    tmp_path: Path, cli_runner: CliRunner
) -> None:
    template_path = tmp_path / "template.adl"
    template_path.write_text(
        _template_with_slot_adl(
            "openEHR-EHR-COMPOSITION.template_with_slot.v1",
            include_pattern='"openEHR-EHR-OBSERVATION.wanted.v1"',
        ),
        encoding="utf-8",
    )

    out = tmp_path / "out.opt.json"

    res = cli_runner.invoke(
        app,
        [
            "compile-opt",
            str(template_path),
            "--repo",
            str(tmp_path / "does_not_exist"),
            "--out",
            str(out),
            "--json",
        ],
    )

    assert res.exit_code == 2
    payload = json.loads(res.stdout)
    assert any(item["code"] == "CLI011" for item in payload)
