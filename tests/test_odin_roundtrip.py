from openehr_am.odin.ast import (
    OdinBoolean,
    OdinInteger,
    OdinKeyedList,
    OdinKeyedListItem,
    OdinList,
    OdinNode,
    OdinNull,
    OdinObject,
    OdinObjectItem,
    OdinReal,
    OdinString,
)
from openehr_am.odin.emit import to_odin
from openehr_am.odin.parser import parse_odin


def _norm(node: OdinNode):
    match node:
        case OdinString(value=v):
            return ("s", v)
        case OdinInteger(value=v):
            return ("i", v)
        case OdinReal(value=v):
            return ("r", v)
        case OdinBoolean(value=v):
            return ("b", v)
        case OdinNull():
            return ("null",)
        case OdinList(items=items):
            return ("list", tuple(_norm(x) for x in items))
        case OdinObject(items=items):
            return ("obj", tuple((it.key, _norm(it.value)) for it in items))
        case OdinKeyedList(items=items):
            return ("klist", tuple((_norm(it.key), _norm(it.value)) for it in items))
        case _:
            raise AssertionError(f"Unexpected node type: {type(node).__name__}")


def _roundtrip(node: OdinNode) -> OdinNode:
    text = to_odin(node)
    parsed, issues = parse_odin(text)
    assert issues == []
    assert parsed is not None
    return parsed


def test_to_odin_roundtrip_primitives() -> None:
    assert _norm(_roundtrip(OdinString("hi\nthere"))) == _norm(OdinString("hi\nthere"))
    assert _norm(_roundtrip(OdinInteger(29_000_000))) == _norm(OdinInteger(29_000_000))
    assert _norm(_roundtrip(OdinReal(3.14))) == _norm(OdinReal(3.14))
    assert _norm(_roundtrip(OdinBoolean(True))) == _norm(OdinBoolean(True))
    assert _norm(_roundtrip(OdinNull())) == _norm(OdinNull())


def test_to_odin_roundtrip_list_object_and_keyed_list() -> None:
    lst = OdinList(items=(OdinInteger(1), OdinInteger(2)))
    obj = OdinObject(
        items=(
            OdinObjectItem(key="a", value=OdinInteger(1)),
            OdinObjectItem(key="b", value=lst),
        )
    )

    parsed_obj = _roundtrip(obj)
    assert _norm(parsed_obj) == _norm(obj)

    klist = OdinKeyedList(
        items=(
            OdinKeyedListItem(key=OdinString("k"), value=OdinInteger(1)),
            OdinKeyedListItem(key=OdinString("k2"), value=OdinObject(items=())),
        )
    )

    parsed_klist = _roundtrip(klist)
    assert _norm(parsed_klist) == _norm(klist)


def test_to_odin_roundtrip_nested_keyed_list_in_object() -> None:
    nested = OdinKeyedList(
        items=(OdinKeyedListItem(key=OdinString("k"), value=OdinInteger(1)),)
    )
    obj = OdinObject(items=(OdinObjectItem(key="m", value=nested),))

    parsed = _roundtrip(obj)
    assert _norm(parsed) == _norm(obj)
