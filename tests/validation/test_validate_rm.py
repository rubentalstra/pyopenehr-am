from pathlib import Path

from openehr_am.aom.archetype import Archetype
from openehr_am.aom.constraints import Cardinality, CAttribute, CComplexObject, Interval
from openehr_am.bmm.repository import ModelRepository
from openehr_am.validation.issue import Severity
from openehr_am.validation.rm import validate_rm


def test_validate_rm_emits_bmm500_for_unknown_type(tmp_path: Path) -> None:
    # Minimal RM with only COMPOSITION.
    rm_dir = tmp_path / "rm"
    rm_dir.mkdir()

    (rm_dir / "rm.bmm").write_text(
        """
<
    model_name = <\"RM\">
    packages = <
        [\"rm\"] = <
            classes = <
                [\"COMPOSITION\"] = < properties = < > >
            >
        >
    >
>
""".strip(),
        encoding="utf-8",
    )

    repo, _issues = ModelRepository.load_from_dir(rm_dir)

    # Archetype references COMPOSITION (ok) and DOES_NOT_EXIST (bad).
    aom = Archetype(
        archetype_id="openEHR-EHR-COMPOSITION.test.v1",
        definition=CComplexObject(
            rm_type_name="COMPOSITION",
            attributes=(
                CAttribute(
                    rm_attribute_name="content",
                    children=(
                        CComplexObject(rm_type_name="DOES_NOT_EXIST", node_id="at0001"),
                    ),
                ),
            ),
        ),
    )

    issues = validate_rm(aom, rm_repo=repo)

    assert any(i.code == "BMM500" and i.severity == Severity.ERROR for i in issues)
    assert any(i.node_id == "at0001" for i in issues if i.code == "BMM500")


def test_validate_rm_no_repo_no_issues() -> None:
    aom = Archetype(
        archetype_id="openEHR-EHR-COMPOSITION.test.v1",
        definition=CComplexObject(rm_type_name="COMPOSITION"),
    )

    issues = validate_rm(aom, rm_repo=None)
    assert issues == ()


def test_validate_rm_emits_bmm510_for_unknown_attribute(tmp_path: Path) -> None:
    rm_dir = tmp_path / "rm"
    rm_dir.mkdir()

    (rm_dir / "rm.bmm").write_text(
        """
<
    model_name = <\"RM\">
    packages = <
        [\"rm\"] = <
            classes = <
                [\"COMPOSITION\"] = <
                    properties = <
                        [\"content\"] = < type = <\"String\"> >
                    >
                >
            >
        >
    >
>
""".strip(),
        encoding="utf-8",
    )

    repo, _issues = ModelRepository.load_from_dir(rm_dir)

    aom = Archetype(
        archetype_id="openEHR-EHR-COMPOSITION.test.v1",
        definition=CComplexObject(
            rm_type_name="COMPOSITION",
            node_id="at0000",
            attributes=(CAttribute(rm_attribute_name="does_not_exist"),),
        ),
    )

    issues = validate_rm(aom, rm_repo=repo)
    assert any(i.code == "BMM510" and i.severity == Severity.ERROR for i in issues)
    assert any(i.node_id == "at0000" for i in issues if i.code == "BMM510")


def test_validate_rm_does_not_emit_bmm510_for_inherited_attribute(
    tmp_path: Path,
) -> None:
    rm_dir = tmp_path / "rm"
    rm_dir.mkdir()

    (rm_dir / "rm.bmm").write_text(
        """
<
    model_name = <\"RM\">
    packages = <
        [\"rm\"] = <
            classes = <
                [\"LOCATABLE\"] = <
                    properties = <
                        [\"uid\"] = < type = <\"String\"> >
                    >
                >

                [\"COMPOSITION\"] = <
                    parent = <\"LOCATABLE\">
                    properties = < >
                >
            >
        >
    >
>
""".strip(),
        encoding="utf-8",
    )

    repo, _issues = ModelRepository.load_from_dir(rm_dir)

    aom = Archetype(
        archetype_id="openEHR-EHR-COMPOSITION.test.v1",
        definition=CComplexObject(
            rm_type_name="COMPOSITION",
            attributes=(CAttribute(rm_attribute_name="uid"),),
        ),
    )

    issues = validate_rm(aom, rm_repo=repo)
    assert not any(i.code == "BMM510" for i in issues)


def test_validate_rm_emits_bmm520_for_multiplicity_exceeding_rm(tmp_path: Path) -> None:
    rm_dir = tmp_path / "rm"
    rm_dir.mkdir()

    (rm_dir / "rm.bmm").write_text(
        """
<
    model_name = <\"RM\">
    packages = <
        [\"rm\"] = <
            classes = <
                [\"COMPOSITION\"] = <
                    properties = <
                        [\"content\"] = <
                            type = <\"String\">
                            multiplicity = < lower = <0> upper = <1> >
                        >
                    >
                >
            >
        >
    >
>
""".strip(),
        encoding="utf-8",
    )

    repo, _issues = ModelRepository.load_from_dir(rm_dir)

    aom = Archetype(
        archetype_id="openEHR-EHR-COMPOSITION.test.v1",
        definition=CComplexObject(
            rm_type_name="COMPOSITION",
            node_id="at0000",
            attributes=(
                CAttribute(
                    rm_attribute_name="content",
                    cardinality=Cardinality(occurrences=Interval(lower=0, upper=2)),
                ),
            ),
        ),
    )

    issues = validate_rm(aom, rm_repo=repo)
    assert any(i.code == "BMM520" and i.severity == Severity.ERROR for i in issues)
    assert any(i.node_id == "at0000" for i in issues if i.code == "BMM520")


def test_validate_rm_does_not_emit_bmm520_when_within_rm(tmp_path: Path) -> None:
    rm_dir = tmp_path / "rm"
    rm_dir.mkdir()

    (rm_dir / "rm.bmm").write_text(
        """
<
    model_name = <\"RM\">
    packages = <
        [\"rm\"] = <
            classes = <
                [\"COMPOSITION\"] = <
                    properties = <
                        [\"content\"] = <
                            type = <\"String\">
                            multiplicity = < lower = <0> upper = <*> >
                        >
                    >
                >
            >
        >
    >
>
""".strip(),
        encoding="utf-8",
    )

    repo, _issues = ModelRepository.load_from_dir(rm_dir)

    aom = Archetype(
        archetype_id="openEHR-EHR-COMPOSITION.test.v1",
        definition=CComplexObject(
            rm_type_name="COMPOSITION",
            attributes=(
                CAttribute(
                    rm_attribute_name="content",
                    cardinality=Cardinality(occurrences=Interval(lower=0, upper=2)),
                ),
            ),
        ),
    )

    issues = validate_rm(aom, rm_repo=repo)
    assert not any(i.code == "BMM520" for i in issues)
