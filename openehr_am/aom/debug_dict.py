"""Deterministic debug serialization for AOM objects.

This module provides helpers to convert AOM dataclasses into JSON-serialisable
Python objects.

It is intended for debugging, tests, and CLI `--json` style output.
"""

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any


def aom_to_dict(value: Any) -> Any:
    """Convert an AOM object (or nested structure) into JSON-serialisable values.

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
        return [aom_to_dict(v) for v in value]

    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for k in sorted(value.keys(), key=str):
            out[str(k)] = aom_to_dict(value[k])
        return out

    if is_dataclass(value):
        out2: dict[str, Any] = {}
        for f in fields(value):
            out2[f.name] = aom_to_dict(getattr(value, f.name))
        return out2

    return repr(value)


__all__ = ["aom_to_dict"]
