from pathlib import Path


def repo_root(start: Path | None = None) -> Path:
    """Return the repository root by searching upward for pyproject.toml.

    This is intentionally filesystem-based (not import-based) so it keeps
    working if tests are moved into deeper subdirectories.
    """

    base = (start or Path(__file__).resolve()).resolve()
    if base.is_file():
        base = base.parent

    for candidate in (base, *base.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate

    raise RuntimeError(
        "Could not locate repo root: pyproject.toml not found when searching upward "
        f"from {base}"
    )
