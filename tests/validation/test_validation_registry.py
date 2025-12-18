from openehr_am.validation.context import ValidationContext
from openehr_am.validation.issue import Issue, Severity
from openehr_am.validation.registry import ValidationLayer, ValidationRegistry


def test_registry_runs_layers_in_pipeline_order() -> None:
    registry = ValidationRegistry()
    called: list[str] = []

    def make_check(layer: ValidationLayer):
        def check(_ctx: ValidationContext):
            called.append(layer.value)
            return []

        return check

    for layer in (
        ValidationLayer.SYNTAX,
        ValidationLayer.SEMANTIC,
        ValidationLayer.RM,
        ValidationLayer.OPT,
    ):
        registry.register(layer, make_check(layer), name=f"check_{layer.value}")

    registry.run(ValidationContext(artefact=object()))

    assert called == ["syntax", "semantic", "rm", "opt"]


def test_registry_runs_within_layer_deterministically() -> None:
    registry = ValidationRegistry()
    called: list[str] = []

    def check_a(_ctx: ValidationContext):
        called.append("a")
        return []

    def check_b(_ctx: ValidationContext):
        called.append("b")
        return []

    def check_c(_ctx: ValidationContext):
        called.append("c")
        return []

    registry.register(ValidationLayer.SYNTAX, check_b, name="b", priority=0)
    registry.register(ValidationLayer.SYNTAX, check_a, name="a", priority=0)
    registry.register(ValidationLayer.SYNTAX, check_c, name="c", priority=10)

    registry.run(ValidationContext(artefact=object()), layers=[ValidationLayer.SYNTAX])

    assert called == ["c", "a", "b"]


def test_registry_layer_filtering_uses_pipeline_order_for_subset() -> None:
    registry = ValidationRegistry()
    called: list[str] = []

    def check_syntax(_ctx: ValidationContext):
        called.append("syntax")
        return []

    def check_opt(_ctx: ValidationContext):
        called.append("opt")
        return []

    registry.register(ValidationLayer.SYNTAX, check_syntax)
    registry.register(ValidationLayer.OPT, check_opt)

    # Even if the caller passes layers out-of-order, execution follows
    # the standard pipeline order.
    registry.run(
        ValidationContext(artefact=object()),
        layers=[ValidationLayer.OPT, ValidationLayer.SYNTAX],
    )

    assert called == ["syntax", "opt"]


def test_registry_returns_issues_sorted_deterministically() -> None:
    registry = ValidationRegistry()

    def check(_ctx: ValidationContext):
        return [
            Issue(
                code="AOM200", severity=Severity.ERROR, message="b", file="b", line=2
            ),
            Issue(
                code="AOM200", severity=Severity.ERROR, message="a", file="a", line=1
            ),
        ]

    registry.register(ValidationLayer.SEMANTIC, check)

    issues = registry.run(ValidationContext(artefact=object()))

    assert [issue.file for issue in issues] == ["a", "b"]
