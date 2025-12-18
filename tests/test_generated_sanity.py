import os
import re
from pathlib import Path

import pytest

_GRAMMAR_NAME_RE = re.compile(
    r"^\s*(?:lexer\s+|parser\s+)?grammar\s+([A-Za-z_]\w*)\s*;\s*$"
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _grammar_names(grammars: list[Path]) -> list[str]:
    names: list[str] = []
    for grammar in grammars:
        text = grammar.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            m = _GRAMMAR_NAME_RE.match(line)
            if m:
                names.append(m.group(1))
                break
    return sorted(set(names))


@pytest.mark.skipif(
    os.environ.get("OPENEHR_AM_CHECK_GENERATED") not in {"1", "true", "TRUE"},
    reason="Set OPENEHR_AM_CHECK_GENERATED=1 to enable generated-code sanity checks.",
)
def test_generated_outputs_present_for_grammars() -> None:
    """Optional local sanity check for committed generated output.

    This is intentionally lightweight and does not run Java/ANTLR.

    - Skips if there are no grammar sources under grammars/.
    - Fails if openehr_am/_generated/ is missing expected files for those grammars.

    CI remains the primary enforcement (it runs the generator and checks git diff).
    """

    root = _repo_root()
    grammars_dir = root / "grammars"
    generated_dir = root / "openehr_am" / "_generated"

    grammars = sorted(grammars_dir.rglob("*.g4")) if grammars_dir.exists() else []
    if not grammars:
        pytest.skip("No grammars found under grammars/*.g4")

    assert generated_dir.exists(), "Missing openehr_am/_generated/"
    assert (generated_dir / "README.md").exists(), (
        "Missing openehr_am/_generated/README.md"
    )

    # When generation has run at least once, we expect a package marker.
    # (The generator writes one deterministically.)
    assert (generated_dir / "__init__.py").exists(), (
        "Missing openehr_am/_generated/__init__.py"
    )

    missing: list[str] = []

    for name in _grammar_names(grammars):
        lexer = generated_dir / f"{name}Lexer.py"
        parser = generated_dir / f"{name}Parser.py"

        if not lexer.exists() and not parser.exists():
            missing.append(f"{name}Lexer.py / {name}Parser.py")

    assert not missing, (
        "Generated output appears missing or out of date. "
        "Run scripts/generate_parsers.py and commit changes. Missing: "
        + ", ".join(missing)
    )
