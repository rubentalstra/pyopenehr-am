# Quickstart

This project is a **pure-Python** openEHR AM toolkit targeting **Python 3.14+**.

- Specs baseline: https://specifications.openehr.org/
- Public API is intentionally small: parsing → validation → (optional) OPT
  compilation.

## Install (dev)

From a clone of this repository:

```bash
python3.14 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

This installs the `openehr-am` CLI (console script) and the `openehr_am` Python
package.

If you don’t want to install the console script, you can also run the CLI via:

```bash
python -m openehr_am.cli.main --help
```

## CLI: parse (lint) with `--json`

Create a tiny ADL2 archetype file:

```bash
cat > demo.archetype.adl <<'ADL'
archetype
openEHR-EHR-OBSERVATION.demo.v1

language
original_language = <"en">
language = <"en">

description
<>

terminology
<>

definition
-- TODO
ADL
```

Parse it (syntax-only) and emit Issues as strict JSON:

```bash
openehr-am lint demo.archetype.adl --json
```

- Output is a JSON array of Issue objects (no Rich markup).
- Success is typically `[]`.

Equivalent form:

```bash
openehr-am lint demo.archetype.adl --format json
```

## CLI: semantic validation (and optional RM validation)

Validate semantic constraints:

```bash
openehr-am validate demo.archetype.adl
```

Validate semantic + RM constraints using a BMM/RM repository directory:

```bash
openehr-am validate demo.archetype.adl --rm /path/to/bmm-repo
```

Emit Issues as JSON and treat warnings as errors:

```bash
openehr-am validate demo.archetype.adl --json --strict
```

## CLI: compile a template to OPT2 JSON

Create a minimal template that references an archetype via a slot include:

```bash
mkdir -p demo_repo

cat > demo_repo/wanted.adl <<'ADL'
archetype
openEHR-EHR-OBSERVATION.wanted.v1

language
original_language = <"en">
language = <"en">

description
<>

terminology
<>

definition
-- TODO
ADL

cat > demo.template.adl <<'ADL'
template
openEHR-EHR-COMPOSITION.template_with_slot.v1

language
original_language = <"en">
language = <"en">

description
<>

terminology
<>

definition
COMPOSITION matches {
  content matches {
    OBSERVATION matches {
      archetype_slot matches {
        include matches { "openEHR-EHR-OBSERVATION.wanted.v1" }
      }
    }
  }
}
ADL
```

Compile to an OPT JSON file:

```bash
openehr-am compile-opt demo.template.adl --repo demo_repo --out demo.opt.json
```

If you want Issues in JSON:

```bash
openehr-am compile-opt demo.template.adl --repo demo_repo --out demo.opt.json --json
```

## Exit codes

The CLI uses these exit codes:

- `0`: no errors
- `1`: validation errors (or warnings in `--strict` mode)
- `2`: I/O / usage errors

## Python API

The stable public API is exposed from the top-level package.

### Parse + validate syntax from a file

```python
from pathlib import Path

from openehr_am import parse_archetype, validate

archetype, parse_issues = parse_archetype(path=Path("demo.archetype.adl"))

# Parse/build issues are returned explicitly by parse_*.
assert parse_issues == []
assert archetype is not None

# You can also validate syntax directly from a path or text.
syntax_issues = validate(Path("demo.archetype.adl"), level="syntax")
assert syntax_issues == ()
```

### Validate semantic + RM (BMM-backed)

```python
from openehr_am import load_bmm_repo, parse_archetype, validate

archetype, issues = parse_archetype(path="demo.archetype.adl")
if archetype is None:
    # issues contains structured diagnostics (code, severity, best-effort location)
    raise SystemExit(1)

rm_repo, rm_issues = load_bmm_repo("/path/to/bmm-repo")
if rm_repo is None:
    raise SystemExit(1)

# Run semantic + RM rules.
all_issues = validate(archetype, level="all", rm=rm_repo)
```

### Compile OPT and validate OPT integrity

```python
from pathlib import Path

from openehr_am import compile_opt, parse_template, validate

template, parse_issues = parse_template(path=Path("demo.template.adl"))
assert template is not None
assert parse_issues == []

opt, compile_issues = compile_opt(template, archetype_dir=Path("demo_repo"), rm=None)
assert opt is not None
assert compile_issues == []

# OPT-level consistency checks.
opt_issues = validate(opt, level="opt")
assert opt_issues == ()
```
