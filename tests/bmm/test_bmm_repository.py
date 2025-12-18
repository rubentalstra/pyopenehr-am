from pathlib import Path

from openehr_am.bmm.repository import ModelRepository
from openehr_am.validation.issue import Severity


def test_model_repository_load_from_dir_and_get_class(tmp_path: Path) -> None:
    a = tmp_path / "a.bmm"
    a.write_text(
        """
<
  model_name = <\"RM_A\">
  packages = <
    [\"rm\"] = <
      classes = <
        [\"A\"] = <
          properties = <
            [\"b\"] = < type = <\"B\"> >
          >
        >
      >
    >
  >
>
""".strip(),
        encoding="utf-8",
    )

    b = tmp_path / "b.bmm"
    b.write_text(
        """
<
  model_name = <\"RM_B\">
  packages = <
    [\"rm\"] = <
      classes = <
        [\"B\"] = <
          properties = <
            [\"value\"] = < type = <\"String\"> >
          >
        >
      >
    >
  >
>
""".strip(),
        encoding="utf-8",
    )

    repo, issues = ModelRepository.load_from_dir(tmp_path)

    assert repo.get_class("A") is not None
    assert repo.get_class("B") is not None

    # Type reference B should resolve now that both files are loaded.
    assert not any(i.code == "BMM500" for i in issues)


def test_model_repository_emits_bmm500_for_unknown_type(tmp_path: Path) -> None:
    a = tmp_path / "rm.bmm"
    a.write_text(
        """
<
  model_name = <\"RM\">
  packages = <
    [\"rm\"] = <
      classes = <
        [\"A\"] = <
          properties = <
            [\"x\"] = < type = <\"DOES_NOT_EXIST\"> >
          >
        >
      >
    >
  >
>
""".strip(),
        encoding="utf-8",
    )

    _repo, issues = ModelRepository.load_from_dir(tmp_path)

    assert any(i.code == "BMM500" and i.severity == Severity.ERROR for i in issues)
