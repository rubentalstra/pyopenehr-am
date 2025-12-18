"""Specialisation flattening (minimal subset).

This module contains MVP flattening rules used during OPT compilation.

Current scope:
- Flatten an archetype specialisation chain by merging the child's definition
  over the parent's definition.
- Emit OPT730 on detected structural conflicts.

Design notes:
- This is *not* full AOM2/OPT2 flattening.
- Output is deterministic: merged attributes and children are sorted.

# Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html
# Spec: https://specifications.openehr.org/releases/AM/latest/OPT2.html
"""

from dataclasses import replace

from openehr_am.aom.archetype import Archetype
from openehr_am.aom.constraints import (
    CArchetypeSlot,
    Cardinality,
    CAttribute,
    CComplexObject,
    CObject,
    CPrimitiveObject,
    Interval,
    PrimitiveBooleanConstraint,
    PrimitiveIntegerConstraint,
    PrimitiveRealConstraint,
    PrimitiveStringConstraint,
)
from openehr_am.aom.repository import ArchetypeRepository
from openehr_am.opt.model import (
    OptBooleanConstraint,
    OptCardinality,
    OptCAttribute,
    OptCComplexObject,
    OptCObject,
    OptCPrimitiveObject,
    OptIntegerConstraint,
    OptInterval,
    OptRealConstraint,
    OptStringConstraint,
)
from openehr_am.validation.issue import Issue, Severity


def flatten_specialisation_definition(
    archetype: Archetype,
    repo: ArchetypeRepository,
) -> tuple[CComplexObject | None, list[Issue]]:
    """Flatten an archetype's definition across its specialisation chain."""

    issues: list[Issue] = []

    parent_id = archetype.parent_archetype_id
    if parent_id is None:
        return archetype.definition, []

    parent = repo.get(parent_id)
    if parent is None:
        # Missing parents are handled earlier (OPT700). Fall back to child's.
        return archetype.definition, []

    parent_def, parent_issues = flatten_specialisation_definition(parent, repo)
    issues.extend(parent_issues)
    if any(i.severity is Severity.ERROR for i in issues):
        return None, issues

    if parent_def is None:
        return archetype.definition, issues
    if archetype.definition is None:
        return parent_def, issues

    merged, merge_issues = _merge_objects(
        parent_def,
        archetype.definition,
        path="/",
        parent_archetype_id=parent.archetype_id,
        child_archetype_id=archetype.archetype_id,
    )
    issues.extend(merge_issues)

    if any(i.severity is Severity.ERROR for i in issues):
        return None, issues

    assert isinstance(merged, CComplexObject)
    return merged, issues


def aom_definition_to_opt(
    definition: CComplexObject,
    *,
    root_path: str = "/",
    source_archetype_id: str | None = None,
) -> OptCComplexObject:
    """Convert an AOM definition subtree to OPT flattened nodes.

    Notes:
        This is a structural conversion only. It does not attempt to resolve RM
        paths or enforce OPT-specific rules.
    """

    obj = _aom_object_to_opt(
        definition,
        path=root_path,
        source_archetype_id=source_archetype_id,
    )
    assert isinstance(obj, OptCComplexObject)
    return obj


def _aom_interval_to_opt(value: Interval | None) -> OptInterval | None:
    if value is None:
        return None
    return OptInterval(
        lower=value.lower,
        upper=value.upper,
        lower_included=value.lower_included,
        upper_included=value.upper_included,
        span=value.span,
    )


def _aom_cardinality_to_opt(value: Cardinality | None) -> OptCardinality | None:
    if value is None:
        return None
    occ = _aom_interval_to_opt(value.occurrences)
    assert occ is not None
    return OptCardinality(
        occurrences=occ,
        is_ordered=value.is_ordered,
        is_unique=value.is_unique,
        span=value.span,
    )


def _aom_object_to_opt(
    node: CObject,
    *,
    path: str,
    source_archetype_id: str | None,
) -> OptCObject:
    occurrences = _aom_interval_to_opt(node.occurrences)

    if isinstance(node, CComplexObject):
        attrs: list[OptCAttribute] = []
        for a in sorted(node.attributes, key=lambda x: x.rm_attribute_name):
            attr_path = _join_path(path, a.rm_attribute_name, None)
            children = tuple(
                _aom_object_to_opt(
                    c,
                    path=_join_path(attr_path, None, c.node_id),
                    source_archetype_id=source_archetype_id,
                )
                for c in _sorted_children(a.children)
            )
            attrs.append(
                OptCAttribute(
                    rm_attribute_name=a.rm_attribute_name,
                    children=children,
                    existence=_aom_interval_to_opt(a.existence),
                    cardinality=_aom_cardinality_to_opt(a.cardinality),
                    path=attr_path,
                    span=a.span,
                )
            )

        return OptCComplexObject(
            rm_type_name=node.rm_type_name,
            node_id=node.node_id,
            path=path,
            occurrences=occurrences,
            source_archetype_id=source_archetype_id,
            attributes=tuple(attrs),
            span=node.span,
        )

    if isinstance(node, CPrimitiveObject):
        return OptCPrimitiveObject(
            rm_type_name=node.rm_type_name,
            node_id=node.node_id,
            path=path,
            occurrences=occurrences,
            source_archetype_id=source_archetype_id,
            constraint=_aom_primitive_to_opt(node.constraint),
            span=node.span,
        )

    if isinstance(node, CArchetypeSlot):
        # Slots should be resolved before producing OPT definition.
        return OptCComplexObject(
            rm_type_name=node.rm_type_name,
            node_id=node.node_id,
            path=path,
            occurrences=occurrences,
            source_archetype_id=source_archetype_id,
            attributes=(),
            span=node.span,
        )

    return OptCComplexObject(
        rm_type_name=node.rm_type_name,
        node_id=node.node_id,
        path=path,
        occurrences=occurrences,
        source_archetype_id=source_archetype_id,
        attributes=(),
        span=node.span,
    )


def _aom_primitive_to_opt(
    value: PrimitiveStringConstraint
    | PrimitiveIntegerConstraint
    | PrimitiveRealConstraint
    | PrimitiveBooleanConstraint
    | None,
) -> (
    OptStringConstraint
    | OptIntegerConstraint
    | OptRealConstraint
    | OptBooleanConstraint
    | None
):
    if value is None:
        return None

    if isinstance(value, PrimitiveStringConstraint):
        return OptStringConstraint(
            values=value.values, pattern=value.pattern, span=value.span
        )
    if isinstance(value, PrimitiveIntegerConstraint):
        return OptIntegerConstraint(
            values=value.values,
            interval=_aom_interval_to_opt(value.interval),
            span=value.span,
        )
    if isinstance(value, PrimitiveRealConstraint):
        return OptRealConstraint(
            values=value.values,
            interval=_aom_interval_to_opt(value.interval),
            span=value.span,
        )
    if isinstance(value, PrimitiveBooleanConstraint):
        return OptBooleanConstraint(values=value.values, span=value.span)

    return None


def _merge_objects(
    parent: CObject,
    child: CObject,
    *,
    path: str,
    parent_archetype_id: str,
    child_archetype_id: str,
) -> tuple[CObject, list[Issue]]:
    if parent.rm_type_name != child.rm_type_name:
        return parent, [
            _opt730(
                message=(
                    "Specialisation flattening conflict: RM type mismatch at "
                    f"{path!r}: parent={parent.rm_type_name!r}, child={child.rm_type_name!r}"
                ),
                span=child.span or parent.span,
            )
        ]

    # Merge primitive vs complex vs slot kinds.
    if isinstance(parent, CPrimitiveObject) or isinstance(child, CPrimitiveObject):
        if not (
            isinstance(parent, CPrimitiveObject) and isinstance(child, CPrimitiveObject)
        ):
            return parent, [
                _opt730(
                    message=f"Specialisation flattening conflict: primitive/object mismatch at {path!r}",
                    span=child.span or parent.span,
                )
            ]
        if parent.constraint != child.constraint and child.constraint is not None:
            return parent, [
                _opt730(
                    message=f"Specialisation flattening conflict: primitive constraint differs at {path!r}",
                    span=child.span or parent.span,
                )
            ]
        merged = replace(
            parent,
            occurrences=child.occurrences or parent.occurrences,
            constraint=child.constraint or parent.constraint,
            span=child.span or parent.span,
        )
        return merged, []

    if isinstance(parent, CArchetypeSlot) or isinstance(child, CArchetypeSlot):
        if not (
            isinstance(parent, CArchetypeSlot) and isinstance(child, CArchetypeSlot)
        ):
            return parent, [
                _opt730(
                    message=f"Specialisation flattening conflict: slot/object mismatch at {path!r}",
                    span=child.span or parent.span,
                )
            ]
        if child.includes and child.includes != parent.includes:
            return parent, [
                _opt730(
                    message=f"Specialisation flattening conflict: slot includes differ at {path!r}",
                    span=child.span or parent.span,
                )
            ]
        if child.excludes and child.excludes != parent.excludes:
            return parent, [
                _opt730(
                    message=f"Specialisation flattening conflict: slot excludes differ at {path!r}",
                    span=child.span or parent.span,
                )
            ]
        merged = replace(
            parent,
            occurrences=child.occurrences or parent.occurrences,
            includes=child.includes or parent.includes,
            excludes=child.excludes or parent.excludes,
            span=child.span or parent.span,
        )
        return merged, []

    if not (isinstance(parent, CComplexObject) and isinstance(child, CComplexObject)):
        return parent, [
            _opt730(
                message=f"Specialisation flattening conflict: unsupported object types at {path!r}",
                span=child.span or parent.span,
            )
        ]

    issues: list[Issue] = []

    parent_by_name = {a.rm_attribute_name: a for a in parent.attributes}
    child_by_name = {a.rm_attribute_name: a for a in child.attributes}

    merged_attrs: list[CAttribute] = []
    for name in sorted(set(parent_by_name.keys()) | set(child_by_name.keys())):
        p_attr = parent_by_name.get(name)
        c_attr = child_by_name.get(name)
        attr_path = _join_path(path, name, None)

        if p_attr is None:
            assert c_attr is not None
            merged_attrs.append(c_attr)
            continue
        if c_attr is None:
            merged_attrs.append(p_attr)
            continue

        existence, existence_issues = _merge_interval(
            p_attr.existence, c_attr.existence, path=attr_path
        )
        issues.extend(existence_issues)
        cardinality, cardinality_issues = _merge_cardinality(
            p_attr.cardinality, c_attr.cardinality, path=attr_path
        )
        issues.extend(cardinality_issues)

        merged_children, child_issues = _merge_children(
            p_attr.children,
            c_attr.children,
            path=attr_path,
            parent_archetype_id=parent_archetype_id,
            child_archetype_id=child_archetype_id,
        )
        issues.extend(child_issues)

        merged_attrs.append(
            CAttribute(
                rm_attribute_name=name,
                children=merged_children,
                existence=existence,
                cardinality=cardinality,
                span=c_attr.span or p_attr.span,
            )
        )

    merged = CComplexObject(
        rm_type_name=parent.rm_type_name,
        node_id=child.node_id or parent.node_id,
        occurrences=child.occurrences or parent.occurrences,
        attributes=tuple(merged_attrs),
        span=child.span or parent.span,
    )

    if any(i.severity is Severity.ERROR for i in issues):
        return parent, issues

    return merged, []


def _merge_children(
    parent_children: tuple[CObject, ...],
    child_children: tuple[CObject, ...],
    *,
    path: str,
    parent_archetype_id: str,
    child_archetype_id: str,
) -> tuple[tuple[CObject, ...], list[Issue]]:
    issues: list[Issue] = []

    def key(o: CObject) -> tuple[str, str, str | None]:
        # Prefer node_id matching (stronger identity).
        if o.node_id is not None:
            return ("node_id", o.node_id, None)
        return ("rm_type", o.rm_type_name, o.node_id)

    p_by: dict[tuple[str, str, str | None], CObject] = {}
    for o in parent_children:
        k = key(o)
        existing = p_by.get(k)
        if existing is not None and existing.rm_type_name != o.rm_type_name:
            issues.append(
                _opt730(
                    message=(
                        "Specialisation flattening conflict: duplicate node identity in parent at "
                        f"{path!r}"
                    ),
                    span=o.span or existing.span,
                )
            )
            continue
        p_by[k] = o

    c_by: dict[tuple[str, str, str | None], CObject] = {}
    for o in child_children:
        k = key(o)
        existing = c_by.get(k)
        if existing is not None and existing.rm_type_name != o.rm_type_name:
            issues.append(
                _opt730(
                    message=(
                        "Specialisation flattening conflict: duplicate node identity in child at "
                        f"{path!r}"
                    ),
                    span=o.span or existing.span,
                )
            )
            continue
        c_by[k] = o

    merged: list[CObject] = []
    for k in sorted(set(p_by.keys()) | set(c_by.keys())):
        p = p_by.get(k)
        c = c_by.get(k)
        if p is None:
            assert c is not None
            merged.append(c)
            continue
        if c is None:
            merged.append(p)
            continue

        # If the identity is node_id-based and rm_type differs, treat as conflict.
        if k[0] == "node_id" and p.rm_type_name != c.rm_type_name:
            issues.append(
                _opt730(
                    message=(
                        "Specialisation flattening conflict: node_id reused with different RM type at "
                        f"{path!r}: node_id={p.node_id!r}, parent={p.rm_type_name!r}, child={c.rm_type_name!r}"
                    ),
                    span=c.span or p.span,
                )
            )
            continue

        merged_node, merge_issues = _merge_objects(
            p,
            c,
            path=_join_path(path, None, c.node_id or p.node_id),
            parent_archetype_id=parent_archetype_id,
            child_archetype_id=child_archetype_id,
        )
        issues.extend(merge_issues)
        merged.append(merged_node)

    return tuple(_sorted_children(tuple(merged))), issues


def _merge_interval(
    parent: Interval | None,
    child: Interval | None,
    *,
    path: str,
) -> tuple[Interval | None, list[Issue]]:
    if child is None:
        return parent, []
    if parent is None:
        return child, []
    if child != parent:
        return parent, [
            _opt730(
                message=f"Specialisation flattening conflict: interval differs at {path!r}",
                span=child.span or parent.span,
            )
        ]
    return parent, []


def _merge_cardinality(
    parent: Cardinality | None,
    child: Cardinality | None,
    *,
    path: str,
) -> tuple[Cardinality | None, list[Issue]]:
    if child is None:
        return parent, []
    if parent is None:
        return child, []
    if child != parent:
        return parent, [
            _opt730(
                message=f"Specialisation flattening conflict: cardinality differs at {path!r}",
                span=child.span or parent.span,
            )
        ]
    return parent, []


def _sorted_children(children: tuple[CObject, ...]) -> tuple[CObject, ...]:
    return tuple(sorted(children, key=lambda o: (o.rm_type_name, o.node_id or "")))


def _join_path(base: str, attr: str | None, node_id: str | None) -> str:
    p = base.rstrip("/") or "/"
    if attr:
        if p == "/":
            p = f"/{attr}"
        else:
            p = f"{p}/{attr}"
    if node_id:
        p = f"{p}[{node_id}]"
    return p


def _opt730(*, message: str, span) -> Issue:
    return Issue(
        code="OPT730",
        severity=Severity.ERROR,
        message=message,
        file=span.file if span else None,
        line=span.start_line if span else None,
        col=span.start_col if span else None,
        end_line=span.end_line if span else None,
        end_col=span.end_col if span else None,
    )


__all__ = [
    "aom_definition_to_opt",
    "flatten_specialisation_definition",
]
