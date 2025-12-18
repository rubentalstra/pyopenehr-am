from pathlib import Path

from tests.repo_root import repo_root


def test_no_future_annotations_import_in_openehr_am() -> None:
    package_root = repo_root(Path(__file__).resolve()) / "openehr_am"

    offenders: list[Path] = []
    needle = "from __future__ import annotations"

    for path in package_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if needle in text:
            offenders.append(path.relative_to(package_root.parent))

    assert offenders == [], (
        "Python 3.14+ baseline: do not use 'from __future__ import annotations' in openehr_am/. "
        f"Found in: {', '.join(str(p) for p in offenders)}"
    )
