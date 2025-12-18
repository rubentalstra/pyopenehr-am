import dataclasses

import pytest

from openehr_am.antlr.span import SourceSpan
from openehr_am.odin.ast import (
    OdinBoolean,
    OdinInteger,
    OdinKeyedList,
    OdinKeyedListItem,
    OdinList,
    OdinNull,
    OdinObject,
    OdinObjectItem,
    OdinReal,
    OdinString,
)


def test_source_span_is_frozen_slots_dataclass() -> None:
    assert dataclasses.is_dataclass(SourceSpan)
    span = SourceSpan(file="x.odin", start_line=1, start_col=1, end_line=1, end_col=3)

    assert not hasattr(span, "__dict__")
    with pytest.raises(dataclasses.FrozenInstanceError):
        span.start_line = 2  # type: ignore[misc]


def test_primitives_are_immutable_and_can_carry_spans() -> None:
    span = SourceSpan(file=None, start_line=1, start_col=1, end_line=1, end_col=1)

    s = OdinString("hi", span=span)
    i = OdinInteger(12)
    r = OdinReal(1.25)
    b = OdinBoolean(True)
    n = OdinNull(span=span)

    assert s.value == "hi"
    assert s.span is span
    assert i.span is None
    assert n.span is span
    assert r.value == 1.25
    assert b.value is True

    with pytest.raises(dataclasses.FrozenInstanceError):
        s.value = "bye"  # type: ignore[misc]


def test_containers_preserve_order_and_nesting() -> None:
    obj = OdinObject(
        items=(
            OdinObjectItem(key="a", value=OdinInteger(1)),
            OdinObjectItem(key="b", value=OdinString("x")),
        )
    )

    lst = OdinList(items=(OdinNull(), obj))

    keyed = OdinKeyedList(
        items=(
            OdinKeyedListItem(key=OdinString("k"), value=lst),
            OdinKeyedListItem(key=OdinInteger(2), value=OdinBoolean(False)),
        )
    )

    assert [it.key for it in obj.items] == ["a", "b"]
    assert isinstance(lst.items[1], OdinObject)
    assert isinstance(keyed.items[0].key, OdinString)
    assert keyed.items[0].key.value == "k"
    assert isinstance(keyed.items[0].value, OdinList)
