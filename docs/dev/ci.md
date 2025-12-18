# CI

CI should run on Python 3.14 and include:

- ruff (check + format)
- pytest
- type checking (pyright or mypy)
- parser generation drift check (run generator; fail if `git diff` non-empty)
- build sdist/wheel + `twine check` (release readiness)
