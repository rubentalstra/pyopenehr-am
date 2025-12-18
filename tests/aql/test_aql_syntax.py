import pytest

from openehr_am.aql import check_aql_syntax


@pytest.mark.parametrize(
    "query",
    [
        "SELECT e/ehr_id/value FROM EHR e",
        "SELECT DISTINCT e/ehr_id/value FROM EHR e WHERE EXISTS e/ehr_id/value",
        "SELECT e/ehr_id/value FROM EHR e LIMIT 10 OFFSET 5",
    ],
)
def test_check_aql_syntax_accepts_valid_queries(query: str) -> None:
    issues = check_aql_syntax(query)
    assert issues == []


@pytest.mark.parametrize(
    "query",
    [
        "",
        "SELECT FROM",
        "SELECT e/ehr_id/value EHR e",  # missing FROM
        "SELECT e/ehr_id/value FROM",  # incomplete
    ],
)
def test_check_aql_syntax_reports_aql100(query: str) -> None:
    issues = check_aql_syntax(query)
    assert issues
    assert issues[0].code == "AQL100"
    assert issues[0].severity.value == "ERROR"
