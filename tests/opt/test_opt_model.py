import dataclasses
import json

import pytest

from openehr_am.antlr.span import SourceSpan
from openehr_am.opt.model import (
    OperationalTemplate,
    OptCardinality,
    OptCAttribute,
    OptCComplexObject,
    OptCPrimitiveObject,
    OptIntegerConstraint,
    OptInterval,
)


def test_operational_template_to_json_is_deterministic() -> None:
    span = SourceSpan(file="x.opt", start_line=1, start_col=1, end_line=1, end_col=2)

    root = OptCComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        path="/",
        occurrences=OptInterval(0, 1, span=span),
        span=span,
    )

    opt = OperationalTemplate(
        template_id="openEHR-EHR-COMPOSITION.example_template.v1",
        definition=root,
        span=span,
    )

    j1 = opt.to_json()
    j2 = opt.to_json()
    assert j1 == j2

    # Matches json.dumps of the deterministic to_dict() with the same settings.
    assert j1 == json.dumps(
        opt.to_dict(),
        ensure_ascii=False,
        separators=(",", ":"),
        indent=None,
    )

    # Indented output is also deterministic.
    assert opt.to_json(indent=2) == opt.to_json(indent=2)


def test_opt_models_are_slots_and_frozen() -> None:
    interval = OptInterval(lower=0, upper=1)
    assert hasattr(interval, "__slots__")

    with pytest.raises(dataclasses.FrozenInstanceError):
        interval.lower = 1  # pyright: ignore[reportAttributeAccessIssue]


def test_operational_template_to_dict_is_deterministic_and_json_serializable() -> None:
    span = SourceSpan(file="x.opt", start_line=1, start_col=1, end_line=1, end_col=2)

    root = OptCComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0000",
        path="/",
        occurrences=OptInterval(0, 1, span=span),
        attributes=(
            OptCAttribute(
                rm_attribute_name="data",
                path="/data",
                cardinality=OptCardinality(
                    occurrences=OptInterval(0, None, span=span),
                    is_ordered=False,
                    is_unique=False,
                    span=span,
                ),
                children=(
                    OptCPrimitiveObject(
                        rm_type_name="Integer",
                        path="/data[at0001]/count",
                        constraint=OptIntegerConstraint(
                            interval=OptInterval(0, 10, span=span),
                            span=span,
                        ),
                        span=span,
                    ),
                ),
                span=span,
            ),
        ),
        span=span,
    )

    opt = OperationalTemplate(
        template_id="openEHR-EHR-COMPOSITION.example_template.v1",
        concept="at0000",
        original_language="en",
        language="en",
        root_archetype_id="openEHR-EHR-OBSERVATION.example.v1",
        component_archetype_ids=(
            "openEHR-EHR-OBSERVATION.example.v1",
            "openEHR-EHR-CLUSTER.other.v1",
        ),
        definition=root,
        span=span,
    )

    d1 = opt.to_dict()
    d2 = opt.to_dict()
    assert d1 == d2

    # Top-level key ordering is deterministic (dataclass field order).
    assert list(d1.keys()) == [
        "template_id",
        "concept",
        "original_language",
        "language",
        "root_archetype_id",
        "component_archetype_ids",
        "definition",
        "span",
    ]

    json.dumps(d1)
