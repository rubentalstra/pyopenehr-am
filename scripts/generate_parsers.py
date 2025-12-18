import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate ANTLR-derived Python parser code into openehr_am/_generated/. "
            "Currently a no-op unless a grammars/ directory is present."
        ),
    )
    _ = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    grammars_dir = repo_root / "grammars"
    generated_dir = repo_root / "openehr_am" / "_generated"

    if not grammars_dir.exists():
        print(
            "scripts/generate_parsers.py: no grammars/ directory; nothing to generate"
        )
        return 0

    if not generated_dir.exists():
        raise SystemExit(
            "openehr_am/_generated/ is missing. Create it and commit generated code."
        )

    raise SystemExit(
        "Parser generation is not implemented yet. "
        "Add grammars under grammars/ and implement this script to regenerate "
        "openehr_am/_generated/ deterministically."
    )


if __name__ == "__main__":
    raise SystemExit(main())
