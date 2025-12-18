"""Deterministic JSON export for OPT objects.

This module provides a small helper that turns the deterministic `to_dict()`
output of OPT dataclasses into stable JSON strings.
"""

import json
from typing import Any

from openehr_am.opt.debug_dict import opt_to_dict


def opt_to_json(value: Any, *, indent: int | None = None) -> str:
    """Serialize an OPT object (or nested structure) to JSON deterministically.

    Notes:
        - Uses `opt_to_dict()` to obtain a JSON-serialisable structure.
        - Uses stable separators to avoid whitespace differences.
        - Does not sort keys, because the underlying dicts are already emitted
          deterministically by field order / sorted-key rules.
    """

    data = opt_to_dict(value)
    return json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":"),
        indent=indent,
    )


__all__ = ["opt_to_json"]
