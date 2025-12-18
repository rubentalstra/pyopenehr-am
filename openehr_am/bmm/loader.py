"""BMM loader (subset): ODIN -> BMM dataclasses.

This is a permissive loader: it should never raise for malformed BMM content.
Instead, it returns `(model, issues)`.

# Spec: https://specifications.openehr.org/releases/BASE/latest/bmm.html
"""

from dataclasses import dataclass
from pathlib import Path

from openehr_am.bmm.model import Class, Model, Multiplicity, Package, Property, TypeRef
from openehr_am.odin.ast import (
    OdinBoolean,
    OdinInteger,
    OdinKeyedList,
    OdinList,
    OdinNode,
    OdinNull,
    OdinObject,
    OdinPrimitive,
    OdinReal,
    OdinString,
)
from openehr_am.odin.parser import parse_odin
from openehr_am.validation.issue import Issue, Severity


@dataclass(slots=True, frozen=True)
class _Ctx:
    filename: str | None


def load_bmm(path: str | Path) -> tuple[Model | None, list[Issue]]:
    """Load a BMM schema file (ODIN) into `Model`.

    This currently supports only a small subset:
    - `model_name` (string)
    - `packages` (keyed list)
      - package: `name` (string, optional), `packages` (keyed list), `classes` (keyed list)
      - class: `name` (optional), `parent` (optional), `properties` (keyed list)
      - property: `name` (optional), `type` (string or object), `multiplicity` (object)

    Returns:
        `(model, issues)` where `model` is None on fatal shape errors.

    Raises:
        OSError: if the file cannot be read.
    """

    p = Path(path)
    text = p.read_text(encoding="utf-8")

    node, issues = parse_odin(text, filename=str(p))
    if node is None:
        return None, issues

    ctx = _Ctx(filename=str(p))

    try:
        model = _build_model(node, ctx, issues)
        return model, issues
    except (AttributeError, TypeError, ValueError, IndexError, KeyError) as e:
        # Loader must not raise for malformed artefacts.
        issues.append(
            Issue(
                code="BMM550",
                severity=Severity.ERROR,
                message=f"BMM load failed: {e}",
                file=ctx.filename,
            )
        )
        return None, issues


def _build_model(node: OdinNode, ctx: _Ctx, issues: list[Issue]) -> Model | None:
    obj = _expect_object(node, ctx, issues, where="root")
    if obj is None:
        return None

    allowed = {"model_name", "packages"}
    _warn_unknown_keys(obj, allowed, ctx, issues)

    model_name = _get_string(obj, "model_name", ctx, issues, required=True)
    if model_name is None:
        return None

    model = Model(name=model_name)

    packages_node = _get_node(obj, "packages")
    if packages_node is None:
        return model

    pkgs = _expect_keyed_list(packages_node, ctx, issues, where="packages")
    if pkgs is None:
        return model

    for item in pkgs.items:
        key = _primitive_to_str(item.key)
        if key is None:
            _add_issue(
                issues,
                code="BMM550",
                severity=Severity.ERROR,
                message="Package key must be a string",
                ctx=ctx,
                span=item.span,
            )
            continue

        pkg = _build_package(key, item.value, ctx, issues)
        if pkg is not None:
            model.add_package(pkg)

    return model


def _build_package(
    key: str, node: OdinNode, ctx: _Ctx, issues: list[Issue]
) -> Package | None:
    obj = _expect_object(node, ctx, issues, where=f"package[{key}]")
    if obj is None:
        return None

    allowed = {"name", "packages", "classes"}
    _warn_unknown_keys(obj, allowed, ctx, issues)

    name = _get_string(obj, "name", ctx, issues, required=False) or key
    pkg = Package(name=name)

    # Subpackages.
    sub_pkgs_node = _get_node(obj, "packages")
    sub_pkgs = (
        _expect_keyed_list(
            sub_pkgs_node, ctx, issues, where=f"package[{name}].packages"
        )
        if sub_pkgs_node is not None
        else None
    )
    if sub_pkgs is not None:
        for item in sub_pkgs.items:
            sub_key = _primitive_to_str(item.key)
            if sub_key is None:
                _add_issue(
                    issues,
                    code="BMM550",
                    severity=Severity.ERROR,
                    message="Subpackage key must be a string",
                    ctx=ctx,
                    span=item.span,
                )
                continue
            sub = _build_package(sub_key, item.value, ctx, issues)
            if sub is not None:
                pkg.add_package(sub)

    # Classes.
    classes_node = _get_node(obj, "classes")
    classes = (
        _expect_keyed_list(classes_node, ctx, issues, where=f"package[{name}].classes")
        if classes_node is not None
        else None
    )

    if classes is not None:
        for item in classes.items:
            cls_key = _primitive_to_str(item.key)
            if cls_key is None:
                _add_issue(
                    issues,
                    code="BMM550",
                    severity=Severity.ERROR,
                    message="Class key must be a string",
                    ctx=ctx,
                    span=item.span,
                )
                continue

            cls = _build_class(cls_key, item.value, ctx, issues)
            if cls is not None:
                pkg.add_class(cls)

    return pkg


def _build_class(
    key: str, node: OdinNode, ctx: _Ctx, issues: list[Issue]
) -> Class | None:
    obj = _expect_object(node, ctx, issues, where=f"class[{key}]")
    if obj is None:
        return None

    allowed = {"name", "parent", "properties"}
    _warn_unknown_keys(obj, allowed, ctx, issues)

    name = _get_string(obj, "name", ctx, issues, required=False) or key
    parent = _get_string(obj, "parent", ctx, issues, required=False)

    cls = Class(name=name, parent=parent)

    props_node = _get_node(obj, "properties")
    props = (
        _expect_keyed_list(props_node, ctx, issues, where=f"class[{name}].properties")
        if props_node is not None
        else None
    )
    if props is None:
        return cls

    for item in props.items:
        prop_key = _primitive_to_str(item.key)
        if prop_key is None:
            _add_issue(
                issues,
                code="BMM550",
                severity=Severity.ERROR,
                message="Property key must be a string",
                ctx=ctx,
                span=item.span,
            )
            continue

        prop = _build_property(prop_key, item.value, ctx, issues)
        if prop is not None:
            cls.add_property(prop)

    return cls


def _build_property(
    key: str, node: OdinNode, ctx: _Ctx, issues: list[Issue]
) -> Property | None:
    obj = _expect_object(node, ctx, issues, where=f"property[{key}]")
    if obj is None:
        return None

    allowed = {"name", "type", "multiplicity"}
    _warn_unknown_keys(obj, allowed, ctx, issues)

    name = _get_string(obj, "name", ctx, issues, required=False) or key

    type_node = _get_node(obj, "type")
    if type_node is None:
        _add_issue(
            issues,
            code="BMM540",
            severity=Severity.ERROR,
            message=f"Missing required property field: type (property {name!r})",
            ctx=ctx,
            span=obj.span,
        )
        return None

    type_ref = _build_type_ref(type_node, ctx, issues)
    if type_ref is None:
        return None

    mult = Multiplicity.one()
    mult_node = _get_node(obj, "multiplicity")
    if mult_node is not None:
        parsed = _build_multiplicity(mult_node, ctx, issues)
        if parsed is not None:
            mult = parsed

    return Property(name=name, type_ref=type_ref, multiplicity=mult)


def _build_type_ref(node: OdinNode, ctx: _Ctx, issues: list[Issue]) -> TypeRef | None:
    match node:
        case OdinString(value=v):
            return TypeRef(name=v)
        case OdinObject() as obj:
            allowed = {"name", "parameters", "nullable"}
            _warn_unknown_keys(obj, allowed, ctx, issues)

            name = _get_string(obj, "name", ctx, issues, required=True)
            if name is None:
                return None

            nullable = _get_bool(obj, "nullable", ctx, issues, required=False) or False

            params_node = _get_node(obj, "parameters")
            params: list[TypeRef] = []
            if params_node is not None:
                if isinstance(params_node, OdinList):
                    for item in params_node.items:
                        p = _build_type_ref(item, ctx, issues)
                        if p is not None:
                            params.append(p)
                elif isinstance(
                    params_node, (OdinString, OdinInteger, OdinReal, OdinBoolean)
                ):
                    p = _build_type_ref(params_node, ctx, issues)
                    if p is not None:
                        params.append(p)
                else:
                    _add_issue(
                        issues,
                        code="BMM550",
                        severity=Severity.ERROR,
                        message="type.parameters must be a primitive or list of primitives",
                        ctx=ctx,
                        span=getattr(params_node, "span", None),
                    )

            return TypeRef(name=name, parameters=tuple(params), nullable=nullable)
        case _:
            _add_issue(
                issues,
                code="BMM550",
                severity=Severity.ERROR,
                message="Invalid type reference shape",
                ctx=ctx,
                span=getattr(node, "span", None),
            )
            return None


def _build_multiplicity(
    node: OdinNode, ctx: _Ctx, issues: list[Issue]
) -> Multiplicity | None:
    obj = _expect_object(node, ctx, issues, where="multiplicity")
    if obj is None:
        return None

    allowed = {"lower", "upper"}
    _warn_unknown_keys(obj, allowed, ctx, issues)

    lower = _get_int(obj, "lower", ctx, issues, required=True)
    if lower is None:
        return None

    upper_node = _get_node(obj, "upper")
    upper: int | None
    if upper_node is None or isinstance(upper_node, OdinNull):
        upper = None
    elif isinstance(upper_node, OdinInteger):
        upper = upper_node.value
    elif isinstance(upper_node, OdinString) and upper_node.value == "*":
        upper = None
    else:
        _add_issue(
            issues,
            code="BMM550",
            severity=Severity.ERROR,
            message="Multiplicity.upper must be integer, null, or '*'",
            ctx=ctx,
            span=getattr(upper_node, "span", None),
        )
        return None

    try:
        return Multiplicity(lower=lower, upper=upper)
    except ValueError as e:
        _add_issue(
            issues,
            code="BMM550",
            severity=Severity.ERROR,
            message=f"Invalid multiplicity: {e}",
            ctx=ctx,
            span=obj.span,
        )
        return None


def _warn_unknown_keys(
    obj: OdinObject, allowed: set[str], ctx: _Ctx, issues: list[Issue]
) -> None:
    for item in obj.items:
        if item.key in allowed:
            continue
        issues.append(
            Issue(
                code="BMM530",
                severity=Severity.WARN,
                message=f"Unsupported BMM field: {item.key}",
                file=ctx.filename,
                line=item.key_span.start_line if item.key_span else None,
                col=item.key_span.start_col if item.key_span else None,
                end_line=item.key_span.end_line if item.key_span else None,
                end_col=item.key_span.end_col if item.key_span else None,
            )
        )


def _get_node(obj: OdinObject, key: str) -> OdinNode | None:
    for item in obj.items:
        if item.key == key:
            return item.value
    return None


def _get_string(
    obj: OdinObject,
    key: str,
    ctx: _Ctx,
    issues: list[Issue],
    *,
    required: bool,
) -> str | None:
    node = _get_node(obj, key)
    if node is None:
        if required:
            _add_issue(
                issues,
                code="BMM540",
                severity=Severity.ERROR,
                message=f"Missing required BMM field: {key}",
                ctx=ctx,
                span=obj.span,
            )
        return None

    if isinstance(node, OdinString):
        return node.value

    _add_issue(
        issues,
        code="BMM550",
        severity=Severity.ERROR,
        message=f"BMM field {key!r} must be a string",
        ctx=ctx,
        span=getattr(node, "span", None),
    )
    return None


def _get_int(
    obj: OdinObject,
    key: str,
    ctx: _Ctx,
    issues: list[Issue],
    *,
    required: bool,
) -> int | None:
    node = _get_node(obj, key)
    if node is None:
        if required:
            _add_issue(
                issues,
                code="BMM540",
                severity=Severity.ERROR,
                message=f"Missing required BMM field: {key}",
                ctx=ctx,
                span=obj.span,
            )
        return None

    if isinstance(node, OdinInteger):
        return node.value

    _add_issue(
        issues,
        code="BMM550",
        severity=Severity.ERROR,
        message=f"BMM field {key!r} must be an integer",
        ctx=ctx,
        span=getattr(node, "span", None),
    )
    return None


def _get_bool(
    obj: OdinObject,
    key: str,
    ctx: _Ctx,
    issues: list[Issue],
    *,
    required: bool,
) -> bool | None:
    node = _get_node(obj, key)
    if node is None:
        if required:
            _add_issue(
                issues,
                code="BMM540",
                severity=Severity.ERROR,
                message=f"Missing required BMM field: {key}",
                ctx=ctx,
                span=obj.span,
            )
        return None

    if isinstance(node, OdinBoolean):
        return node.value

    _add_issue(
        issues,
        code="BMM550",
        severity=Severity.ERROR,
        message=f"BMM field {key!r} must be a boolean",
        ctx=ctx,
        span=getattr(node, "span", None),
    )
    return None


def _expect_object(
    node: OdinNode, ctx: _Ctx, issues: list[Issue], *, where: str
) -> OdinObject | None:
    if isinstance(node, OdinObject):
        return node
    _add_issue(
        issues,
        code="BMM550",
        severity=Severity.ERROR,
        message=f"Expected ODIN object at {where}",
        ctx=ctx,
        span=getattr(node, "span", None),
    )
    return None


def _expect_keyed_list(
    node: OdinNode, ctx: _Ctx, issues: list[Issue], *, where: str
) -> OdinKeyedList | None:
    if isinstance(node, OdinKeyedList):
        return node
    _add_issue(
        issues,
        code="BMM550",
        severity=Severity.ERROR,
        message=f"Expected ODIN keyed list at {where}",
        ctx=ctx,
        span=getattr(node, "span", None),
    )
    return None


def _expect_list(
    node: OdinNode, ctx: _Ctx, issues: list[Issue], *, where: str
) -> OdinList | None:
    if isinstance(node, OdinList):
        return node
    _add_issue(
        issues,
        code="BMM550",
        severity=Severity.ERROR,
        message=f"Expected ODIN list at {where}",
        ctx=ctx,
        span=getattr(node, "span", None),
    )
    return None


def _primitive_to_str(p: OdinPrimitive) -> str | None:
    if isinstance(p, OdinString):
        return p.value
    if isinstance(p, OdinInteger):
        return str(p.value)
    if isinstance(p, OdinReal):
        return str(p.value)
    if isinstance(p, OdinBoolean):
        return "true" if p.value else "false"
    if isinstance(p, OdinNull):
        return None
    return None


def _add_issue(
    issues: list[Issue],
    *,
    code: str,
    severity: Severity,
    message: str,
    ctx: _Ctx,
    span,
) -> None:
    line = getattr(span, "start_line", None)
    col = getattr(span, "start_col", None)
    end_line = getattr(span, "end_line", None)
    end_col = getattr(span, "end_col", None)

    issues.append(
        Issue(
            code=code,
            severity=severity,
            message=message,
            file=ctx.filename,
            line=line,
            col=col,
            end_line=end_line,
            end_col=end_col,
        )
    )
