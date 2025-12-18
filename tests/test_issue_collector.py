import json

from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.issue_collector import IssueCollector


def test_issue_collector_extend_sorts_deterministically() -> None:
    collector = IssueCollector()

    # Intentionally out-of-order.
    collector.extend(
        [
            Issue(
                code="AOM200",
                severity=Severity.ERROR,
                message="b",
                file="b.adl",
                line=2,
                col=1,
            ),
            Issue(
                code="AOM200",
                severity=Severity.WARN,
                message="a",
                file="a.adl",
                line=3,
                col=1,
            ),
            Issue(
                code="AOM210",
                severity=Severity.ERROR,
                message="c",
                file="a.adl",
                line=1,
                col=9,
            ),
            Issue(
                code="OPT700",
                severity=Severity.ERROR,
                message="no file",
                file=None,
                line=None,
                col=None,
            ),
        ]
    )

    assert [i.file for i in collector.issues] == ["a.adl", "a.adl", "b.adl", None]
    assert [i.code for i in collector.issues] == [
        "AOM210",
        "AOM200",
        "AOM200",
        "OPT700",
    ]


def test_issue_collector_has_errors() -> None:
    collector = IssueCollector(
        [
            Issue(code="AOM270", severity=Severity.WARN, message="warn"),
        ]
    )
    assert collector.has_errors() is False

    collector.extend([Issue(code="AOM200", severity=Severity.ERROR, message="err")])
    assert collector.has_errors() is True


def test_issue_collector_to_json_is_strict_json_and_sorted() -> None:
    collector = IssueCollector(
        [
            Issue(code="AOM200", severity=Severity.ERROR, message="b", file="b.adl"),
            Issue(code="AOM200", severity=Severity.ERROR, message="a", file="a.adl"),
        ]
    )

    payload = json.loads(collector.to_json())
    assert isinstance(payload, list)
    assert [item["file"] for item in payload] == ["a.adl", "b.adl"]
    assert payload[0]["severity"] == "ERROR"
