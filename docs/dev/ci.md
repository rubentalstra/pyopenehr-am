# CI

CI should run on Python 3.14 and include:

- ruff (check + format)
- pytest
- type checking (pyright or mypy)
- parser generation drift check (run generator; fail if `git diff` non-empty)
- coverage reporting (pytest-cov)
- build sdist/wheel + `twine check` (release readiness)

## Local coverage

Install dev deps and run:

`pytest -q --cov=openehr_am --cov-report=term-missing --cov-report=xml`
