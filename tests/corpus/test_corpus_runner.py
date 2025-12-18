from dataclasses import dataclass
from pathlib import Path

import pytest

from tests.repo_root import repo_root
from tests.support.issue_snapshot import format_issues

from openehr_am import parse_archetype, parse_template, validate
from openehr_am.odin.parser import parse_odin
from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.issue_collector import IssueCollector


@dataclass(slots=True, frozen=True)
class CorpusResult:
    path: Path
    artefact_kind: str
    parsed_ok: bool
    issues: tuple[Issue, ...]


def _detect_adl_kind(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        head = stripped.casefold()
        if head == "archetype":
            return "archetype"
        if head == "template":
            return "template"
        return "unknown"
    return "unknown"


def _run_adl(path: Path) -> CorpusResult:
    text = path.read_text(encoding="utf-8")
    kind = _detect_adl_kind(text)

    if kind == "template":
        obj, parse_issues = parse_template(path=path)
    elif kind == "archetype":
        obj, parse_issues = parse_archetype(path=path)
    else:
        # Fallback: validate syntax only.
        obj = None
        parse_issues = list(validate(path, level="syntax"))

    collector = IssueCollector(parse_issues)
    if obj is not None:
        collector.extend(validate(obj, level="all"))

    return CorpusResult(
        path=path,
        artefact_kind=f"adl:{kind}",
        parsed_ok=obj is not None,
        issues=collector.issues,
    )


def _run_odin(path: Path) -> CorpusResult:
    text = path.read_text(encoding="utf-8")
    node, issues = parse_odin(text, filename=str(path))
    collector = IssueCollector(issues)
    return CorpusResult(
        path=path,
        artefact_kind="odin",
        parsed_ok=node is not None,
        issues=collector.issues,
    )


def _run_corpus_file(path: Path) -> CorpusResult:
    match path.suffix:
        case ".adl":
            return _run_adl(path)
        case ".odin":
            return _run_odin(path)
        case _:
            raise ValueError(f"Unsupported corpus file type: {path}")


def _corpus_files() -> list[Path]:
    root = repo_root()
    corpus_dir = root / "tests" / "corpus"
    return sorted(
        [
            p
            for p in corpus_dir.iterdir()
            if p.is_file() and p.suffix in {".adl", ".odin"}
        ],
        key=lambda p: p.name,
    )


@pytest.mark.parametrize("path", _corpus_files(), ids=lambda p: p.name)
def test_corpus_files_parse_and_validate(path: Path) -> None:
    root = repo_root()
    res = _run_corpus_file(path)

    has_error = any(i.severity is Severity.ERROR for i in res.issues)

    if path.name.startswith("ok_"):
        assert res.parsed_ok, (
            f"Expected parse OK for {path.name}\n" + format_issues(list(res.issues), root=root)
        )
        assert not has_error, (
            f"Expected no ERROR issues for {path.name}\n"
            + format_issues(list(res.issues), root=root)
        )
    elif path.name.startswith("bad_"):
        assert has_error, (
            f"Expected at least one ERROR issue for {path.name}\n"
            + format_issues(list(res.issues), root=root)
        )
    else:
        raise AssertionError(
            f"Corpus file name must start with ok_ or bad_: {path.name}"
        )


def test_corpus_snapshot_for_missing_id() -> None:
    root = repo_root()
    path = root / "tests" / "corpus" / "bad_missing_id.adl"

    res = _run_corpus_file(path)
    assert format_issues(list(res.issues), root=root) == (
        "tests/corpus/bad_missing_id.adl:1:1: ERROR ADL001: Missing artefact id\n"
    )
