---
name: Python typing and annotations (3.14+)
description: How to use typing, annotations, and introspection correctly on Python 3.14+
applyTo: "openehr_am/**/*.py"
---
# Typing & annotations (Python 3.14+)

## Annotations semantics
- Python 3.14 uses deferred evaluation of annotations by default.
- Do not add `from __future__ import annotations` (it changes semantics and is unnecessary for 3.14+).

## Runtime introspection
- If you need evaluated annotations at runtime, use:
  - `annotationlib.get_annotations(obj, ...)`
- Avoid reading `__annotations__` directly for anything important.

## Style
- Prefer `X | None` over `Optional[X]`.
- Prefer built-in generics (`list[str]`) over `typing.List[str]`.
- Keep public function signatures typed and stable.

## Performance
- Use `slots=True` dataclasses to reduce memory for large trees/models.
