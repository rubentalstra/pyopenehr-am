"""Deterministic debug serialization for OPT objects.

This module mirrors the AOM debug-dict helper but is kept separate so OPT
serialization can evolve without affecting AOM.
"""

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any


def opt_to_dict(value: Any) -> Any:
    """Convert an OPT object (or nested structure) into JSON-serialisable values.

    Determinism:
        - Dataclass fields are emitted in definition order.
        - Tuples/lists preserve element order.
        - Dict keys are emitted in sorted key order (by `str(key)`).

    Notes:
        This is a debug helper. It is intentionally permissive and will fall
        back to `repr(value)` for unknown object types.
    """

    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, Enum):
        return value.value

    if isinstance(value, (tuple, list)):
        return [opt_to_dict(v) for v in value]

    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for k in sorted(value.keys(), key=str):
            out[str(k)] = opt_to_dict(value[k])
        return out

    if is_dataclass(value):
        out2: dict[str, Any] = {}
        for f in fields(value):
            out2[f.name] = opt_to_dict(getattr(value, f.name))
        return out2

    return repr(value)


__all__ = ["opt_to_dict"]
