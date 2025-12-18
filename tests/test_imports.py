def test_imports_smoke() -> None:
    import openehr_am
    from openehr_am.cli.main import app

    assert openehr_am is not None
    assert app is not None
