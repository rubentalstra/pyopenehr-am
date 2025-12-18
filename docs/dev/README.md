# Development

This project is **pure Python only** and targets **Python 3.14+ only**.

## Setup

```bash
pip install -e ".[dev]"
```

## Pre-commit (recommended)

Install the git hooks:

```bash
pre-commit install
```

Run the hooks across all files:

```bash
pre-commit run --all-files
```

By default, Ruff runs on each commit and `pytest` runs on `pre-push`.

## Tests

```bash
pytest
```
