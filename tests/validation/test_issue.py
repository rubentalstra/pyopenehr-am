import json

from openehr_am.validation.issue import Issue, Severity


def test_issue_to_dict_is_json_serializable() -> None:
    issue = Issue(
        code="AOM200",
        severity=Severity.ERROR,
        message="Terminology code 'at0001' is referenced but not defined.",
        file="test.adl",
        line=12,
        col=3,
        end_line=12,
        end_col=9,
        path="/data[at0001]",
        node_id="at0001",
    )

    d = issue.to_dict()

    assert d["severity"] == "ERROR"
    assert d["code"] == "AOM200"
    assert d["file"] == "test.adl"

    # Must be JSON serializable (strict JSON logging / CLI mode).
    json.dumps(d)


def test_issue_pretty_with_location_span_and_extras() -> None:
    issue = Issue(
        code="ADL001",
        severity=Severity.ERROR,
        message="Unexpected token '}'.",
        file="broken.adl",
        line=2,
        col=10,
        end_col=11,
        path="/definition",
        node_id="at0000",
    )

    assert (
        issue.pretty()
        == "broken.adl:2:10-11: ERROR ADL001: Unexpected token '}'. (path=/definition, node_id=at0000)"
    )


def test_issue_pretty_without_location() -> None:
    issue = Issue(code="OPT700", severity=Severity.ERROR, message="Missing archetype.")
    assert issue.pretty() == "ERROR OPT700: Missing archetype."
