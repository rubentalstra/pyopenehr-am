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
2. Run the generator (choose one):

   Option A: use an ANTLR tool jar (recommended for deterministic tool pinning)

   - `ANTLR4_JAR=/path/to/antlr-4.13.2-complete.jar python scripts/generate_parsers.py`
     (or
     `python scripts/generate_parsers.py --antlr-jar /path/to/antlr-4.13.2-complete.jar`)

   Option B: use an `antlr4` executable (often provided by `antlr4-tools`)

   - `python scripts/generate_parsers.py` (auto-detects `antlr4` on `PATH`)
   - or `python scripts/generate_parsers.py --antlr4 /path/to/antlr4`

3. Review the changes under `openehr_am/_generated/`.
4. Commit regenerated output.

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

## Regeneration steps (copy/paste)

From the repo root:

```bash
python -m pip install -e '.[dev]'

# If you use a jar:
ANTLR4_JAR=/path/to/antlr-4.13.2-complete.jar python scripts/generate_parsers.py

# If you use an antlr4 executable:
python scripts/generate_parsers.py

git status
git diff
```

Important details:

- The generator normalizes machine-specific headers in generated Python files
  (ANTLR includes absolute paths by default), so output diffs should be stable
  across machines.
- `openehr_am/_generated/README.md` is preserved; everything else in
  `openehr_am/_generated/` is replaced on regeneration.

## Version matching (tool vs runtime)

Per ANTLR’s Python target documentation, the **ANTLR tool version** used to
generate code should match the installed **antlr4-python3-runtime** version. The
generator enforces this when it can detect both versions.

If you see an error like:

```text
ANTLR tool/runtime version mismatch
```

use a jar / `antlr4` that matches the runtime pinned in this repository.

## CI enforcement

CI runs the generator and fails if committed generated code drifts.

Policy:

- `openehr_am/_generated/` is committed.
- CI re-runs `python scripts/generate_parsers.py`.
- CI fails the job if `git diff` is non-empty afterwards.

Locally, you can run the same check:

```bash
ANTLR4_JAR=/path/to/antlr-4.13.2-complete.jar python scripts/generate_parsers.py
git diff --exit-code
```

If you use an `antlr4` executable instead of a jar:

```bash
python scripts/generate_parsers.py
git diff --exit-code
```

## Troubleshooting

- `No ANTLR tool configured`: provide `ANTLR4_JAR` / `--antlr-jar`, or ensure an
  `antlr4` executable is on `PATH`.
- `JVM launcher not found on PATH`: a JVM is required when generating via
  `java -jar ...`.
- `ANTLR generation failed`: check that your grammar changes compile; run the
  generator again to see the error output from the ANTLR tool.

## Optional local pytest check

There is an optional, lightweight sanity test that checks whether committed
generated output is present for the grammars (it does not run the ANTLR
generator).

Enable it locally with:

```bash
OPENEHR_AM_CHECK_GENERATED=1 pytest -q tests/meta/test_generated_sanity.py
```
