from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.opt import register_opt_check, validate_opt


def test_validate_opt_runs_registered_check(monkeypatch) -> None:
    # Use a fresh registry to avoid leaking global registrations across tests.
    from openehr_am.validation import opt as opt_module
    from openehr_am.validation.registry import ValidationRegistry

    fresh_registry = ValidationRegistry()
    monkeypatch.setattr(opt_module, "DEFAULT_REGISTRY", fresh_registry)

    seen: list[object] = []

    def stub_check(ctx: ValidationContext):
        seen.append(ctx.artefact)
        return [
            Issue(
                code="OPT750",
                severity=Severity.ERROR,
                message="stub opt failure",
                file="x",
                line=2,
                col=1,
            )
        ]

    register_opt_check(stub_check)

    opt_obj = object()
    issues = validate_opt(opt_obj)

    assert seen == [opt_obj]
    assert [i.code for i in issues] == ["OPT750"]


def test_validate_opt_duplicate_component_archetype_ids_emits_opt750() -> None:
    from openehr_am.opt.model import OperationalTemplate

    opt = OperationalTemplate(
        template_id="t.v1",
        component_archetype_ids=("a.v1", "a.v1"),
        root_archetype_id="a.v1",
    )

    issues = validate_opt(opt)

    assert any(i.code == "OPT750" for i in issues)
    assert any("Duplicate archetype id" in i.message for i in issues)


def test_validate_opt_root_not_in_components_emits_opt750() -> None:
    from openehr_am.opt.model import OperationalTemplate

    opt = OperationalTemplate(
        template_id="t.v1",
        component_archetype_ids=("a.v1",),
        root_archetype_id="b.v1",
    )

    issues = validate_opt(opt)

    assert any(i.code == "OPT750" for i in issues)
    assert any("root_archetype_id is not included" in i.message for i in issues)


def test_validate_opt_duplicate_object_paths_emits_opt750() -> None:
    from openehr_am.opt.model import (
        OperationalTemplate,
        OptCAttribute,
        OptCComplexObject,
    )

    dup_child_1 = OptCComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0001",
        path="/content[at0001]",
        attributes=(),
    )
    dup_child_2 = OptCComplexObject(
        rm_type_name="OBSERVATION",
        node_id="at0001",
        path="/content[at0001]",
        attributes=(),
    )

    root = OptCComplexObject(
        rm_type_name="COMPOSITION",
        path="/",
        attributes=(
            OptCAttribute(
                rm_attribute_name="content",
                path="/content",
                children=(dup_child_1, dup_child_2),
            ),
        ),
    )

    opt = OperationalTemplate(
        template_id="t.v1",
        root_archetype_id="a.v1",
        component_archetype_ids=("a.v1",),
        definition=root,
    )

    issues = validate_opt(opt)

    assert any(i.code == "OPT750" for i in issues)
    assert any("Duplicate object path" in i.message for i in issues)
