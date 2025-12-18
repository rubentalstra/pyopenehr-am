"""ADL parser (MVP).

Public entrypoint: :func:`parse_adl`.

This is a parsing-layer module: it must never raise for invalid ADL input.
Instead, it returns `Issue` objects.

The MVP parser only extracts:
- artefact kind
- artefact id
- language/original_language (best-effort, from the language ODIN block)
- ODIN blocks for: language, description, terminology

The definition and rules sections are recognised but not parsed yet.

# Spec: https://specifications.openehr.org/releases/AM/latest/ADL2.html
"""

from dataclasses import replace

from openehr_am.adl.ast import AdlArtefact, AdlSectionPlaceholder, ArtefactKind
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

    language_node, language_span, language_issues = _parse_odin_section(
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

    definition_placeholder = _placeholder_section(
        lines, section_map, "definition", filename
    )
    rules_placeholder = _placeholder_section(lines, section_map, "rules", filename)

    root_span = _root_span(lines, filename=filename)

    artefact = AdlArtefact(
        kind=kind,
        artefact_id=artefact_id,
        original_language=original_language,
        language=language,
        description=description_node,
        terminology=terminology_node,
        definition=definition_placeholder,
        rules=rules_placeholder,
        span=root_span,
        kind_span=kind_span,
        artefact_id_span=artefact_id_span,
        original_language_span=None,
        language_span=None,
        description_span=description_span,
        terminology_span=terminology_span,
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


_SECTION_NAMES = {
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
    for other_name, other_idx in section_map.items():
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
    lines: list[str], section_map: dict[str, int], name: str, filename: str | None
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
