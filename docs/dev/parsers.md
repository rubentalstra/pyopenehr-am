# Parser generation (ANTLR)

## Policy

- Generated Python parser code is **committed** under `openehr_am/_generated/`.
- Do not edit generated files by hand.
- Update grammars under `grammars/` and regenerate.

This is enforced by CI: it runs the generator and fails if `git diff` is
non-empty.

## Reality check: JVM tool vs Python runtime

- This project uses the **ANTLR Python runtime** (`antlr4-python3-runtime`) at
  _runtime_ (pure Python).
- The **ANTLR code generator** (the tool that turns `.g4` grammars into Python
  code) is a **JVM tool**. So: a JVM is only required for contributors
  regenerating parsers, not for end-users installing/using the library.

Also: the ANTLR docs stress that the **tool version and Python runtime version
must match** to avoid subtle failures.

Reference: https://github.com/antlr/antlr4/blob/master/doc/python-target.md

## Why we commit generated code

- Installing from sdist/wheel must not require the ANTLR generator.
- Contributors can regenerate when changing grammars; users should not need to.

## Workflow

1. Put grammar sources under `grammars/` (e.g. ANTLR `.g4`).
2. Run the generator:
   - `ANTLR4_JAR=/path/to/antlr-4.13.2-complete.jar python scripts/generate_parsers.py`
     (or
     `python scripts/generate_parsers.py --antlr-jar /path/to/antlr-4.13.2-complete.jar`)

- Alternatively, if you have an `antlr4` executable installed, you can use it
  without configuring a jar:
  - `python scripts/generate_parsers.py` (auto-detects `antlr4` on `PATH`)
  - or `python scripts/generate_parsers.py --antlr4 /path/to/antlr4`

3. Commit any regenerated output under `openehr_am/_generated/`.
4. Sanity check:
   - `git diff` should be clean after committing regenerated output.

## Contributor prerequisites

End-users of the library must not need the ANTLR generator. These requirements
are for contributors who change grammars.

- JVM: a working launcher on your `PATH`

Choose one of:

- ANTLR tool jar: download an `antlr-*-complete.jar` from the official ANTLR
  project and point the generator at it via `ANTLR4_JAR` or `--antlr-jar`.
- An `antlr4` executable on `PATH` (often provided by OS packages or
  `antlr4-tools`).

The repo intentionally does not vendor the ANTLR jar.

Notes:

- The generator must be deterministic (no timestamps, no machine-specific
  paths).
- The generator should be safe to run repeatedly (idempotent).

## CI enforcement

CI runs the generator and fails if `git diff` shows changes.

Locally, you can run the same check:

```bash
ANTLR4_JAR=/path/to/antlr-4.13.2-complete.jar python scripts/generate_parsers.py
git diff --exit-code
```

## Optional local pytest check

There is an optional, lightweight sanity test that checks whether committed
generated output is present for the grammars (it does not run the ANTLR
generator).

Enable it locally with:

```bash
OPENEHR_AM_CHECK_GENERATED=1 pytest -q tests/meta/test_generated_sanity.py
```
