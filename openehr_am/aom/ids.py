"""Identifier helpers for AOM objects.

This module provides small, non-throwing helpers for common identifier formats:

- Node ids: `atNNNN` (archetype term codes) and `acNNNN` (archetype constraint codes)
- openEHR archetype ids (minimal parsing)

These helpers intentionally do **not** emit `Issue` objects; validation rules
live in `openehr_am/validation/`.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from openehr_am.aom.debug_dict import aom_to_dict

type NodeIdPrefix = Literal["at", "ac"]


class NodeIdKind(StrEnum):
    TERM = "at"
    CONSTRAINT = "ac"


@dataclass(slots=True, frozen=True)
class NodeId:
    """Parsed node id."""

    prefix: NodeIdPrefix
    number: int

    @property
    def kind(self) -> NodeIdKind:
        return NodeIdKind(self.prefix)

    def __str__(self) -> str:
        return format_node_id(self.prefix, self.number)

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


def is_node_id(value: str) -> bool:
    """Return True if value matches `atNNNN` or `acNNNN` (exactly 4 digits)."""

    parsed = try_parse_node_id(value)
    return parsed is not None


def is_at_code(value: str) -> bool:
    """Return True if value matches `atNNNN` (exactly 4 digits)."""

    parsed = try_parse_node_id(value)
    return parsed is not None and parsed.prefix == "at"


def is_ac_code(value: str) -> bool:
    """Return True if value matches `acNNNN` (exactly 4 digits)."""

    parsed = try_parse_node_id(value)
    return parsed is not None and parsed.prefix == "ac"


def try_parse_node_id(value: str) -> NodeId | None:
    """Parse `atNNNN`/`acNNNN`.

    Returns:
        A `NodeId` on success, or `None` if the format is invalid.
    """

    if len(value) != 6:
        return None

    prefix = value[:2]
    if prefix not in ("at", "ac"):
        return None

    digits = value[2:]
    if not digits.isdigit():
        return None

    return NodeId(prefix=prefix, number=int(digits))


def format_node_id(prefix: NodeIdPrefix, number: int) -> str:
    """Format a node id as `atNNNN`/`acNNNN`.

    Notes:
        - Values outside [0, 9999] are rejected (returns ValueError) because
          this is a programmer-controlled formatting operation.
    """

    if number < 0 or number > 9999:
        raise ValueError(f"node id number out of range: {number}")

    return f"{prefix}{number:04d}"


@dataclass(slots=True, frozen=True)
class ArchetypeId:
    """Minimal parsed representation of an openEHR archetype id.

    Example:
        `openEHR-EHR-OBSERVATION.example.v1`

    Notes:
        - This is intentionally permissive about allowed characters in
          `concept`; detailed validation is handled in validation rules.
    """

    raw: str

    originator: str
    rm_name: str
    rm_entity: str

    concept: str
    version: str

    def to_dict(self) -> dict[str, object]:
        return aom_to_dict(self)


def try_parse_archetype_id(value: str) -> ArchetypeId | None:
    """Parse an openEHR archetype id.

    Expected shape (minimal):
        `<originator>-<rm_name>-<rm_entity>.<concept>.<version>`

    Returns:
        `ArchetypeId` on success, else `None`.
    """

    parts = value.split(".")
    if len(parts) < 3:
        return None

    # openEHR archetype ids typically look like:
    #   <originator>-<rm_name>-<rm_entity>.<concept>.vN(.N...)
    # Therefore, the version may itself contain '.' separators. We locate the
    # last segment that starts with 'v' and treat everything to the right as
    # part of the version token.
    version_start = -1
    for i in range(len(parts) - 1, -1, -1):
        if parts[i].startswith("v"):
            version_start = i
            break

    if version_start < 2:
        return None

    qualified = ".".join(parts[: version_start - 1])
    concept = parts[version_start - 1]
    version = ".".join(parts[version_start:])

    if not qualified or not concept or not version:
        return None

    qparts = qualified.split("-")
    if len(qparts) != 3:
        return None

    originator, rm_name, rm_entity = qparts

    if not originator or not rm_name or not rm_entity:
        return None

    if not _is_version_token(version):
        return None

    return ArchetypeId(
        raw=value,
        originator=originator,
        rm_name=rm_name,
        rm_entity=rm_entity,
        concept=concept,
        version=version,
    )


def is_archetype_id(value: str) -> bool:
    """Return True if value parses as an openEHR archetype id (minimal rules)."""

    return try_parse_archetype_id(value) is not None


def _is_version_token(value: str) -> bool:
    # Accept vN, vN.N, vN.N.N, ... (no regex).
    if len(value) < 2:
        return False
    if value[0] != "v":
        return False

    digits_and_dots = value[1:]
    if digits_and_dots[0] == "." or digits_and_dots[-1] == ".":
        return False

    saw_digit = False
    last_was_dot = False

    for ch in digits_and_dots:
        if ch.isdigit():
            saw_digit = True
            last_was_dot = False
            continue
        if ch == ".":
            if last_was_dot:
                return False
            last_was_dot = True
            continue
        return False

    return saw_digit and not last_was_dot


__all__ = [
    "NodeIdPrefix",
    "NodeIdKind",
    "NodeId",
    "is_node_id",
    "is_at_code",
    "is_ac_code",
    "try_parse_node_id",
    "format_node_id",
    "ArchetypeId",
    "try_parse_archetype_id",
    "is_archetype_id",
]
