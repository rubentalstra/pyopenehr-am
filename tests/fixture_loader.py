from pathlib import Path

_FIXTURES_DIR = Path(__file__).parent / "fixtures"


def fixture_path(*parts: str) -> Path:
    return _FIXTURES_DIR.joinpath(*parts)


def load_fixture_text(*parts: str) -> str:
    return fixture_path(*parts).read_text(encoding="utf-8")
