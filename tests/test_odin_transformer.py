from dataclasses import dataclass

from openehr_am.odin.ast import (
    OdinBoolean,
    OdinInteger,
    OdinKeyedList,
    OdinList,
    OdinObject,
    OdinReal,
    OdinString,
)
from openehr_am.odin.transformer import transform_odin_parse_tree


@dataclass(slots=True, frozen=True)
class Tok:
    text: str
    line: int = 1
    column: int = 0  # ANTLR-style (0-based)


class Ctx:
    def __init__(self, text: str, *, start: Tok | None = None, stop: Tok | None = None):
        self._text = text
        self.start = start
        self.stop = stop

    def getText(self) -> str:  # noqa: N802 (ANTLR API)
        return self._text


class StringValueCtx(Ctx):
    pass


class IntegerValueCtx(Ctx):
    pass


class RealValueCtx(Ctx):
    pass


class BooleanValueCtx(Ctx):
    pass


class PrimitiveValueCtx(Ctx):
    def __init__(self, child: Ctx):
        super().__init__(child.getText(), start=child.start, stop=child.stop)
        self._child = child

    def string_value(self) -> Ctx | None:
        return self._child if isinstance(self._child, StringValueCtx) else None

    def integer_value(self) -> Ctx | None:
        return self._child if isinstance(self._child, IntegerValueCtx) else None

    def real_value(self) -> Ctx | None:
        return self._child if isinstance(self._child, RealValueCtx) else None

    def boolean_value(self) -> Ctx | None:
        return self._child if isinstance(self._child, BooleanValueCtx) else None


class PrimitiveObjectCtx(Ctx):
    def __init__(self, primitive: Ctx):
        super().__init__(
            primitive.getText(), start=primitive.start, stop=primitive.stop
        )
        self._primitive = primitive

    def primitive_value(self) -> Ctx | None:
        return (
            self._primitive if isinstance(self._primitive, PrimitiveValueCtx) else None
        )

    def primitive_list_value(self) -> Ctx | None:
        return (
            self._primitive
            if isinstance(self._primitive, PrimitiveListValueCtx)
            else None
        )


class PrimitiveListValueCtx(Ctx):
    def __init__(
        self, values: list[PrimitiveValueCtx], text: str, start: Tok, stop: Tok
    ):
        super().__init__(text, start=start, stop=stop)
        self._values = values

    def primitive_value(self) -> list[PrimitiveValueCtx]:
        return self._values


class AttributeIdCtx(Ctx):
    pass


class AttrValCtx(Ctx):
    def __init__(self, attr_id: AttributeIdCtx, obj_block: Ctx, start: Tok, stop: Tok):
        super().__init__(
            f"{attr_id.getText()}={obj_block.getText()}", start=start, stop=stop
        )
        self._attr_id = attr_id
        self._obj_block = obj_block

    def attribute_id(self) -> AttributeIdCtx:
        return self._attr_id

    def object_block(self) -> Ctx:
        return self._obj_block


class AttrValsCtx(Ctx):
    def __init__(self, attr_vals: list[AttrValCtx], start: Tok, stop: Tok):
        super().__init__("", start=start, stop=stop)
        self._attr_vals = attr_vals

    def attr_val(self) -> list[AttrValCtx]:
        return self._attr_vals


class ObjectBlockCtx(Ctx):
    def __init__(self, ovb: Ctx):
        super().__init__(ovb.getText(), start=ovb.start, stop=ovb.stop)
        self._ovb = ovb

    def object_value_block(self) -> Ctx:
        return self._ovb


class ObjectValueBlockCtx(Ctx):
    def __init__(
        self,
        *,
        primitive_object: PrimitiveObjectCtx | None = None,
        attr_vals: AttrValsCtx | None = None,
        keyed_objects: list[Ctx] | None = None,
        start: Tok,
        stop: Tok,
        text: str,
    ):
        super().__init__(text, start=start, stop=stop)
        self._primitive_object = primitive_object
        self._attr_vals = attr_vals
        self._keyed_objects = keyed_objects or []

    def primitive_object(self) -> Ctx | None:
        return self._primitive_object

    def attr_vals(self) -> Ctx | None:
        return self._attr_vals

    def keyed_object(self) -> list[Ctx]:
        return self._keyed_objects


class KeyedObjectCtx(Ctx):
    def __init__(
        self, key: PrimitiveValueCtx, obj_block: ObjectBlockCtx, start: Tok, stop: Tok
    ):
        super().__init__("", start=start, stop=stop)
        self._key = key
        self._obj_block = obj_block

    def primitive_value(self) -> PrimitiveValueCtx:
        return self._key

    def object_block(self) -> ObjectBlockCtx:
        return self._obj_block


class OdinTextCtx(Ctx):
    def __init__(self, child: Ctx):
        super().__init__(child.getText(), start=child.start, stop=child.stop)
        self._child = child

    def attr_vals(self) -> Ctx | None:
        return self._child if isinstance(self._child, AttrValsCtx) else None

    def object_value_block(self) -> Ctx | None:
        return self._child if isinstance(self._child, ObjectValueBlockCtx) else None

    def keyed_object(self) -> list[Ctx]:
        return self._child if isinstance(self._child, list) else []


def test_transform_string() -> None:
    t = Tok('"hi\\nthere"', line=1, column=0)
    sv = StringValueCtx(t.text, start=t, stop=t)
    pv = PrimitiveValueCtx(sv)
    po = PrimitiveObjectCtx(pv)

    ovb = ObjectValueBlockCtx(
        primitive_object=po,
        start=Tok("<", 1, 0),
        stop=Tok(">", 1, 12),
        text=f"<{t.text}>",
    )

    node, issues = transform_odin_parse_tree(OdinTextCtx(ovb), filename="x.odin")
    assert issues == []
    assert isinstance(node, OdinString)
    assert node.value == "hi\nthere"
    assert node.span is not None
    assert node.span.file == "x.odin"


def test_transform_number_integer_and_real() -> None:
    it = Tok("29e6", 1, 0)
    iv = IntegerValueCtx(it.text, start=it, stop=it)
    node, issues = transform_odin_parse_tree(PrimitiveValueCtx(iv))
    assert issues == []
    assert isinstance(node, OdinInteger)
    assert node.value == 29_000_000

    rt = Tok("3.14", 1, 0)
    rv = RealValueCtx(rt.text, start=rt, stop=rt)
    node2, issues2 = transform_odin_parse_tree(PrimitiveValueCtx(rv))
    assert issues2 == []
    assert isinstance(node2, OdinReal)
    assert node2.value == 3.14


def test_transform_boolean() -> None:
    bt = Tok("True", 1, 0)
    bv = BooleanValueCtx(bt.text, start=bt, stop=bt)
    node, issues = transform_odin_parse_tree(PrimitiveValueCtx(bv))
    assert issues == []
    assert isinstance(node, OdinBoolean)
    assert node.value is True


def test_transform_primitive_list_to_odin_list() -> None:
    v1 = PrimitiveValueCtx(
        IntegerValueCtx("1", start=Tok("1", 1, 1), stop=Tok("1", 1, 1))
    )
    v2 = PrimitiveValueCtx(
        IntegerValueCtx("2", start=Tok("2", 1, 4), stop=Tok("2", 1, 4))
    )
    pl = PrimitiveListValueCtx(
        values=[v1, v2], text="1,2", start=Tok("1", 1, 1), stop=Tok("2", 1, 4)
    )
    po = PrimitiveObjectCtx(pl)
    ovb = ObjectValueBlockCtx(
        primitive_object=po,
        start=Tok("<", 1, 0),
        stop=Tok(">", 1, 5),
        text="<1,2>",
    )

    node, issues = transform_odin_parse_tree(OdinTextCtx(ovb))
    assert issues == []
    assert isinstance(node, OdinList)
    assert [x.value for x in node.items if isinstance(x, OdinInteger)] == [1, 2]


def test_transform_object_attr_vals() -> None:
    a_id = AttributeIdCtx("a", start=Tok("a", 1, 1), stop=Tok("a", 1, 1))
    prim = PrimitiveObjectCtx(
        PrimitiveValueCtx(
            IntegerValueCtx("1", start=Tok("1", 1, 6), stop=Tok("1", 1, 6))
        )
    )
    ovb_inner = ObjectValueBlockCtx(
        primitive_object=prim,
        start=Tok("<", 1, 5),
        stop=Tok(">", 1, 7),
        text="<1>",
    )
    av = AttrValCtx(
        a_id, ObjectBlockCtx(ovb_inner), start=Tok("a", 1, 1), stop=Tok(">", 1, 7)
    )
    avs = AttrValsCtx([av], start=Tok("a", 1, 1), stop=Tok(">", 1, 7))

    root = OdinTextCtx(avs)
    node, issues = transform_odin_parse_tree(root)

    assert issues == []
    assert isinstance(node, OdinObject)
    assert node.items[0].key == "a"
    assert isinstance(node.items[0].value, OdinInteger)
    assert node.items[0].value.value == 1


def test_transform_keyed_list() -> None:
    key = PrimitiveValueCtx(
        StringValueCtx('"k"', start=Tok('"k"', 1, 3), stop=Tok('"k"', 1, 5))
    )
    val_prim = PrimitiveObjectCtx(
        PrimitiveValueCtx(
            IntegerValueCtx("1", start=Tok("1", 1, 12), stop=Tok("1", 1, 12))
        )
    )
    val_ovb = ObjectValueBlockCtx(
        primitive_object=val_prim,
        start=Tok("<", 1, 11),
        stop=Tok(">", 1, 13),
        text="<1>",
    )
    ko = KeyedObjectCtx(
        key, ObjectBlockCtx(val_ovb), start=Tok("[", 1, 1), stop=Tok(">", 1, 13)
    )

    container = ObjectValueBlockCtx(
        keyed_objects=[ko],
        start=Tok("<", 1, 0),
        stop=Tok(">", 1, 14),
        text='<["k"]=<1>>',
    )

    node, issues = transform_odin_parse_tree(OdinTextCtx(container))
    assert issues == []
    assert isinstance(node, OdinKeyedList)
    assert isinstance(node.items[0].key, OdinString)
    assert node.items[0].key.value == "k"
    assert isinstance(node.items[0].value, OdinInteger)
    assert node.items[0].value.value == 1
