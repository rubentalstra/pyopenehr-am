"""OPT compilation helpers.

This package contains utilities for compiling templates and archetypes into an
Operational Template (OPT2).
"""

from openehr_am.opt.compiler import compile_opt
from openehr_am.opt.dependencies import (
    DependencyGraph,
    build_archetype_dependency_graph,
    dependency_order_for_archetypes,
    detect_dependency_cycles,
)
from openehr_am.opt.json import opt_to_json
from openehr_am.opt.model import (
    OperationalTemplate,
    OptBooleanConstraint,
    OptCardinality,
    OptCAttribute,
    OptCComplexObject,
    OptCObject,
    OptCPrimitiveObject,
    OptIntegerConstraint,
    OptInterval,
    OptPrimitiveConstraint,
    OptRealConstraint,
    OptStringConstraint,
)

__all__ = [
    "DependencyGraph",
    "build_archetype_dependency_graph",
    "detect_dependency_cycles",
    "dependency_order_for_archetypes",
    "OperationalTemplate",
    "OptInterval",
    "OptCardinality",
    "OptStringConstraint",
    "OptIntegerConstraint",
    "OptRealConstraint",
    "OptBooleanConstraint",
    "OptPrimitiveConstraint",
    "OptCObject",
    "OptCAttribute",
    "OptCComplexObject",
    "OptCPrimitiveObject",
    "opt_to_json",
    "compile_opt",
]
