"""ODIN syntax AST -> ODIN text.

This is primarily intended for debugging and for round-trip tests.

The emitter targets the subset of ODIN currently supported by
:func:`openehr_am.odin.parser.parse_odin`.

# Spec: https://specifications.openehr.org/releases/LANG/latest/odin.html
"""

import math

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


def to_odin(node: OdinNode) -> str:
    """Render an ODIN node back to ODIN text.

    This function emits a deterministic ODIN representation for the currently
    supported ODIN subset.

    It may raise ValueError for AST shapes that cannot be represented in the
    supported subset (e.g. empty lists).
    """

    match node:
        case OdinObject():
            return _emit_object_document(node)
        case OdinKeyedList():
            return _emit_keyed_list_document(node)
        case _:
            return _emit_object_block(node)


def _emit_object_document(obj: OdinObject) -> str:
    if not obj.items:
        return "<>"

    parts: list[str] = []
    for item in obj.items:
        parts.append(_emit_object_item(item))

    return "; ".join(parts)


def _emit_object_item(item: OdinObjectItem) -> str:
    if not _is_ident(item.key):
        raise ValueError(f"Invalid ODIN identifier key: {item.key!r}")

    return f"{item.key} = {_emit_object_block(item.value)}"


def _emit_keyed_list_document(klist: OdinKeyedList) -> str:
    if not klist.items:
        raise ValueError(
            "Empty ODIN keyed lists are not representable in the supported subset"
        )

    return "\n".join(_emit_keyed_list_item(it) for it in klist.items)


def _emit_object_block(node: OdinNode) -> str:
    """Emit a node as an ODIN `object_block`.

    In the supported subset this always renders as an `object_value_block`:
    `< ... >`.
    """

    match node:
        case OdinObject(items=items):
            if not items:
                return "<>"
            inner = "; ".join(_emit_object_item(it) for it in items)
            return f"<{inner}>"

        case OdinKeyedList(items=items):
            if not items:
                raise ValueError(
                    "Empty ODIN keyed lists are not representable in the supported subset"
                )
            inner = "; ".join(_emit_keyed_list_item(it) for it in items)
            return f"<{inner}>"

        case OdinList(items=items):
            if not items:
                raise ValueError(
                    "Empty ODIN lists are not representable in the supported subset"
                )
            prims: list[str] = []
            for it in items:
                match it:
                    case (
                        OdinString()
                        | OdinInteger()
                        | OdinReal()
                        | OdinBoolean()
                        | OdinNull()
                    ):
                        prims.append(_emit_primitive_literal(it))
                    case _:
                        raise ValueError(
                            "ODIN list items must be primitives in the supported subset"
                        )
            return f"<{','.join(prims)}>"

        case _ if _is_primitive(node):
            return f"<{_emit_primitive_literal(node)}>"

        case _:
            raise ValueError(f"Unsupported ODIN node type: {type(node).__name__}")


def _emit_keyed_list_item(item: OdinKeyedListItem) -> str:
    return f"[{_emit_primitive_literal(item.key)}] = {_emit_object_block(item.value)}"


def _emit_primitive_literal(node: OdinPrimitive) -> str:
    match node:
        case OdinString(value=v):
            return _quote_string(v)
        case OdinInteger(value=v):
            return str(v)
        case OdinReal(value=v):
            if not math.isfinite(v):
                raise ValueError(
                    "Non-finite floats are not representable in the supported ODIN subset"
                )
            return repr(v)
        case OdinBoolean(value=v):
            return "True" if v else "False"
        case OdinNull():
            return "Null"
        case _:
            raise ValueError(f"Unsupported ODIN primitive type: {type(node).__name__}")


def _quote_string(value: str) -> str:
    out: list[str] = ['"']

    for ch in value:
        match ch:
            case "\\":
                out.append("\\\\")
            case '"':
                out.append('\\"')
            case "\n":
                out.append("\\n")
            case "\r":
                out.append("\\r")
            case "\t":
                out.append("\\t")
            case _:
                if ord(ch) < 0x20:
                    raise ValueError(
                        "Control characters are not representable in the supported ODIN subset"
                    )
                out.append(ch)

    out.append('"')
    return "".join(out)


def _is_ident(s: str) -> bool:
    if not s:
        return False
    first = s[0]
    if not (first.isalpha() or first == "_"):
        return False
    return all(ch.isalnum() or ch == "_" for ch in s)


def _is_primitive(node: OdinNode) -> bool:
    return isinstance(
        node,
        (
            OdinString,
            OdinInteger,
            OdinReal,
            OdinBoolean,
            OdinNull,
        ),
    )
