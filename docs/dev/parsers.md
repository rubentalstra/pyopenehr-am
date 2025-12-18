# Parser generation (ANTLR)

## Policy

- Generated Python parser code is **committed** under `openehr_am/_generated/`.
- Do not edit generated files by hand.
- Update grammars under `grammars/` and regenerate.

This is enforced by CI: it runs the generator and fails if `git diff` is
non-empty.

## Why we commit generated code

- Installing from sdist/wheel must not require Java/ANTLR.
- Contributors can regenerate when changing grammars; users should not need to.

## Workflow

1. Put grammar sources under `grammars/` (e.g. ANTLR `.g4`).
2. Run the generator:
   - `ANTLR4_JAR=/path/to/antlr-4.13.2-complete.jar python scripts/generate_parsers.py`
     (or
     `python scripts/generate_parsers.py --antlr-jar /path/to/antlr-4.13.2-complete.jar`)
3. Commit any regenerated output under `openehr_am/_generated/`.
4. Sanity check:
   - `git diff` should be clean after committing regenerated output.

## Contributor prerequisites

End-users of the library must not need Java/ANTLR. These requirements are for
contributors who change grammars.

- Java: a working `java` on your `PATH`
- ANTLR tool jar: download an `antlr-*-complete.jar` from the official ANTLR
  project and point the generator at it via `ANTLR4_JAR` or `--antlr-jar`.

The repo intentionally does not vendor the ANTLR jar.

Notes:

- The generator must be deterministic (no timestamps, no machine-specific
  paths).
- The generator should be safe to run repeatedly (idempotent).

## CI enforcement

CI runs the generator and fails if `git diff` shows changes.

Locally, you can run the same check:

```bash
python scripts/generate_parsers.py
git diff --exit-code
```
