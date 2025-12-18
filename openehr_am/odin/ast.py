"""ODIN syntax-layer AST nodes.

This module models ODIN values as a small, immutable syntax AST.

Parsing code should attach a best-effort :class:`~openehr_am.antlr.span.SourceSpan`
where feasible.

No semantic validation belongs here.
"""

from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan


@dataclass(slots=True, frozen=True)
class OdinString:
    value: str
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OdinInteger:
    value: int
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OdinReal:
    value: float
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OdinBoolean:
    value: bool
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OdinNull:
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OdinObjectItem:
    key: str
    value: OdinNode

    key_span: SourceSpan | None = None
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OdinObject:
    items: tuple[OdinObjectItem, ...]
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OdinList:
    items: tuple[OdinNode, ...]
    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OdinKeyedListItem:
    key: OdinPrimitive
    value: OdinNode

    span: SourceSpan | None = None


@dataclass(slots=True, frozen=True)
class OdinKeyedList:
    items: tuple[OdinKeyedListItem, ...]
    span: SourceSpan | None = None


type OdinPrimitive = OdinString | OdinInteger | OdinReal | OdinBoolean | OdinNull


type OdinNode = OdinPrimitive | OdinObject | OdinList | OdinKeyedList


__all__ = [
    "OdinBoolean",
    "OdinInteger",
    "OdinKeyedList",
    "OdinKeyedListItem",
    "OdinList",
    "OdinNode",
    "OdinNull",
    "OdinObject",
    "OdinObjectItem",
    "OdinPrimitive",
    "OdinReal",
    "OdinString",
]
