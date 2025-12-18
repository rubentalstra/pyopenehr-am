# Releasing

This project targets Python 3.14+ and publishes source + wheel distributions.

## Checklist

1. Ensure your working tree is clean.
2. Run local checks:
   - `ruff format --check .`
   - `ruff check .`
   - `pyright`
   - `pytest`
3. Update the version in:
   - `pyproject.toml` (`[project].version`)
   - `openehr_am/__about__.py` (`__version__`)
4. Build and verify artifacts:
   - `python -m build`
   - `python -m twine check --strict dist/*`
5. Tag the release (e.g. `vX.Y.Z`) and push the tag.
6. Publish to PyPI using your preferred toolchain.

CI enforces:

- ruff (format + lint)
- pyright
- pytest
- `python -m build` + `twine check --strict` (on GitHub Release publish)
