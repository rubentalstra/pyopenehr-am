# Validation Rule Template

Use this template when adding new validation rules under
`openehr_am/validation/`.

## 1) Rule metadata

- **Rule name:** (e.g., `terminology_references_defined`)
- **Layer:** syntax / semantic / rm / opt
- **Issue code(s):** (e.g., `AOM200`)
- **Default severity:** WARN / ERROR
- **Spec provenance:** paste the spec URL(s) that justify the rule
- **What it checks:** 1–2 sentences
- **False positives risk:** low / medium / high
- **Autofix possible:** yes / no (if yes, describe a safe fix)

## 2) Implementation checklist

- [ ] Add Issue code(s) to `docs/issue-codes.md` if not already present
- [ ] Implement the check as a small function returning `list[Issue]`
- [ ] Register the check in the validation registry for the correct layer
- [ ] Add tests:
  - [ ] happy path (no issues)
  - [ ] failing path asserting the Issue code(s)
  - [ ] location/path assertion if available (line/col, node id, path)

## 3) Code skeleton

```python
from dataclasses import dataclass
from openehr_am.validation.issue import Issue, Severity

def check_example(ctx) -> list[Issue]:
    issues: list[Issue] = []

    # Spec: https://specifications.openehr.org/...
    # Rationale: short explanation

    if ctx.something_is_wrong():
        issues.append(Issue(
            code="AOM200",
            severity=Severity.ERROR,
            message="Explain what is wrong.",
            file=ctx.file,
            line=ctx.line,
            col=ctx.col,
            path=ctx.path,
            node_id=ctx.node_id,
        ))

    return issues
```

## 4) Test skeleton

```python
def test_example_emits_AOM200():
    issues = validate_archetype_text(BROKEN_TEXT, level="semantic")
    assert any(i.code == "AOM200" for i in issues)
```
