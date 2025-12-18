import pytest

from openehr_am.path.parser import parse_path


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("/definition", []),
        ("/definition/data", [("data", None)]),
        (
            "/definition/data[at0001]/events[at0002]/data",
            [("data", "at0001"), ("events", "at0002"), ("data", None)],
        ),
        ("/data[at0001]", [("data", "at0001")]),
        ("'/definition/items[at0001.1]'", [("items", "at0001.1")]),
    ],
)
def test_parse_path_success(text: str, expected: list[tuple[str, str | None]]):
    node, issues = parse_path(text)
    assert issues == []
    assert node is not None

    got: list[tuple[str, str | None]] = []
    for seg in node.segments:
        got.append((seg.name, None if seg.predicate is None else seg.predicate.text))

    assert got == expected


@pytest.mark.parametrize(
    "text",
    [
        "",
        "data",
        "/",
        "/definition/",
        "/definition//data",
        "/definition/data[",
        "/definition/data]",
        "/definition/[at0001]",
        "/definition/data[]",
        "/definition/data[/]",
    ],
)
def test_parse_path_failure_emits_path900(text: str):
    node, issues = parse_path(text)
    assert node is None
    assert len(issues) == 1
    assert issues[0].code == "PATH900"
    assert issues[0].severity.value == "ERROR"
