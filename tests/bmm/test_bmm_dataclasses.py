import pytest

from openehr_am.bmm import Class, Model, Multiplicity, Package, Property, TypeRef


def test_multiplicity_validation() -> None:
    assert Multiplicity(lower=0, upper=None).allows(0)
    assert Multiplicity(lower=0, upper=None).allows(999)

    with pytest.raises(ValueError):
        Multiplicity(lower=-1, upper=1)

    with pytest.raises(ValueError):
        Multiplicity(lower=1, upper=0)


def test_multiplicity_helpers() -> None:
    assert Multiplicity.one() == Multiplicity(lower=1, upper=1)
    assert Multiplicity.optional() == Multiplicity(lower=0, upper=1)
    assert Multiplicity.many().is_unbounded
    assert Multiplicity.exactly(2).allows(2)
    assert not Multiplicity.exactly(2).allows(1)


def test_typeref_rendering() -> None:
    assert TypeRef("DV_TEXT").render() == "DV_TEXT"
    assert TypeRef("DV_TEXT", nullable=True).render() == "DV_TEXT?"

    t = TypeRef("LIST", parameters=(TypeRef("DV_TEXT"),))
    assert t.render() == "LIST[DV_TEXT]"


def test_property_is_multiple() -> None:
    p1 = Property("items", TypeRef("DV_TEXT"), Multiplicity.many())
    assert p1.is_multiple

    p2 = Property("value", TypeRef("DV_TEXT"), Multiplicity.one())
    assert not p2.is_multiple


def test_model_class_lookup_is_deterministic_and_detects_ambiguity() -> None:
    pkg_a = Package("a")
    pkg_b = Package("b")

    pkg_a.add_class(Class("FOO"))
    pkg_b.add_class(Class("BAR"))

    m = Model("rm")
    m.add_package(pkg_b)
    m.add_package(pkg_a)

    assert [c.name for c in m.iter_classes()] == ["FOO", "BAR"]
    assert m.find_class("FOO") is pkg_a.classes["FOO"]
    assert m.find_class("MISSING") is None

    pkg_b.add_class(Class("FOO"))
    with pytest.raises(ValueError):
        m.find_class("FOO")
