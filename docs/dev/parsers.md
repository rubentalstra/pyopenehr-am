# Parser generation (ANTLR)

## Policy

- Generated Python parser code is **committed** under `openehr_am/_generated/`.
- Do not edit generated files by hand.
- Update grammars under `grammars/` and regenerate.

## Why we commit generated code

- Installing from sdist/wheel must not require Java/ANTLR.
- Contributors can regenerate when changing grammars; users should not need to.

## Workflow

1. Install Java + download ANTLR tool (document exact version in this file).
2. Run:
   - `python scripts/generate_parsers.py`
3. Ensure `git diff` is clean after committing regenerated output.

## CI enforcement

CI runs the generator and fails if `git diff` shows changes.
