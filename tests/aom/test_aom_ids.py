import pytest

from openehr_am.aom.ids import (
    format_node_id,
    is_ac_code,
    is_archetype_id,
    is_at_code,
    is_node_id,
    try_parse_archetype_id,
    try_parse_node_id,
)


def test_is_node_id_accepts_at_and_ac() -> None:
    assert is_node_id("at0000")
    assert is_node_id("ac1234")


def test_is_node_id_rejects_wrong_length_or_prefix() -> None:
    assert not is_node_id("at000")
    assert not is_node_id("at00000")
    assert not is_node_id("ax0000")


def test_is_node_id_rejects_non_digits() -> None:
    assert not is_node_id("at00a0")


def test_is_at_code_and_is_ac_code() -> None:
    assert is_at_code("at0001")
    assert not is_at_code("ac0001")

    assert is_ac_code("ac0001")
    assert not is_ac_code("at0001")


def test_try_parse_node_id_returns_parts() -> None:
    parsed = try_parse_node_id("at0042")
    assert parsed is not None
    assert parsed.prefix == "at"
    assert parsed.number == 42
    assert str(parsed) == "at0042"


def test_format_node_id_pads_with_zeros() -> None:
    assert format_node_id("at", 7) == "at0007"


def test_format_node_id_rejects_out_of_range() -> None:
    with pytest.raises(ValueError):
        format_node_id("ac", -1)

    with pytest.raises(ValueError):
        format_node_id("ac", 10000)


def test_try_parse_archetype_id_accepts_typical_openEHR_id() -> None:
    aid = try_parse_archetype_id("openEHR-EHR-OBSERVATION.example.v1")
    assert aid is not None

    assert aid.originator == "openEHR"
    assert aid.rm_name == "EHR"
    assert aid.rm_entity == "OBSERVATION"
    assert aid.concept == "example"
    assert aid.version == "v1"


def test_is_archetype_id_rejects_bad_shapes() -> None:
    assert not is_archetype_id("openEHR-EHR-OBSERVATION")
    assert not is_archetype_id("openEHR-EHR-OBSERVATION.example")
    assert not is_archetype_id("openEHR-EHR.example.v1")
    assert not is_archetype_id("openEHR-EHR-OBSERVATION.example.1")
    assert not is_archetype_id("openEHR-EHR-OBSERVATION.example.v1.")


def test_is_archetype_id_accepts_multi_segment_version() -> None:
    assert is_archetype_id("openEHR-EHR-OBSERVATION.example.v1.0.0")
