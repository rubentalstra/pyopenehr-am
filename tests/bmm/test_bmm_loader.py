from pathlib import Path

from openehr_am.bmm.loader import load_bmm
from openehr_am.validation.issue import Severity
from tests.fixture_loader import fixture_path


def test_load_bmm_tiny_fixture_builds_model() -> None:
    p = fixture_path("odin", "bmm_tiny.odin")
    model, _issues = load_bmm(p)

    assert model is not None
    assert model.name == "TINY_RM"

    dv_text = model.find_class("DV_TEXT")
    assert dv_text is not None

    value = dv_text.get_property("value")
    assert value is not None
    assert value.type_ref.render() == "String"
    assert value.multiplicity.lower == 1
    assert value.multiplicity.upper == 1

    mappings = dv_text.get_property("mappings")
    assert mappings is not None
    assert mappings.type_ref.render() == "LIST[String]"
    assert mappings.multiplicity.lower == 0
    assert mappings.multiplicity.upper is None


def test_load_bmm_emits_issue_for_unknown_fields() -> None:
    p = fixture_path("odin", "bmm_tiny.odin")
    _model, issues = load_bmm(p)

    assert any(i.code == "BMM530" and i.severity == Severity.WARN for i in issues)


def test_load_bmm_missing_model_name_is_error(tmp_path: Path) -> None:
    bad = tmp_path / "bad_bmm.odin"
    bad.write_text("< packages = < > >", encoding="utf-8")

    model, issues = load_bmm(bad)
    assert model is None
    assert any(i.code == "BMM540" and i.severity == Severity.ERROR for i in issues)
