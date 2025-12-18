"""Resolve openEHR paths against an AOM constraint tree (subset).

Public entrypoint: :func:`resolve_path`.

This module is used by validation rules that need to check whether paths
referenced in an archetype/template actually point to nodes in the AOM
constraint model.

Supported subset:
- Segment names resolve via `CAttribute.rm_attribute_name`.
- Optional single predicate `[ ... ]` is treated as a node-id selector and
  matched by exact string equality against `CObject.node_id`.
- A leading `/definition` is ignored (handled by the parser).

On valid syntax but no matching nodes, this emits `PATH910`.

# Spec: https://specifications.openehr.org/releases/BASE/latest/architecture_overview.html#_paths
"""

from collections.abc import Iterable

from openehr_am.aom.constraints import CAttribute, CComplexObject, CObject
from openehr_am.path.ast import Path
from openehr_am.path.parser import parse_path
from openehr_am.validation.issue import Issue, Severity


def resolve_path(
    definition: CComplexObject | None,
    path: str | Path,
    *,
    filename: str | None = None,
) -> tuple[tuple[CObject, ...] | None, list[Issue]]:
    """Resolve `path` against the AOM constraint `definition`.

    Args:
        definition: Root AOM constraint object (typically archetype.definition).
        path: A path string or already-parsed `Path`.
        filename: Optional filename to place into emitted Issues.

    Returns:
        (nodes, issues)

        - On parse failure: nodes is None and issues includes PATH900.
        - On no matches: nodes is an empty tuple and issues includes PATH910.
        - On success: nodes is a non-empty tuple and issues is empty.

    Notes:
        This function never raises for invalid path input.

    # Spec: https://specifications.openehr.org/releases/BASE/latest/architecture_overview.html#_paths
    """

    if isinstance(path, str):
        parsed, issues = parse_path(path, filename=filename)
        if issues:
            return None, issues
        assert parsed is not None
        path_ast = parsed
        raw_text = path
    else:
        path_ast = path
        raw_text = str(path)

    if definition is None:
        return (), [
            Issue(
                code="PATH910",
                severity=Severity.ERROR,
                message="Path resolves to no nodes",
                file=filename,
                path=raw_text,
            )
        ]

    current: tuple[CObject, ...] = (definition,)

    for seg in path_ast.segments:
        next_nodes: list[CObject] = []

        for node in current:
            if not isinstance(node, CComplexObject):
                continue

            attr = _find_attribute(node.attributes, seg.name)
            if attr is None:
                continue

            if seg.predicate is None:
                next_nodes.extend(attr.children)
                continue

            pred_text = seg.predicate.text
            for child in attr.children:
                if child.node_id == pred_text:
                    next_nodes.append(child)

        current = tuple(next_nodes)
        if not current:
            return (), [
                Issue(
                    code="PATH910",
                    severity=Severity.ERROR,
                    message="Path resolves to no nodes",
                    file=filename,
                    path=raw_text,
                )
            ]

    return current, []


def _find_attribute(attrs: Iterable[CAttribute], name: str) -> CAttribute | None:
    for attr in attrs:
        if attr.rm_attribute_name == name:
            return attr
    return None
