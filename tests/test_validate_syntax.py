from pathlib import Path

from openehr_am.validation.issue import Severity
from openehr_am.validation.syntax import validate_syntax
from tests.fixture_loader import load_fixture_text


def test_validate_syntax_text_ok() -> None:
    text = load_fixture_text("adl", "minimal_archetype.adl")
    issues = validate_syntax(text=text, filename="minimal_archetype.adl")
    assert issues == ()


def test_validate_syntax_text_missing_id_emits_adl001() -> None:
    text = load_fixture_text("adl", "invalid_missing_id.adl")
    issues = validate_syntax(text=text, filename="invalid_missing_id.adl")
    assert [i.code for i in issues] == ["ADL001"]
    assert issues[0].severity == Severity.ERROR


def test_validate_syntax_path_missing_file_emits_adl005(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.adl"
    issues = validate_syntax(path=missing)
    assert [i.code for i in issues] == ["ADL005"]
    assert issues[0].severity == Severity.ERROR
    assert issues[0].file == str(missing)
