"""Dependency extraction and cycle detection for OPT compilation.

Current supported dependencies (MVP):
    - Archetype specialisation parent (`specialise`/`specialize` section)

Future dependencies will include archetype slot filling and template includes.

Determinism:
    - Nodes are ordered lexicographically by id.
    - Dependency lists are ordered lexicographically.

# Spec: https://specifications.openehr.org/releases/AM/latest/OPT2.html
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from openehr_am.antlr.span import SourceSpan
from openehr_am.aom.archetype import Archetype
from openehr_am.validation.issue import Issue, Severity


@dataclass(slots=True, frozen=True)
class DependencyGraph:
    """A deterministic directed dependency graph.

    Convention:
        `edges[a]` contains the ids that `a` depends on.
    """

    nodes: tuple[str, ...]
    edges: dict[str, tuple[str, ...]]

    def to_dict(self) -> dict[str, object]:
        return {
            "nodes": list(self.nodes),
            "edges": {k: list(self.edges[k]) for k in self.nodes},
        }


def build_archetype_dependency_graph(
    archetypes: Iterable[Archetype],
) -> tuple[DependencyGraph, dict[str, SourceSpan | None]]:
    """Build a dependency graph for a set of AOM Archetypes."""

    by_id: dict[str, Archetype] = {}
    for a in archetypes:
        # If duplicates exist at this stage, keep first deterministically.
        if a.archetype_id not in by_id:
            by_id[a.archetype_id] = a

    nodes = tuple(sorted(by_id.keys()))
    spans = {k: by_id[k].span for k in nodes}

    edges: dict[str, tuple[str, ...]] = {}
    for k in nodes:
        deps: list[str] = []
        parent = by_id[k].parent_archetype_id
        if parent:
            deps.append(parent)
        edges[k] = tuple(sorted(set(deps)))

    return DependencyGraph(nodes=nodes, edges=edges), spans


def detect_dependency_cycles(
    graph: DependencyGraph,
    *,
    spans_by_node: Mapping[str, SourceSpan | None] | None = None,
) -> list[Issue]:
    """Detect dependency cycles and emit OPT705 issues."""

    spans_by_node = spans_by_node or {}
    node_set = set(graph.nodes)

    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []
    index_in_stack: dict[str, int] = {}

    seen_cycles: set[tuple[str, ...]] = set()
    out: list[Issue] = []

    def _canonical_cycle(cycle_nodes: list[str]) -> tuple[str, ...]:
        if not cycle_nodes:
            return ()
        rotations = [
            tuple(cycle_nodes[i:] + cycle_nodes[:i]) for i in range(len(cycle_nodes))
        ]
        return min(rotations)

    def _emit_cycle(cycle: list[str]) -> None:
        canonical = _canonical_cycle(cycle)
        if not canonical or canonical in seen_cycles:
            return
        seen_cycles.add(canonical)

        rendered = " -> ".join([*canonical, canonical[0]])
        span = spans_by_node.get(canonical[0])
        out.append(
            Issue(
                code="OPT705",
                severity=Severity.ERROR,
                message=f"Dependency cycle detected: {rendered}",
                file=span.file if span else None,
                line=span.start_line if span else None,
                col=span.start_col if span else None,
                end_line=span.end_line if span else None,
                end_col=span.end_col if span else None,
            )
        )

    def _dfs(n: str) -> None:
        visiting.add(n)
        index_in_stack[n] = len(stack)
        stack.append(n)

        for dep in graph.edges.get(n, ()):
            if dep not in node_set:
                continue
            if dep in visiting:
                start = index_in_stack[dep]
                _emit_cycle(stack[start:])
                continue
            if dep in visited:
                continue
            _dfs(dep)

        stack.pop()
        index_in_stack.pop(n, None)
        visiting.remove(n)
        visited.add(n)

    for n in graph.nodes:
        if n in visited:
            continue
        _dfs(n)

    return out


def dependency_order_for_archetypes(
    archetypes: Iterable[Archetype],
) -> tuple[tuple[str, ...], list[Issue]]:
    """Return a deterministic dependency order for archetype compilation.

    If cycles are present, returns an empty order and OPT705 Issues.
    """

    graph, spans = build_archetype_dependency_graph(archetypes)
    cycle_issues = detect_dependency_cycles(graph, spans_by_node=spans)
    if cycle_issues:
        return (), cycle_issues

    dependents: dict[str, list[str]] = {n: [] for n in graph.nodes}
    indegree: dict[str, int] = {n: 0 for n in graph.nodes}

    node_set = set(graph.nodes)
    for n in graph.nodes:
        deps = [d for d in graph.edges.get(n, ()) if d in node_set]
        indegree[n] = len(deps)
        for d in deps:
            dependents[d].append(n)

    ready = [n for n in graph.nodes if indegree[n] == 0]
    ready.sort()
    order: list[str] = []

    while ready:
        n = ready.pop(0)
        order.append(n)

        for child in sorted(dependents[n]):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
        ready.sort()

    if len(order) != len(graph.nodes):
        return (), [
            Issue(
                code="OPT705",
                severity=Severity.ERROR,
                message="Dependency cycle detected (incomplete topological order)",
            )
        ]

    return tuple(order), []


__all__ = [
    "DependencyGraph",
    "build_archetype_dependency_graph",
    "detect_dependency_cycles",
    "dependency_order_for_archetypes",
]
