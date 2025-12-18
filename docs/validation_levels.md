# Validation levels

Validation can be run in pipeline layers. You choose a layer via
`validate(obj, level=...)` (Python API) or the CLI commands.

- Pipeline overview: [architecture.md](architecture.md)
- openEHR specifications: https://specifications.openehr.org/

## Levels

- `syntax` — parsing/grammar-level issues (ADL2 / ODIN)
- `semantic` — semantic AOM validity rules (AOM2-ish)
- `rm` — reference model (RM) conformance using BMM schemas
- `opt` — OPT integrity checks
- `all` — run everything applicable for the input object

## What each level checks

- `syntax`
  - Purpose: parse-only checks (lexing/parsing; structural validity of the
    text).
  - Input: ADL2 text (`str`) or an ADL2 file path (`str`/`Path`).
  - Output: `Issue` objects with best-effort file/line/column spans.

- `semantic`
  - Purpose: semantic checks on the AOM object model.
  - Input: an AOM `Archetype` or `Template` (typically returned by
    `parse_archetype` / `parse_template`).

- `rm`
  - Purpose: RM conformance checks (type/property conformance) using a loaded
    BMM repository.
  - Input: an AOM `Archetype` or `Template`, plus `rm=ModelRepository`.
  - Notes: use `load_bmm_repo(dir)` to load a BMM/RM repository.

- `opt`
  - Purpose: integrity checks on an `OperationalTemplate`.
  - Input: an `OperationalTemplate` produced by `compile_opt`.

- `all`
  - Purpose: “run what makes sense for this object type”.
  - Behavior depends on the input:
    - ADL2 text/path: runs `syntax`.
    - AOM `Archetype`/`Template`: runs `semantic`, then `rm` (if `rm` is
      provided).
    - `OperationalTemplate`: runs `opt`.

## Input compatibility

The validator is strict about which levels apply to which input types:

- ADL2 text/path input: only `syntax` or `all`.
- AOM `Archetype`/`Template`: `semantic`, `rm`, or `all`.
- `OperationalTemplate`: `opt` or `all`.

If you choose an incompatible combination, `validate(...)` raises `TypeError`.

## CLI mapping

The CLI is a thin wrapper around the same pipeline:

- `openehr-am lint <file>`
  - Equivalent to `validate(<file>, level="syntax")`.

- `openehr-am validate <file> [--rm <dir>]`
  - Parses into AOM, then runs:
    - semantic validation
    - RM validation if `--rm` is provided

- `openehr-am compile-opt <template> --repo <dir> --out <file>`
  - Compiles a template + archetype repository to OPT JSON.

All CLI commands support `--json` / `--format json` to emit Issues as strict
JSON.

## Python API examples

### Syntax validation

```python
from pathlib import Path

from openehr_am import validate

issues = validate(Path("some.archetype.adl"), level="syntax")
for issue in issues:
		print(issue)
```

### Semantic + RM validation

```python
from openehr_am import load_bmm_repo, parse_archetype, validate

archetype, parse_issues = parse_archetype(path="some.archetype.adl")
if archetype is None:
		raise SystemExit(1)

rm_repo, rm_issues = load_bmm_repo("/path/to/bmm-repo")
if rm_repo is None:
		raise SystemExit(1)

issues = validate(archetype, level="all", rm=rm_repo)
```

### OPT validation

```python
from openehr_am import compile_opt, parse_template, validate

template, parse_issues = parse_template(path="some.template.adl")
if template is None:
		raise SystemExit(1)

opt, compile_issues = compile_opt(template, archetype_dir="/path/to/archetypes")
if opt is None:
		raise SystemExit(1)

issues = validate(opt, level="opt")
```

## Output: Issues

All validation results are returned as structured `Issue` objects.

- Issue codes are documented in [issue-codes.md](issue-codes.md).
- The CLI can render Issues as Rich tables (human) or strict JSON (`--json`).
