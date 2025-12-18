def test_imports_work() -> None:
    import openehr_am
    import openehr_am.cli.app
    import openehr_am.cli.main

    assert isinstance(openehr_am.__version__, str)
