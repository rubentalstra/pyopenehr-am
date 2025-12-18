import re
from pathlib import Path

from openehr_am.validation.issue import validate_issue_code
from tests.repo_root import repo_root

_CODE_RE = re.compile(r"\b(?:ADL|ODN|AOM|BMM|OPT|PATH|CLI)\d{3}\b")


def _repo_root() -> Path:
    return repo_root(Path(__file__).resolve())


def _iter_python_source_files(root: Path) -> list[Path]:
    src_root = root / "openehr_am"
    paths: list[Path] = []
    for p in src_root.rglob("*.py"):
        if "_generated" in p.parts:
            continue
        paths.append(p)
    return sorted(paths)


def _extract_codes(text: str) -> set[str]:
    return set(_CODE_RE.findall(text))


def test_validate_issue_code_accepts_known_prefixes_and_ranges() -> None:
    assert validate_issue_code("ADL001")
    assert validate_issue_code("ADL199")

    assert validate_issue_code("ODN100")
    assert validate_issue_code("ODN199")

    assert validate_issue_code("AOM200")
    assert validate_issue_code("AOM499")

    assert validate_issue_code("BMM500")
    assert validate_issue_code("BMM699")

    assert validate_issue_code("OPT700")
    assert validate_issue_code("OPT899")

    assert validate_issue_code("PATH900")
    assert validate_issue_code("PATH999")

    assert validate_issue_code("CLI001")
    assert validate_issue_code("CLI199")


def test_validate_issue_code_rejects_wrong_format_or_range() -> None:
    assert not validate_issue_code("")
    assert not validate_issue_code("adl001")  # must be uppercase
    assert not validate_issue_code("ADL01")  # must be ###
    assert not validate_issue_code("ADL000")  # below range
    assert not validate_issue_code("ADL200")  # above range

    assert not validate_issue_code("ODN099")
    assert not validate_issue_code("ODN200")

    assert not validate_issue_code("AOM199")
    assert not validate_issue_code("AOM500")

    assert not validate_issue_code("PATH089")
    assert not validate_issue_code("PATH1000")

    assert not validate_issue_code("CLI000")
    assert not validate_issue_code("CLI200")
    assert not validate_issue_code("CLI999")

    assert not validate_issue_code("XYZ123")  # unknown prefix


def test_issue_codes_used_in_source_are_documented() -> None:
    root = _repo_root()

    documented = _extract_codes(
        (root / "docs" / "issue-codes.md").read_text(encoding="utf-8")
    )

    used: set[str] = set()
    for path in _iter_python_source_files(root):
        used |= _extract_codes(path.read_text(encoding="utf-8"))

    # Only enforce “used ⊆ documented”. The docs can mention future codes.
    missing = sorted(used - documented)
    assert not missing, (
        "Issue codes used in source but missing from docs/issue-codes.md: "
        + ", ".join(missing)
    )
