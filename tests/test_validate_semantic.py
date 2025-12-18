from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.semantic import register_semantic_check, validate_semantic


def test_validate_semantic_runs_registered_check(monkeypatch) -> None:
    # Use a fresh registry to avoid leaking global registrations across tests.
    from openehr_am.validation import semantic as semantic_module
    from openehr_am.validation.registry import ValidationRegistry

    fresh_registry = ValidationRegistry()
    monkeypatch.setattr(semantic_module, "DEFAULT_REGISTRY", fresh_registry)

    aom_obj = object()
    seen: list[object] = []

    def stub_check(ctx: ValidationContext):
        seen.append(ctx.artefact)
        return [
            Issue(
                code="AOM205",
                severity=Severity.ERROR,
                message="stub semantic failure",
                file="x",
                line=2,
                col=1,
            )
        ]

    register_semantic_check(stub_check)
    issues = validate_semantic(aom_obj)

    assert seen == [aom_obj]
    assert [i.code for i in issues] == ["AOM205"]
