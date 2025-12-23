from openehr_am.odin.ast import OdinInteger, OdinObject
from openehr_am.odin.parser import parse_odin
from openehr_am.validation.issue import Severity


def test_parse_odin_returns_issue_on_garbage_input() -> None:
    node, issues = parse_odin("@")

    assert node is None
    assert len(issues) == 1
    assert issues[0].code == "ODN100"
    assert issues[0].severity == Severity.ERROR
    assert issues[0].line == 1
    assert issues[0].col == 1


def test_parse_odin_returns_issue_on_unterminated_string() -> None:
    node, issues = parse_odin('a = <"unterminated>')

    assert node is None
    assert issues
    assert issues[0].code == "ODN100"


def test_parse_odin_returns_issue_on_missing_block_end() -> None:
    node, issues = parse_odin("a = <1")

    assert node is None
    assert issues
    assert issues[0].code == "ODN100"


def test_parse_odin_never_raises_on_various_malformed_inputs() -> None:
    samples = [
        "<",
        ">",
        "a = <>",
        "a = <,>",
        "a = <[1] =>",
        "a = <[1] = <1>",
        "a = <True False>",
        "a = <1,>",
        'a = <"x" "y">',
        'a = <["k"] = <1> ["k"] = <2>>',  # duplicate key is not checked yet
    ]

    for text in samples:
        node, issues = parse_odin(text)
        assert not (node is None and issues == [])


def test_parse_odin_parses_implicit_object_document() -> None:
    node, issues = parse_odin("a = <1>")

    assert issues == []
    assert isinstance(node, OdinObject)
    assert node.items[0].key == "a"
    assert isinstance(node.items[0].value, OdinInteger)
    assert node.items[0].value.value == 1


def test_parse_odin_sets_issue_filename() -> None:
    node, issues = parse_odin("@", filename="broken.odin")

    assert node is None
    assert issues
    assert issues[0].file == "broken.odin"


def test_parse_odin_empty_document_returns_empty_object() -> None:
    node, issues = parse_odin("")

    assert issues == []
    assert node is not None
    assert isinstance(node, OdinObject)
    assert node.items == ()
