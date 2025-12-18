from pathlib import Path


def _read_fixture(name: str) -> str:
    fixtures = Path(__file__).resolve().parents[1] / "fixtures" / "adl"
    return (fixtures / name).read_text(encoding="utf-8")


def test_archetype_repository_loads_by_id(tmp_path: Path) -> None:
    from openehr_am.aom.repository import ArchetypeRepository

    (tmp_path / "minimal.adl").write_text(
        _read_fixture("minimal_archetype.adl"), encoding="utf-8"
    )

    repo, issues = ArchetypeRepository.load_from_dir(tmp_path)
    assert issues == []

    archetype = repo.get("openEHR-EHR-OBSERVATION.test.v1")
    assert archetype is not None
    assert archetype.archetype_id == "openEHR-EHR-OBSERVATION.test.v1"
    assert repo.ids() == ("openEHR-EHR-OBSERVATION.test.v1",)


def test_archetype_repository_skips_invalid_adl_and_returns_issues(
    tmp_path: Path,
) -> None:
    from openehr_am.aom.repository import ArchetypeRepository

    (tmp_path / "bad.adl").write_text(
        _read_fixture("invalid_missing_id.adl"), encoding="utf-8"
    )

    repo, issues = ArchetypeRepository.load_from_dir(tmp_path)
    assert len(repo) == 0
    assert any(i.code == "ADL001" for i in issues)


def test_archetype_repository_duplicate_id_emits_issue_and_keeps_first(
    tmp_path: Path,
) -> None:
    from openehr_am.aom.repository import ArchetypeRepository

    # Deterministic scan order: a.adl then b.adl
    (tmp_path / "a.adl").write_text(
        _read_fixture("minimal_archetype.adl"), encoding="utf-8"
    )
    (tmp_path / "b.adl").write_text(
        _read_fixture("minimal_archetype.adl"), encoding="utf-8"
    )

    repo, issues = ArchetypeRepository.load_from_dir(tmp_path)
    assert any(i.code == "AOM242" for i in issues)

    archetype = repo.get("openEHR-EHR-OBSERVATION.test.v1")
    assert archetype is not None
    assert archetype.span is not None
    assert archetype.span.file == str(tmp_path / "a.adl")
