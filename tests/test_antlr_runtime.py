from openehr_am.antlr.runtime import IssueCollectingErrorListener
from openehr_am.validation.issue import Severity
from openehr_am.validation.issue_collector import IssueCollector


def test_antlr_error_listener_converts_syntax_error_to_issue() -> None:
    collector = IssueCollector()
    listener = IssueCollectingErrorListener(collector, file="broken.adl")

    # Simulate ANTLR's callback (recognizer/offendingSymbol/e are not required
    # for us to produce a diagnostic).
    listener.syntaxError(
        recognizer=None,
        offendingSymbol=None,
        line=3,
        column=0,
        msg="Unexpected token '}'",
        e=None,
    )

    assert len(collector) == 1
    issue = collector.issues[0]

    assert issue.code == "ADL001"
    assert issue.severity == Severity.ERROR
    assert issue.file == "broken.adl"
    assert issue.line == 3
    assert issue.col == 1  # ANTLR column is 0-based
    assert issue.message == "Unexpected token '}'"
