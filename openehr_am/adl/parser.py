"""ADL parser (MVP).

Public entrypoint: :func:`parse_adl`.

This is a parsing-layer module: it must never raise for invalid ADL input.
Instead, it returns `Issue` objects.

The MVP parser only extracts:
- artefact kind
- artefact id
- language/original_language (best-effort, from the language ODIN block)
- ODIN blocks for: language, description, terminology

The definition section is recognised (minimal cADL subset supported).
The rules section is captured as raw text + best-effort spans (no parsing/evaluation).

# Spec: https://specifications.openehr.org/releases/AM/latest/ADL2.html
"""

from dataclasses import dataclass, replace
from typing import Literal

from openehr_am.adl.ast import (
    AdlArtefact,
    AdlRulesSection,
    AdlRuleStatement,
    AdlSectionPlaceholder,
    ArtefactKind,
)
from openehr_am.adl.cadl_ast import (
    CadlArchetypeSlot,
    CadlArchetypeSlotPattern,
    CadlAttributeNode,
    CadlBooleanConstraint,
    CadlCardinality,
    CadlIntegerConstraint,
    CadlIntegerInterval,
    CadlObjectNode,
    CadlOccurrences,
    CadlPrimitiveConstraint,
    CadlRealConstraint,
    CadlRealInterval,
    CadlStringConstraint,
)
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
from openehr_am.odin.parser import parse_odin
from openehr_am.validation.issue import Issue, Severity


def parse_adl(
    text: str, *, filename: str | None = None
) -> tuple[AdlArtefact | None, list[Issue]]:
    """Parse ADL text into a minimal syntax AST.

    Args:
        text: ADL text.
        filename: Optional filename used for source spans and Issues.

    Returns:
        (artefact, issues). On structural failure, artefact is None.

    Notes:
        - This function never raises for invalid ADL input.
        - Only header + a small subset of sections are extracted.

    # Spec: https://specifications.openehr.org/releases/AM/latest/ADL2.html
    """

    if not isinstance(text, str):
        raise TypeError("parse_adl expects 'text' to be str")

    lines = text.splitlines(keepends=True)
    if not lines:
        issue = Issue(
            code="ADL001",
            severity=Severity.ERROR,
            message="Empty input",
            file=filename,
            line=1,
            col=1,
        )
        return None, [issue]

    kind, kind_span, kind_line_index = _parse_kind(lines, filename=filename)
    issues: list[Issue] = []

    if kind is ArtefactKind.UNKNOWN:
        issues.append(
            Issue(
                code="ADL020",
                severity=Severity.WARN,
                message="Unknown or missing ADL artefact kind",
                file=filename,
                line=kind_span.start_line if kind_span else 1,
                col=kind_span.start_col if kind_span else 1,
            )
        )

    artefact_id, artefact_id_span = _parse_artefact_id(
        lines, start_index=kind_line_index + 1, filename=filename
    )
    if artefact_id is None:
        issues.append(
            Issue(
                code="ADL001",
                severity=Severity.ERROR,
                message="Missing artefact id",
                file=filename,
                line=(kind_span.end_line if kind_span else 1),
                col=1,
            )
        )
        return None, issues

    section_map = _find_sections(lines)

    parent_archetype_id, parent_archetype_id_span, parent_issues = (
        _parse_specialise_section(lines, section_map, filename=filename)
    )
    issues.extend(parent_issues)

    language_node, _language_span, language_issues = _parse_odin_section(
        lines,
        section_map,
        name="language",
        filename=filename,
    )
    issues.extend(language_issues)

    description_node, description_span, description_issues = _parse_odin_section(
        lines,
        section_map,
        name="description",
        filename=filename,
    )
    issues.extend(description_issues)

    terminology_node, terminology_span, terminology_issues = _parse_odin_section(
        lines,
        section_map,
        name="terminology",
        filename=filename,
    )
    issues.extend(terminology_issues)

    original_language, language = _extract_language_fields(language_node)

    definition_node, definition_issues = _parse_definition_section(
        lines,
        section_map,
        filename=filename,
    )
    issues.extend(definition_issues)

    definition_placeholder = _placeholder_section(
        lines, section_map, "definition", filename
    )

    rules_section = _parse_rules_section(lines, section_map, filename=filename)

    root_span = _root_span(lines, filename=filename)

    artefact = AdlArtefact(
        kind=kind,
        artefact_id=artefact_id,
        parent_archetype_id=parent_archetype_id,
        original_language=original_language,
        language=language,
        description=description_node,
        terminology=terminology_node,
        definition=definition_node
        if definition_node is not None
        else definition_placeholder,
        rules=rules_section,
        span=root_span,
        kind_span=kind_span,
        artefact_id_span=artefact_id_span,
        original_language_span=None,
        language_span=None,
        description_span=description_span,
        terminology_span=terminology_span,
        parent_archetype_id_span=parent_archetype_id_span,
    )

    # Basic structural expectations.
    for required in ("language", "description", "terminology"):
        if required not in section_map:
            issues.append(
                Issue(
                    code="ADL010",
                    severity=Severity.ERROR,
                    message=f"Missing required section: {required}",
                    file=filename,
                    line=(artefact_id_span.end_line if artefact_id_span else 1),
                    col=1,
                )
            )

    # Attempt to attach spans for language/original_language keys if present.
    # This is best-effort and intentionally does not add Issues.
    if isinstance(language_node, OdinObject):
        for item in language_node.items:
            if item.key == "original_language" and item.key_span is not None:
                artefact = replace(artefact, original_language_span=item.key_span)
            if item.key == "language" and item.key_span is not None:
                artefact = replace(artefact, language_span=item.key_span)

    return artefact, issues


def _parse_specialise_section(
    lines: list[str],
    section_map: dict[str, int],
    *,
    filename: str | None,
) -> tuple[str | None, SourceSpan | None, list[Issue]]:
    """Parse ADL `specialise`/`specialize` section.

    This is best-effort and does not attempt semantic validation.

    # Spec: https://specifications.openehr.org/releases/AM/latest/ADL2.html
    """

    # Prefer British spelling if both appear.
    name = "specialise" if "specialise" in section_map else "specialize"
    if name not in section_map:
        return None, None, []

    rng = _section_content_range(lines, section_map, name)
    if rng is None:
        return None, None, []

    start_idx, end_idx = rng
    for idx in range(start_idx, end_idx):
        raw = lines[idx].rstrip("\n")
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("--"):
            continue

        # Span for the token within the line.
        start_col = (len(raw) - len(raw.lstrip(" \t"))) + 1
        end_col = start_col + len(stripped) - 1
        span = SourceSpan(
            file=filename,
            start_line=idx + 1,
            start_col=start_col,
            end_line=idx + 1,
            end_col=end_col,
        )
        return stripped, span, []

    # Header exists but no content.
    header_line = section_map[name] + 1
    return (
        None,
        None,
        [
            Issue(
                code="ADL010",
                severity=Severity.ERROR,
                message=f"Empty section content: {name}",
                file=filename,
                line=header_line,
                col=1,
            )
        ],
    )


# -----------------------
# Minimal cADL definition
# -----------------------


@dataclass(slots=True, frozen=True)
class _Token:
    kind: str
    value: str
    start_line: int
    start_col: int
    end_line: int
    end_col: int


_CADL_KEYWORDS = {
    "matches",
    "occurrences",
    "cardinality",
    "ordered",
    "unique",
    "archetype_slot",
    "include",
    "exclude",
    "true",
    "false",
}


def _parse_definition_section(
    lines: list[str],
    section_map: dict[str, int],
    *,
    filename: str | None,
) -> tuple[CadlObjectNode | None, list[Issue]]:
    rng = _section_content_range(lines, section_map, "definition")
    if rng is None:
        return None, []

    start_idx, end_idx = rng
    chunk_lines = lines[start_idx:end_idx]

    # Treat comment-only or whitespace-only definitions as "not present".
    meaningful = []
    for raw in chunk_lines:
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("--"):
            continue
        meaningful.append(raw)
    if not meaningful:
        return None, []

    chunk = "".join(chunk_lines)
    section_start_line = start_idx + 1

    try:
        tokens = _tokenize_cadl(chunk, section_start_line=section_start_line)
        parser = _CadlParser(tokens, filename=filename)
        root = parser.parse_object()
    except _CadlParseError as e:
        issue = Issue(
            code="ADL001",
            severity=Severity.ERROR,
            message=f"Definition parse failure (minimal subset): {e.message}",
            file=filename,
            line=e.line,
            col=e.col,
        )
        return None, [issue]

    validation_issues = root.validate(code="ADL030")
    return root, validation_issues


class _CadlParseError(Exception):
    def __init__(self, *, message: str, line: int, col: int) -> None:
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col


def _tokenize_cadl(chunk: str, *, section_start_line: int) -> list[_Token]:
    tokens: list[_Token] = []

    line = section_start_line
    col = 1
    i = 0

    def advance(n: int = 1) -> None:
        nonlocal i, line, col
        for _ in range(n):
            if i >= len(chunk):
                return
            ch = chunk[i]
            i += 1
            if ch == "\n":
                line += 1
                col = 1
            else:
                col += 1

    while i < len(chunk):
        ch = chunk[i]

        # Whitespace
        if ch.isspace():
            advance()
            continue

        # Comment to end of line
        if ch == "-" and i + 1 < len(chunk) and chunk[i + 1] == "-":
            while i < len(chunk) and chunk[i] != "\n":
                advance()
            continue

        start_line, start_col = line, col

        # Two-char operator
        if ch == "." and i + 1 < len(chunk) and chunk[i + 1] == ".":
            advance(2)
            tokens.append(_Token("DOTDOT", "..", start_line, start_col, line, col - 1))
            continue

        # Single-char symbols
        if ch in "{}[](),;*":
            advance()
            kind = {
                "{": "LBRACE",
                "}": "RBRACE",
                "[": "LBRACK",
                "]": "RBRACK",
                "(": "LPAREN",
                ")": "RPAREN",
                ",": "COMMA",
                ";": "SEMI",
                "*": "STAR",
            }[ch]
            tokens.append(_Token(kind, ch, start_line, start_col, line, col - 1))
            continue

        # String literal (double quotes)
        if ch == '"':
            advance()  # opening
            value_chars: list[str] = []
            while i < len(chunk):
                cur = chunk[i]
                if cur == "\\" and i + 1 < len(chunk):
                    # Minimal escape support.
                    advance()
                    value_chars.append(chunk[i])
                    advance()
                    continue
                if cur == '"':
                    break
                value_chars.append(cur)
                advance()
            if i >= len(chunk) or chunk[i] != '"':
                raise _CadlParseError(
                    message="Unterminated string literal",
                    line=start_line,
                    col=start_col,
                )
            advance()  # closing
            tokens.append(
                _Token(
                    "STRING",
                    "".join(value_chars),
                    start_line,
                    start_col,
                    line,
                    col - 1,
                )
            )
            continue

        # Regex literal (/.../)
        if ch == "/":
            advance()  # opening
            value_chars: list[str] = []
            escaped = False
            while i < len(chunk):
                cur = chunk[i]
                if cur == "\n":
                    raise _CadlParseError(
                        message="Unterminated regex literal",
                        line=start_line,
                        col=start_col,
                    )
                if escaped:
                    value_chars.append(cur)
                    escaped = False
                    advance()
                    continue
                if cur == "\\":
                    escaped = True
                    advance()
                    continue
                if cur == "/":
                    break
                value_chars.append(cur)
                advance()
            if i >= len(chunk) or chunk[i] != "/":
                raise _CadlParseError(
                    message="Unterminated regex literal",
                    line=start_line,
                    col=start_col,
                )
            advance()  # closing
            tokens.append(
                _Token(
                    "REGEX",
                    "".join(value_chars),
                    start_line,
                    start_col,
                    line,
                    col - 1,
                )
            )
            continue

        # Number (int/float)
        if ch.isdigit() or (
            ch == "-" and i + 1 < len(chunk) and chunk[i + 1].isdigit()
        ):
            num_chars: list[str] = []
            if ch == "-":
                num_chars.append("-")
                advance()
            saw_dot = False
            while i < len(chunk):
                cur = chunk[i]
                if cur.isdigit():
                    num_chars.append(cur)
                    advance()
                    continue
                if (
                    cur == "."
                    and not saw_dot
                    and not (i + 1 < len(chunk) and chunk[i + 1] == ".")
                ):
                    saw_dot = True
                    num_chars.append(".")
                    advance()
                    continue
                break
            tokens.append(
                _Token(
                    "NUMBER", "".join(num_chars), start_line, start_col, line, col - 1
                )
            )
            continue

        # Identifier / keyword
        if ch.isalpha() or ch in "_":
            ident_chars: list[str] = []
            while i < len(chunk):
                cur = chunk[i]
                if cur.isalnum() or cur in "_-.":
                    ident_chars.append(cur)
                    advance()
                    continue
                break
            value = "".join(ident_chars)
            kind = "KEYWORD" if value.casefold() in _CADL_KEYWORDS else "IDENT"
            tokens.append(_Token(kind, value, start_line, start_col, line, col - 1))
            continue

        raise _CadlParseError(
            message=f"Unexpected character: {ch!r}", line=line, col=col
        )

    tokens.append(_Token("EOF", "", line, col, line, col))
    return tokens


class _CadlParser:
    def __init__(self, tokens: list[_Token], *, filename: str | None) -> None:
        self._tokens = tokens
        self._i = 0
        self._file = filename

    def _peek(self) -> _Token:
        return self._tokens[self._i]

    def _advance(self) -> _Token:
        tok = self._tokens[self._i]
        self._i = min(self._i + 1, len(self._tokens) - 1)
        return tok

    def _expect(self, kind: str, *, value_casefold: str | None = None) -> _Token:
        tok = self._peek()
        if tok.kind != kind:
            raise _CadlParseError(
                message=f"Expected {kind}, got {tok.kind}",
                line=tok.start_line,
                col=tok.start_col,
            )
        if value_casefold is not None and tok.value.casefold() != value_casefold:
            raise _CadlParseError(
                message=f"Expected {value_casefold!r}, got {tok.value!r}",
                line=tok.start_line,
                col=tok.start_col,
            )
        return self._advance()

    def _span_from(self, start: _Token, end: _Token) -> SourceSpan:
        return SourceSpan(
            file=self._file,
            start_line=start.start_line,
            start_col=start.start_col,
            end_line=end.end_line,
            end_col=end.end_col,
        )

    def parse_object(self) -> CadlObjectNode:
        rm_type_tok = self._expect("IDENT")
        node_id: str | None = None
        node_id_span: SourceSpan | None = None

        if self._peek().kind == "LBRACK":
            self._advance()
            node_tok = self._expect("IDENT")
            self._expect("RBRACK")
            node_id = node_tok.value
            node_id_span = self._span_from(node_tok, node_tok)

        rm_span = self._span_from(rm_type_tok, rm_type_tok)

        occurrences: CadlOccurrences | None = None
        attributes: list[CadlAttributeNode] = []
        primitive: CadlPrimitiveConstraint | None = None
        slot: CadlArchetypeSlot | None = None

        if (
            self._peek().kind == "KEYWORD"
            and self._peek().value.casefold() == "matches"
        ):
            self._advance()
            lbrace = self._expect("LBRACE")

            # Decide whether this is a primitive constraint block or an object body.
            if self._looks_like_primitive_block():
                primitive = self._parse_primitive_constraint_block()
                rbrace = self._expect("RBRACE")
                span = self._span_from(rm_type_tok, rbrace)
                return CadlObjectNode(
                    rm_type_name=rm_type_tok.value,
                    node_id=node_id,
                    occurrences=None,
                    attributes=(),
                    primitive=primitive,
                    span=span,
                    rm_type_name_span=rm_span,
                    node_id_span=node_id_span,
                )

            # Object body
            while self._peek().kind != "RBRACE":
                if self._peek().kind == "EOF":
                    raise _CadlParseError(
                        message="Unterminated matches block",
                        line=lbrace.start_line,
                        col=lbrace.start_col,
                    )

                if (
                    self._peek().kind == "KEYWORD"
                    and self._peek().value.casefold() == "occurrences"
                ):
                    occurrences = self._parse_occurrences()
                    continue

                if (
                    self._peek().kind == "KEYWORD"
                    and self._peek().value.casefold() == "archetype_slot"
                ):
                    slot = self._parse_archetype_slot()
                    continue

                # Attribute: IDENT matches { ... }
                if self._peek().kind == "IDENT":
                    attributes.append(self._parse_attribute())
                    continue

                tok = self._peek()
                raise _CadlParseError(
                    message=f"Unexpected token in object body: {tok.kind} {tok.value!r}",
                    line=tok.start_line,
                    col=tok.start_col,
                )

            rbrace = self._expect("RBRACE")
            span = self._span_from(rm_type_tok, rbrace)
            return CadlObjectNode(
                rm_type_name=rm_type_tok.value,
                node_id=node_id,
                occurrences=occurrences,
                attributes=tuple(attributes),
                primitive=None,
                slot=slot,
                span=span,
                rm_type_name_span=rm_span,
                node_id_span=node_id_span,
            )

        # No matches block.
        span = self._span_from(rm_type_tok, rm_type_tok)
        return CadlObjectNode(
            rm_type_name=rm_type_tok.value,
            node_id=node_id,
            occurrences=None,
            attributes=(),
            primitive=None,
            slot=None,
            span=span,
            rm_type_name_span=rm_span,
            node_id_span=node_id_span,
        )

    def _parse_archetype_slot(self) -> CadlArchetypeSlot:
        slot_tok = self._expect("KEYWORD", value_casefold="archetype_slot")

        # Minimal subset: archetype_slot matches { include/exclude matches { <patterns> } }
        if self._peek().kind != "KEYWORD" or self._peek().value.casefold() != "matches":
            raise _CadlParseError(
                message="Expected 'matches' after 'archetype_slot'",
                line=self._peek().start_line,
                col=self._peek().start_col,
            )
        self._advance()
        lbrace = self._expect("LBRACE")

        includes: list[CadlArchetypeSlotPattern] = []
        excludes: list[CadlArchetypeSlotPattern] = []

        while self._peek().kind != "RBRACE":
            if self._peek().kind == "EOF":
                raise _CadlParseError(
                    message="Unterminated archetype_slot matches block",
                    line=lbrace.start_line,
                    col=lbrace.start_col,
                )

            if self._peek().kind != "KEYWORD" or self._peek().value.casefold() not in {
                "include",
                "exclude",
            }:
                tok = self._peek()
                raise _CadlParseError(
                    message=(
                        "Unexpected token in archetype_slot body: "
                        f"{tok.kind} {tok.value!r}"
                    ),
                    line=tok.start_line,
                    col=tok.start_col,
                )

            mode_tok = self._advance()
            self._expect("KEYWORD", value_casefold="matches")
            self._expect("LBRACE")

            patterns: list[CadlArchetypeSlotPattern] = []
            while self._peek().kind != "RBRACE":
                tok = self._peek()
                if tok.kind in {"STRING", "IDENT"}:
                    value_tok = self._advance()
                    patterns.append(
                        CadlArchetypeSlotPattern(
                            kind="exact",
                            value=value_tok.value,
                            span=self._span_from(value_tok, value_tok),
                        )
                    )
                elif tok.kind == "REGEX":
                    value_tok = self._advance()
                    patterns.append(
                        CadlArchetypeSlotPattern(
                            kind="regex",
                            value=value_tok.value,
                            span=self._span_from(value_tok, value_tok),
                        )
                    )
                else:
                    raise _CadlParseError(
                        message=f"Expected pattern in slot matches set, got {tok.kind}",
                        line=tok.start_line,
                        col=tok.start_col,
                    )

                if self._peek().kind == "COMMA":
                    self._advance()
                    continue

            self._expect("RBRACE")

            if mode_tok.value.casefold() == "include":
                includes.extend(patterns)
            else:
                excludes.extend(patterns)

        rbrace = self._expect("RBRACE")
        span = self._span_from(slot_tok, rbrace)
        return CadlArchetypeSlot(
            includes=tuple(includes),
            excludes=tuple(excludes),
            span=span,
        )

    def _parse_attribute(self) -> CadlAttributeNode:
        name_tok = self._expect("IDENT")
        name_span = self._span_from(name_tok, name_tok)
        self._expect("KEYWORD", value_casefold="matches")
        lbrace = self._expect("LBRACE")

        cardinality: CadlCardinality | None = None
        children: list[CadlObjectNode] = []

        while self._peek().kind != "RBRACE":
            if self._peek().kind == "EOF":
                raise _CadlParseError(
                    message="Unterminated attribute matches block",
                    line=lbrace.start_line,
                    col=lbrace.start_col,
                )

            if (
                self._peek().kind == "KEYWORD"
                and self._peek().value.casefold() == "cardinality"
            ):
                cardinality = self._parse_cardinality()
                continue

            if self._peek().kind == "IDENT":
                children.append(self.parse_object())
                continue

            tok = self._peek()
            raise _CadlParseError(
                message=f"Unexpected token in attribute body: {tok.kind} {tok.value!r}",
                line=tok.start_line,
                col=tok.start_col,
            )

        rbrace = self._expect("RBRACE")
        span = self._span_from(name_tok, rbrace)
        return CadlAttributeNode(
            rm_attribute_name=name_tok.value,
            children=tuple(children),
            cardinality=cardinality,
            span=span,
            rm_attribute_name_span=name_span,
        )

    def _parse_occurrences(self) -> CadlOccurrences:
        occ_tok = self._expect("KEYWORD", value_casefold="occurrences")
        self._expect("KEYWORD", value_casefold="matches")
        self._expect("LBRACE")
        interval, rbrace = self._parse_int_interval_with_rbrace()
        span = self._span_from(occ_tok, rbrace)
        return CadlOccurrences(
            lower=interval.lower,
            upper=interval.upper,
            upper_unbounded=interval.upper_unbounded,
            span=span,
        )

    def _parse_cardinality(self) -> CadlCardinality:
        card_tok = self._expect("KEYWORD", value_casefold="cardinality")
        self._expect("KEYWORD", value_casefold="matches")
        self._expect("LBRACE")

        interval, end_tok = self._parse_int_interval_and_end_token()

        is_ordered: bool | None = None
        is_unique: bool | None = None

        # Optional '; ordered' / '; unique' flags.
        while end_tok.kind != "RBRACE":
            if end_tok.kind != "SEMI":
                raise _CadlParseError(
                    message="Expected ';' or '}' after cardinality interval",
                    line=end_tok.start_line,
                    col=end_tok.start_col,
                )
            self._expect("SEMI")
            flag = self._expect("KEYWORD")
            if flag.value.casefold() == "ordered":
                is_ordered = True
            elif flag.value.casefold() == "unique":
                is_unique = True
            else:
                raise _CadlParseError(
                    message=f"Unknown cardinality flag: {flag.value!r}",
                    line=flag.start_line,
                    col=flag.start_col,
                )
            end_tok = self._peek()

        rbrace = self._expect("RBRACE")
        span = self._span_from(card_tok, rbrace)
        return CadlCardinality(
            lower=interval.lower,
            upper=interval.upper,
            upper_unbounded=interval.upper_unbounded,
            is_ordered=is_ordered,
            is_unique=is_unique,
            span=span,
        )

    def _parse_int_interval_and_end_token(self) -> tuple[CadlIntegerInterval, _Token]:
        lower: int | None
        upper: int | None
        upper_unbounded = False

        lower_tok = self._expect("NUMBER")
        lower = int(lower_tok.value)
        self._expect("DOTDOT")

        if self._peek().kind == "STAR":
            self._advance()
            upper = None
            upper_unbounded = True
        else:
            upper_tok = self._expect("NUMBER")
            upper = int(upper_tok.value)

        interval = CadlIntegerInterval(
            lower=lower, upper=upper, upper_unbounded=upper_unbounded
        )
        return interval, self._peek()

    def _parse_int_interval_with_rbrace(self) -> tuple[CadlIntegerInterval, _Token]:
        interval, _end_tok = self._parse_int_interval_and_end_token()
        rbrace = self._expect("RBRACE")
        return interval, rbrace

    def _looks_like_primitive_block(self) -> bool:
        # Primitive blocks start with a literal (STRING/NUMBER/true/false), '*', or a number interval.
        tok = self._peek()
        if tok.kind in {"STRING", "NUMBER", "STAR", "REGEX"}:
            return True
        if tok.kind == "KEYWORD" and tok.value.casefold() in {"true", "false"}:
            return True
        return False

    def _parse_primitive_constraint_block(self) -> CadlPrimitiveConstraint:
        # Parse until the closing '}' of the matches block (but do not consume it).
        # Supported minimal forms:
        # - interval: NUMBER .. NUMBER|*
        # - set: STRING/NUMBER/true/false (',' ...)*
        start = self._peek()

        if start.kind == "NUMBER":
            # Support mixed forms: interval and/or enumerated numbers.
            number_values: list[str] = []
            interval_lower: str | None = None
            interval_upper: str | None = None
            interval_upper_unbounded = False

            while True:
                if (
                    self._peek().kind == "NUMBER"
                    and self._tokens[self._i + 1].kind == "DOTDOT"
                ):
                    if interval_lower is not None:
                        tok = self._peek()
                        raise _CadlParseError(
                            message="Multiple intervals in one primitive constraint are not supported",
                            line=tok.start_line,
                            col=tok.start_col,
                        )

                    lower_tok = self._expect("NUMBER")
                    interval_lower = lower_tok.value
                    self._expect("DOTDOT")
                    if self._peek().kind == "STAR":
                        self._advance()
                        interval_upper = None
                        interval_upper_unbounded = True
                    else:
                        upper_tok = self._expect("NUMBER")
                        interval_upper = upper_tok.value
                        interval_upper_unbounded = False
                else:
                    tok = self._expect("NUMBER")
                    number_values.append(tok.value)

                if self._peek().kind != "COMMA":
                    break
                self._advance()

            is_real = any("." in v for v in number_values) or (
                interval_lower is not None
                and (
                    "." in interval_lower
                    or (interval_upper is not None and "." in interval_upper)
                )
            )

            if is_real:
                interval = None
                if interval_lower is not None:
                    interval = CadlRealInterval(
                        lower=float(interval_lower),
                        upper=(
                            float(interval_upper)
                            if interval_upper is not None
                            else None
                        ),
                        upper_unbounded=interval_upper_unbounded,
                    )
                values = (
                    tuple(float(v) for v in number_values) if number_values else None
                )
                return CadlRealConstraint(values=values, interval=interval)

            interval = None
            if interval_lower is not None:
                interval = CadlIntegerInterval(
                    lower=int(interval_lower),
                    upper=(int(interval_upper) if interval_upper is not None else None),
                    upper_unbounded=interval_upper_unbounded,
                )
            values = tuple(int(v) for v in number_values) if number_values else None
            return CadlIntegerConstraint(values=values, interval=interval)

        if start.kind in {"STRING", "REGEX"}:
            string_values: list[str] = []
            pattern: str | None = None

            while True:
                if self._peek().kind == "STRING":
                    tok = self._expect("STRING")
                    string_values.append(tok.value)
                elif self._peek().kind == "REGEX":
                    tok = self._expect("REGEX")
                    if pattern is not None:
                        raise _CadlParseError(
                            message="Multiple regex patterns in one string constraint are not supported",
                            line=tok.start_line,
                            col=tok.start_col,
                        )
                    pattern = tok.value
                else:
                    tok = self._peek()
                    raise _CadlParseError(
                        message=f"Expected STRING or REGEX, got {tok.kind}",
                        line=tok.start_line,
                        col=tok.start_col,
                    )

                if self._peek().kind != "COMMA":
                    break
                self._advance()

            values = tuple(string_values) if string_values else None
            return CadlStringConstraint(values=values, pattern=pattern)

        if start.kind == "KEYWORD" and start.value.casefold() in {"true", "false"}:
            bool_values: list[bool] = []
            while True:
                tok = self._expect("KEYWORD")
                val = tok.value.casefold()
                if val == "true":
                    bool_values.append(True)
                elif val == "false":
                    bool_values.append(False)
                else:
                    raise _CadlParseError(
                        message=f"Expected boolean literal, got {tok.value!r}",
                        line=tok.start_line,
                        col=tok.start_col,
                    )
                if self._peek().kind != "COMMA":
                    break
                self._advance()
            return CadlBooleanConstraint(values=tuple(bool_values))

        raise _CadlParseError(
            message="Unsupported primitive constraint",
            line=start.start_line,
            col=start.start_col,
        )


_SECTION_NAMES = {
    "specialise",
    "specialize",
    "language",
    "description",
    "terminology",
    "definition",
    "rules",
}


def _parse_kind(
    lines: list[str], *, filename: str | None
) -> tuple[ArtefactKind, SourceSpan | None, int]:
    # Find the first non-empty, non-comment line and classify based on its first word.
    for idx, raw in enumerate(lines):
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("--"):
            continue

        word = stripped.split(maxsplit=1)[0].casefold()
        kind = {
            "archetype": ArtefactKind.ARCHETYPE,
            "template": ArtefactKind.TEMPLATE,
            "template_overlay": ArtefactKind.TEMPLATE_OVERLAY,
            "operational_template": ArtefactKind.OPERATIONAL_TEMPLATE,
        }.get(word, ArtefactKind.UNKNOWN)

        span = SourceSpan(
            file=filename,
            start_line=idx + 1,
            start_col=1,
            end_line=idx + 1,
            end_col=len(line) if line else 1,
        )
        return kind, span, idx

    return ArtefactKind.UNKNOWN, None, 0


def _parse_artefact_id(
    lines: list[str], *, start_index: int, filename: str | None
) -> tuple[str | None, SourceSpan | None]:
    # ADL2 places the artefact id on the first standalone line after the kind line.
    for idx in range(start_index, len(lines)):
        line = lines[idx].rstrip("\n")
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("--"):
            continue
        if stripped.casefold() in _SECTION_NAMES:
            return None, None

        span = SourceSpan(
            file=filename,
            start_line=idx + 1,
            start_col=1,
            end_line=idx + 1,
            end_col=len(line) if line else 1,
        )
        return stripped, span

    return None, None


def _find_sections(lines: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for idx, raw in enumerate(lines):
        name = raw.rstrip("\n").strip().casefold()
        if name in _SECTION_NAMES:
            out[name] = idx
    return out


def _section_content_range(
    lines: list[str], section_map: dict[str, int], name: str
) -> tuple[int, int] | None:
    start_idx = section_map.get(name)
    if start_idx is None:
        return None

    # Content begins after the section header line.
    content_start = start_idx + 1

    # Find the next section header line after this one.
    next_idx = len(lines)
    for _other_name, other_idx in section_map.items():
        if other_idx > start_idx and other_idx < next_idx:
            next_idx = other_idx

    return content_start, next_idx


def _parse_odin_section(
    lines: list[str],
    section_map: dict[str, int],
    *,
    name: str,
    filename: str | None,
) -> tuple[OdinNode | None, SourceSpan | None, list[Issue]]:
    rng = _section_content_range(lines, section_map, name)
    if rng is None:
        return None, None, []

    start_idx, end_idx = rng
    chunk = "".join(lines[start_idx:end_idx])

    # If there is no content, emit a structural error and carry on.
    if not chunk.strip():
        header_line = section_map[name] + 1
        issue = Issue(
            code="ADL010",
            severity=Severity.ERROR,
            message=f"Empty section content: {name}",
            file=filename,
            line=header_line,
            col=1,
        )
        return None, None, [issue]

    # Compute line offset for shifting ODIN issues/spans.
    section_start_line = start_idx + 1

    node, odin_issues = parse_odin(chunk, filename=filename)
    shifted_issues = [
        _shift_issue(i, line_delta=section_start_line - 1) for i in odin_issues
    ]

    if node is None:
        return None, None, shifted_issues

    shifted_node = _shift_odin_node(node, line_delta=section_start_line - 1)

    # Section span: cover the content range.
    span = _span_for_range(
        lines,
        start_line=section_start_line,
        end_line=end_idx,
        filename=filename,
    )

    return shifted_node, span, shifted_issues


def _placeholder_section(
    lines: list[str],
    section_map: dict[str, int],
    name: Literal["definition", "rules"],
    filename: str | None,
) -> AdlSectionPlaceholder | None:
    idx = section_map.get(name)
    if idx is None:
        return None

    line = lines[idx].rstrip("\n")
    span = SourceSpan(
        file=filename,
        start_line=idx + 1,
        start_col=1,
        end_line=idx + 1,
        end_col=len(line) if line else 1,
    )
    return AdlSectionPlaceholder(name=name, span=span)


def _parse_rules_section(
    lines: list[str],
    section_map: dict[str, int],
    *,
    filename: str | None,
) -> AdlRulesSection | None:
    idx = section_map.get("rules")
    if idx is None:
        return None

    header_line = lines[idx].rstrip("\n")
    header_span = SourceSpan(
        file=filename,
        start_line=idx + 1,
        start_col=1,
        end_line=idx + 1,
        end_col=len(header_line) if header_line else 1,
    )

    rng = _section_content_range(lines, section_map, "rules")
    if rng is None:
        return AdlRulesSection(raw_text="", statements=(), header_span=header_span)

    start_idx, end_idx = rng
    chunk_lines = lines[start_idx:end_idx]
    raw_text = "".join(chunk_lines)

    # Build best-effort statement spans.
    # We do not attempt to parse rule syntax; we only capture meaningful lines.
    statements: list[AdlRuleStatement] = []
    for offset, raw in enumerate(chunk_lines):
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("--"):
            continue

        line_no = start_idx + offset + 1
        line_text = raw.rstrip("\n")
        span = SourceSpan(
            file=filename,
            start_line=line_no,
            start_col=1,
            end_line=line_no,
            end_col=len(line_text) if line_text else 1,
        )
        statements.append(AdlRuleStatement(text=stripped, span=span))

    section_start_line = start_idx + 1
    span = _span_for_range(
        lines,
        start_line=section_start_line,
        end_line=end_idx,
        filename=filename,
    )

    return AdlRulesSection(
        raw_text=raw_text,
        statements=tuple(statements),
        header_span=header_span,
        span=span,
    )


def _extract_language_fields(
    language_node: OdinNode | None,
) -> tuple[str | None, str | None]:
    if not isinstance(language_node, OdinObject):
        return None, None

    original_language: str | None = None
    language: str | None = None

    for item in language_node.items:
        if item.key == "original_language":
            original_language = _as_string(item.value)
        elif item.key == "language":
            language = _as_string(item.value)

    return original_language, language


def _as_string(node: OdinNode) -> str | None:
    # Best-effort: only accept a plain OdinString.
    if isinstance(node, OdinString):
        return node.value
    return None


def _shift_issue(issue: Issue, *, line_delta: int) -> Issue:
    line = issue.line + line_delta if issue.line is not None else None
    end_line = issue.end_line + line_delta if issue.end_line is not None else None
    return replace(issue, line=line, end_line=end_line)


def _shift_span(span: SourceSpan | None, *, line_delta: int) -> SourceSpan | None:
    if span is None:
        return None
    return SourceSpan(
        file=span.file,
        start_line=span.start_line + line_delta,
        start_col=span.start_col,
        end_line=span.end_line + line_delta,
        end_col=span.end_col,
    )


def _shift_odin_node(node: OdinNode, *, line_delta: int) -> OdinNode:
    match node:
        case OdinString(value=value, span=span):
            return OdinString(
                value=value, span=_shift_span(span, line_delta=line_delta)
            )
        case OdinInteger(value=value, span=span):
            return OdinInteger(
                value=value, span=_shift_span(span, line_delta=line_delta)
            )
        case OdinReal(value=value, span=span):
            return OdinReal(value=value, span=_shift_span(span, line_delta=line_delta))
        case OdinBoolean(value=value, span=span):
            return OdinBoolean(
                value=value, span=_shift_span(span, line_delta=line_delta)
            )
        case OdinNull(span=span):
            return OdinNull(span=_shift_span(span, line_delta=line_delta))
        case OdinList(items=items, span=span):
            return OdinList(
                items=tuple(_shift_odin_node(i, line_delta=line_delta) for i in items),
                span=_shift_span(span, line_delta=line_delta),
            )
        case OdinObject(items=items, span=span):
            return OdinObject(
                items=tuple(
                    _shift_odin_object_item(i, line_delta=line_delta) for i in items
                ),
                span=_shift_span(span, line_delta=line_delta),
            )
        case OdinKeyedList(items=items, span=span):
            return OdinKeyedList(
                items=tuple(
                    _shift_odin_keyed_list_item(i, line_delta=line_delta) for i in items
                ),
                span=_shift_span(span, line_delta=line_delta),
            )
        case _:
            # Defensive fallback: keep node unchanged.
            return node


def _shift_odin_object_item(item: OdinObjectItem, *, line_delta: int) -> OdinObjectItem:
    return OdinObjectItem(
        key=item.key,
        value=_shift_odin_node(item.value, line_delta=line_delta),
        key_span=_shift_span(item.key_span, line_delta=line_delta),
        span=_shift_span(item.span, line_delta=line_delta),
    )


def _shift_odin_keyed_list_item(
    item: OdinKeyedListItem, *, line_delta: int
) -> OdinKeyedListItem:
    key = item.key
    shifted_key: OdinPrimitive
    if isinstance(key, OdinString):
        shifted_key = OdinString(
            value=key.value, span=_shift_span(key.span, line_delta=line_delta)
        )
    elif isinstance(key, OdinInteger):
        shifted_key = OdinInteger(
            value=key.value, span=_shift_span(key.span, line_delta=line_delta)
        )
    elif isinstance(key, OdinReal):
        shifted_key = OdinReal(
            value=key.value, span=_shift_span(key.span, line_delta=line_delta)
        )
    elif isinstance(key, OdinBoolean):
        shifted_key = OdinBoolean(
            value=key.value, span=_shift_span(key.span, line_delta=line_delta)
        )
    else:
        shifted_key = OdinNull(span=_shift_span(key.span, line_delta=line_delta))

    return OdinKeyedListItem(
        key=shifted_key,
        value=_shift_odin_node(item.value, line_delta=line_delta),
        span=_shift_span(item.span, line_delta=line_delta),
    )


def _root_span(lines: list[str], *, filename: str | None) -> SourceSpan:
    start_line = 1
    start_col = 1

    # Determine end position.
    last = lines[-1].rstrip("\n")
    end_line = len(lines)
    end_col = len(last) if last else 1

    return SourceSpan(
        file=filename,
        start_line=start_line,
        start_col=start_col,
        end_line=end_line,
        end_col=end_col,
    )


def _span_for_range(
    lines: list[str], *, start_line: int, end_line: int, filename: str | None
) -> SourceSpan | None:
    if start_line < 1:
        return None
    if end_line < start_line:
        return None

    # Clamp to file.
    end_line = min(end_line, len(lines))

    end_idx = end_line - 1

    last = lines[end_idx].rstrip("\n") if end_idx < len(lines) else ""

    return SourceSpan(
        file=filename,
        start_line=start_line,
        start_col=1,
        end_line=end_line,
        end_col=len(last) if last else 1,
    )
