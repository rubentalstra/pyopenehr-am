def test_imports_work() -> None:
    import openehr_am
    import openehr_am.cli.app
    import openehr_am.cli.main

    assert hasattr(openehr_am, "__version__")
    assert isinstance(openehr_am.__version__, str)
