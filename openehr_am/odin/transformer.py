"""ODIN ANTLR parse-tree -> syntax AST transformer.

This module converts an ANTLR parse tree produced from the ODIN grammar into our
syntax-layer AST dataclasses in :mod:`openehr_am.odin.ast`.

It is intentionally implemented using duck-typing so it can work with generated
ANTLR context classes without importing them here.

# Spec: https://specifications.openehr.org/releases/LANG/latest/odin.html
"""

from dataclasses import dataclass
from typing import Any, Protocol

from openehr_am.antlr.span import SourceSpan
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
    OdinPrimitive,
    OdinReal,
    OdinString,
)
from openehr_am.validation.issue import Issue, Severity


class _TokenLike(Protocol):
    line: int
    column: int
    text: str | None


class _CtxLike(Protocol):
    start: _TokenLike | None
    stop: _TokenLike | None

    def getText(self) -> str: ...  # noqa: N802 (ANTLR API)


@dataclass(slots=True)
class _TransformContext:
    filename: str | None


def transform_odin_parse_tree(
    tree: object,
    *,
    filename: str | None = None,
) -> tuple[OdinNode | None, list[Issue]]:
    """Transform an ODIN ANTLR parse tree into ODIN AST.

    Returns (node, issues). If transformation fails, node is None and issues
    contains at least one ERROR Issue with code ODN100.

    This function must not raise for malformed / unexpected parse-tree shapes.

    # Spec: https://specifications.openehr.org/releases/LANG/latest/odin.html
    """

    ctx = _TransformContext(filename=filename)
    issues: list[Issue] = []

    try:
        node = _to_node(tree, ctx, issues)
    except (
        AttributeError,
        TypeError,
        ValueError,
        IndexError,
        KeyError,
    ) as e:  # pragma: no cover
        issues.append(_issue("ODN100", f"ODIN transform failed: {e}", tree, ctx))
        return None, issues

    if issues and node is None:
        return None, issues

    return node, issues


def _to_node(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinNode | None:
    # The ODIN grammar has a few top-level shapes; we implement the subset needed
    # for ODIN blocks embedded in ADL: attr_vals, object_value_block, keyed_object.

    # 1) odin_text: prefer specific accessors if present.
    if _has_method(tree, "attr_vals") or _has_method(tree, "object_value_block"):
        return _visit_odin_text(tree, ctx, issues)

    # 2) value block directly.
    if _has_method(tree, "primitive_object") or _has_method(tree, "attr_vals"):
        return _visit_object_value_block(tree, ctx, issues)

    # 3) fallback by rule-name based on available members.
    if _has_method(tree, "primitive_value"):
        prim = _visit_primitive_object(tree, ctx, issues)
        if prim is not None:
            return prim

    # 4) allow a primitive_value context as the root (useful for unit tests and
    # embedded ODIN fragments).
    if any(
        _has_method(tree, name)
        for name in (
            "string_value",
            "integer_value",
            "real_value",
            "boolean_value",
        )
    ):
        prim2 = _visit_primitive_value(tree, ctx, issues)
        if prim2 is not None:
            return prim2

    issues.append(_issue("ODN100", "Unrecognised ODIN parse-tree root", tree, ctx))
    return None


def _visit_odin_text(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinNode | None:
    # odin_text : attr_vals | object_value_block | keyed_object+ | included_other_language;
    attr_vals = _call0(tree, "attr_vals")
    if attr_vals is not None:
        obj = _visit_attr_vals(attr_vals, ctx, issues)
        return obj

    ovb = _call0(tree, "object_value_block")
    if ovb is not None:
        return _visit_object_value_block(ovb, ctx, issues)

    keyed = _call_list(tree, "keyed_object")
    if keyed:
        items: list[OdinKeyedListItem] = []
        for k in keyed:
            item = _visit_keyed_object(k, ctx, issues)
            if item is not None:
                items.append(item)
        return OdinKeyedList(items=tuple(items), span=_span_from(tree, ctx))

    issues.append(_issue("ODN100", "Unsupported odin_text form", tree, ctx))
    return None


def _visit_attr_vals(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinObject:
    # attr_vals : ( attr_val ';'? )+ ;
    attr_vals = _call_list(tree, "attr_val")
    items: list[OdinObjectItem] = []

    for av in attr_vals:
        item = _visit_attr_val(av, ctx, issues)
        if item is not None:
            items.append(item)

    return OdinObject(items=tuple(items), span=_span_from(tree, ctx))


def _visit_attr_val(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinObjectItem | None:
    # attr_val : attribute_id '=' object_block ;
    attr_id = _call0(tree, "attribute_id")
    if attr_id is None:
        issues.append(_issue("ODN100", "Missing attribute_id", tree, ctx))
        return None

    key = attr_id.getText() if hasattr(attr_id, "getText") else str(attr_id)

    obj_block = _call0(tree, "object_block")
    if obj_block is None:
        issues.append(_issue("ODN100", "Missing object_block", tree, ctx))
        return None

    value = _visit_object_block(obj_block, ctx, issues)
    if value is None:
        return None

    return OdinObjectItem(
        key=key,
        value=value,
        key_span=_span_from(attr_id, ctx),
        span=_span_from(tree, ctx),
    )


def _visit_object_block(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinNode | None:
    # object_block : object_value_block | object_reference_block ;
    ovb = _call0(tree, "object_value_block")
    if ovb is not None:
        return _visit_object_value_block(ovb, ctx, issues)

    # References are not in scope for this task.
    issues.append(
        _issue("ODN100", "object_reference_block not supported yet", tree, ctx)
    )
    return None


def _visit_object_value_block(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinNode | None:
    # object_value_block : ( '(' type_id ')' )? '<' ( primitive_object | attr_vals? | keyed_object* ) '>' | EMBEDDED_URI;

    prim_obj = _call0(tree, "primitive_object")
    if prim_obj is not None:
        prim = _visit_primitive_object(prim_obj, ctx, issues)
        if prim is None:
            return None
        enclosing = _span_from(tree, ctx)
        if isinstance(prim, OdinList):
            return OdinList(items=prim.items, span=enclosing)
        return _with_span_if_missing(prim, enclosing)

    attr_vals = _call0(tree, "attr_vals")
    if attr_vals is not None:
        obj = _visit_attr_vals(attr_vals, ctx, issues)
        return OdinObject(items=obj.items, span=_span_from(tree, ctx))

    keyed = _call_list(tree, "keyed_object")
    if keyed:
        items: list[OdinKeyedListItem] = []
        for k in keyed:
            item = _visit_keyed_object(k, ctx, issues)
            if item is not None:
                items.append(item)
        return OdinKeyedList(items=tuple(items), span=_span_from(tree, ctx))

    # Empty <> is an empty object.
    return OdinObject(items=(), span=_span_from(tree, ctx))


def _visit_keyed_object(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinKeyedListItem | None:
    # keyed_object : '[' primitive_value ']' '=' object_block ;
    pv = _call0(tree, "primitive_value")
    if pv is None:
        issues.append(
            _issue("ODN100", "Missing primitive_value in keyed_object", tree, ctx)
        )
        return None

    key = _visit_primitive_value(pv, ctx, issues)
    if key is None:
        return None

    ob = _call0(tree, "object_block")
    if ob is None:
        issues.append(
            _issue("ODN100", "Missing object_block in keyed_object", tree, ctx)
        )
        return None

    value = _visit_object_block(ob, ctx, issues)
    if value is None:
        return None

    return OdinKeyedListItem(key=key, value=value, span=_span_from(tree, ctx))


def _visit_primitive_object(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinPrimitive | OdinList | None:
    # primitive_object : primitive_value | primitive_list_value | primitive_interval_value;
    pv = _call0(tree, "primitive_value")
    if pv is not None:
        return _visit_primitive_value(pv, ctx, issues)

    pl = _call0(tree, "primitive_list_value")
    if pl is not None:
        prims = _call_list(pl, "primitive_value")
        items: list[OdinPrimitive] = []
        for p in prims:
            item = _visit_primitive_value(p, ctx, issues)
            if item is not None:
                items.append(item)
        return OdinList(items=tuple(items), span=_span_from(tree, ctx))

    issues.append(_issue("ODN100", "Unsupported primitive_object form", tree, ctx))
    return None


def _visit_primitive_value(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinPrimitive | None:
    # primitive_value : string_value | integer_value | real_value | boolean_value | ...

    sv = _call0(tree, "string_value")
    if sv is not None:
        return _visit_string_value(sv, ctx, issues)

    iv = _call0(tree, "integer_value")
    if iv is not None:
        return _visit_integer_value(iv, ctx, issues)

    rv = _call0(tree, "real_value")
    if rv is not None:
        return _visit_real_value(rv, ctx, issues)

    bv = _call0(tree, "boolean_value")
    if bv is not None:
        return _visit_boolean_value(bv, ctx)

    # Not yet supported (dates, character, intervals, coded terms, etc.).
    issues.append(_issue("ODN100", "Unsupported primitive_value", tree, ctx))
    return None


def _visit_string_value(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinString | None:
    get_text = getattr(tree, "getText", None)
    raw = str(get_text()) if callable(get_text) else str(tree)
    try:
        decoded = _decode_odin_string(raw)
    except ValueError as e:
        issues.append(_issue("ODN100", str(e), tree, ctx))
        return None

    return OdinString(value=decoded, span=_span_from(tree, ctx))


def _visit_integer_value(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinPrimitive | None:
    get_text = getattr(tree, "getText", None)
    text = str(get_text()) if callable(get_text) else str(tree)
    try:
        return _number_to_node(text, span=_span_from(tree, ctx))
    except ValueError as e:
        issues.append(_issue("ODN100", str(e), tree, ctx))
        return None


def _visit_real_value(
    tree: object, ctx: _TransformContext, issues: list[Issue]
) -> OdinPrimitive | None:
    get_text = getattr(tree, "getText", None)
    text = str(get_text()) if callable(get_text) else str(tree)
    try:
        return _number_to_node(text, span=_span_from(tree, ctx))
    except ValueError as e:
        issues.append(_issue("ODN100", str(e), tree, ctx))
        return None


def _visit_boolean_value(tree: object, ctx: _TransformContext) -> OdinBoolean:
    get_text = getattr(tree, "getText", None)
    text = str(get_text()) if callable(get_text) else str(tree)
    value = text.casefold() == "true"
    return OdinBoolean(value=value, span=_span_from(tree, ctx))


def _decode_odin_string(token_text: str) -> str:
    """Decode an ODIN STRING token text.

    The ODIN grammar's STRING terminal includes double quotes.
    We implement a minimal escape set: \\n, \\r, \\t, \\\\ and \\".

    Raises ValueError on invalid quoting/escapes.

    # Spec: https://specifications.openehr.org/releases/LANG/latest/odin.html (Special Character Sequences)
    """

    if (
        len(token_text) < 2
        or not token_text.startswith('"')
        or not token_text.endswith('"')
    ):
        raise ValueError("Invalid ODIN string token (missing quotes)")

    inner = token_text[1:-1]
    out: list[str] = []
    i = 0
    while i < len(inner):
        ch = inner[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue

        i += 1
        if i >= len(inner):
            raise ValueError("Unterminated escape sequence in ODIN string")

        esc = inner[i]
        i += 1
        match esc:
            case "n":
                out.append("\n")
            case "r":
                out.append("\r")
            case "t":
                out.append("\t")
            case "\\":
                out.append("\\")
            case '"':
                out.append('"')
            case _:
                raise ValueError(f"Illegal escape sequence \\{esc} in ODIN string")

    return "".join(out)


def _number_to_node(text: str, *, span: SourceSpan | None) -> OdinPrimitive:
    s = text.strip()

    if any(ch in s for ch in "."):
        return OdinReal(value=float(s), span=span)

    if "e" in s.casefold():
        mantissa_s, exp_s = s.casefold().split("e", 1)
        mantissa = int(mantissa_s)
        exp = int(exp_s)
        if exp >= 0:
            return OdinInteger(value=mantissa * (10**exp), span=span)
        return OdinReal(value=mantissa * (10.0**exp), span=span)

    return OdinInteger(value=int(s), span=span)


def _with_span_if_missing(
    node: OdinPrimitive, span: SourceSpan | None
) -> OdinPrimitive:
    if span is None:
        return node

    match node:
        case OdinString(value=v, span=None):
            return OdinString(value=v, span=span)
        case OdinInteger(value=v, span=None):
            return OdinInteger(value=v, span=span)
        case OdinReal(value=v, span=None):
            return OdinReal(value=v, span=span)
        case OdinBoolean(value=v, span=None):
            return OdinBoolean(value=v, span=span)
        case OdinNull(span=None):
            return OdinNull(span=span)
        case _:
            return node


def _span_from(tree: object, ctx: _TransformContext) -> SourceSpan | None:
    start = getattr(tree, "start", None)
    stop = getattr(tree, "stop", None)

    if start is None or stop is None:
        return None

    start_line = getattr(start, "line", None)
    start_column = getattr(start, "column", None)
    stop_line = getattr(stop, "line", None)
    stop_column = getattr(stop, "column", None)
    stop_text = getattr(stop, "text", None)

    if not isinstance(start_line, int):
        return None
    if not isinstance(start_column, int):
        return None
    if not isinstance(stop_line, int):
        return None
    if not isinstance(stop_column, int):
        return None

    stop_text_s = stop_text if isinstance(stop_text, str) else None

    start_col = start_column + 1  # ANTLR is 0-based.
    end_col = (
        (stop_column + 1) if stop_text_s is None else (stop_column + len(stop_text_s))
    )

    return SourceSpan(
        file=ctx.filename,
        start_line=start_line,
        start_col=start_col,
        end_line=stop_line,
        end_col=end_col,
    )


def _issue(code: str, message: str, tree: object, ctx: _TransformContext) -> Issue:
    span = _span_from(tree, ctx)
    return Issue(
        code=code,
        severity=Severity.ERROR,
        message=message,
        file=ctx.filename,
        line=None if span is None else span.start_line,
        col=None if span is None else span.start_col,
        end_line=None if span is None else span.end_line,
        end_col=None if span is None else span.end_col,
    )


def _has_method(obj: object, name: str) -> bool:
    value = getattr(obj, name, None)
    return callable(value)


def _call0(obj: object, name: str) -> Any | None:
    fn = getattr(obj, name, None)
    if not callable(fn):
        return None

    try:
        return fn()
    except TypeError:
        return None


def _call_list(obj: object, name: str) -> list[Any]:
    fn = getattr(obj, name, None)
    if not callable(fn):
        return []

    # ANTLR context accessors are typically overloaded:
    # - foo() -> list[FooContext]
    # - foo(i: int) -> FooContext
    try:
        value = fn()
    except TypeError:
        value = None

    if value is None:
        # Try indexed access until it fails.
        out: list[Any] = []
        i = 0
        while True:
            try:
                item = fn(i)
            except (TypeError, IndexError, AttributeError):
                break
            out.append(item)
            i += 1
        return out

    if isinstance(value, list):
        return value

    return [value]
