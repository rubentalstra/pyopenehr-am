# Validation Rule Template

Use this template when adding new validation rules under
`openehr_am/validation/`.

## 1) Rule metadata

- **Rule name:** (e.g., `terminology_references_defined`)
- **Layer:** syntax / semantic / rm / opt
- **Issue code(s):** (e.g., `AOM200`)
- **Default severity:** WARN / ERROR
- **Spec provenance:** paste the spec URL(s) that justify the rule
  - Example:
    `https://specifications.openehr.org/releases/AM/Release-2.1.0/AOM2.html`
- **What it checks:** 1–2 sentences
- **False positives risk:** low / medium / high
- **Autofix possible:** yes / no (if yes, describe a safe fix)

## 2) Implementation checklist

- [ ] Add Issue code(s) to `docs/issue-codes.md` if not already present
- [ ] Implement the check as a small function returning `list[Issue]`
- [ ] Register the check in the validation registry for the correct layer
- [ ] Add at least:
  - [ ] a happy-path test (no issues)
  - [ ] a failing test asserting the Issue code(s)
  - [ ] a location/path assertion if available (line/col or node id)

## 3) Code skeleton (example)

```python
# openehr_am/validation/aom/terminology.py

from __future__ import annotations

from openehr_am.validation.issue import Issue, Severity

def check_terminology_references_defined(ctx) -> list[Issue]:
    issues: list[Issue] = []

    # Spec: https://specifications.openehr.org/releases/AM/Release-2.1.0/AOM2.html
    # Rationale: referenced at-codes must exist in terminology definitions.

    for ref in ctx.iter_referenced_term_codes():
        if not ctx.terminology.has_code(ref.code):
            issues.append(Issue(
                code="AOM200",
                severity=Severity.ERROR,
                message=f"Terminology code '{ref.code}' is referenced but not defined.",
                file=ref.file,
                line=ref.line,
                col=ref.col,
                path=ref.path,
                node_id=ref.node_id,
            ))

    return issues
```

## 4) Test skeleton (example)

```python
# tests/test_aom_terminology_references.py

def test_missing_terminology_code_emits_AOM200():
    issues = validate_archetype_text(BROKEN_ARCHETYPE_TEXT, level="semantic")
    assert any(i.code == "AOM200" for i in issues)
```
