"""AOM archetype repository.

This module provides a small, deterministic helper for loading a set of `.adl`
archetype files from a directory, parsing them, and indexing the resulting AOM
`Archetype` objects by archetype id.

Notes:
    - Invalid `.adl` contents never raise; problems are returned as `Issue`s.
    - I/O errors for individual files are reported as `Issue`s and skipped.
    - The scan order is deterministic (sorted `Path.rglob`).

# Spec: https://specifications.openehr.org/releases/AM/latest/ADL2.html
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

from openehr_am.adl.parser import parse_adl
from openehr_am.aom.archetype import Archetype
from openehr_am.aom.builder import build_aom_from_adl
from openehr_am.validation.issue import Issue, Severity


@dataclass(slots=True, frozen=True)
class ArchetypeRepository:
    """A deterministic repository of loaded AOM `Archetype` objects."""

    archetypes: tuple[Archetype, ...]
    _index: dict[str, Archetype]
    _source: dict[str, str]

    @classmethod
    def load_from_dir(cls, directory: str | Path) -> tuple[Self, list[Issue]]:
        """Load all `.adl` files under `directory` and index archetypes by id.

        Returns:
            `(repo, issues)`.

        Notes:
            - Directory scanning is recursive.
            - Duplicate archetype ids are kept deterministically (first file wins)
              and an ERROR `Issue` is emitted.
        """

        root = Path(directory)
        if not root.exists() or not root.is_dir():
            raise NotADirectoryError(str(root))

        issues: list[Issue] = []
        archetypes: list[Archetype] = []
        index: dict[str, Archetype] = {}
        source: dict[str, str] = {}

        for p in sorted(root.rglob("*.adl")):
            try:
                text = p.read_text(encoding="utf-8")
            except OSError as e:
                issues.append(
                    Issue(
                        code="ADL005",
                        severity=Severity.ERROR,
                        message=f"Cannot read input file: {e}",
                        file=str(p),
                    )
                )
                continue

            artefact, parse_issues = parse_adl(text, filename=str(p))
            issues.extend(parse_issues)
            if artefact is None:
                continue

            aom_obj, build_issues = build_aom_from_adl(artefact)
            issues.extend(build_issues)
            if not isinstance(aom_obj, Archetype):
                continue

            archetype_id = aom_obj.archetype_id
            existing = index.get(archetype_id)
            if existing is not None:
                issues.append(
                    Issue(
                        code="AOM242",
                        severity=Severity.ERROR,
                        message=(
                            f"Duplicate archetype id {archetype_id!r} across ADL files; "
                            f"keeping first definition from {source[archetype_id]!r}"
                        ),
                        file=str(p),
                    )
                )
                continue

            index[archetype_id] = aom_obj
            source[archetype_id] = str(p)
            archetypes.append(aom_obj)

        return cls(archetypes=tuple(archetypes), _index=index, _source=source), issues

    def get(self, archetype_id: str) -> Archetype | None:
        return self._index.get(archetype_id)

    def __contains__(self, archetype_id: object) -> bool:
        return isinstance(archetype_id, str) and archetype_id in self._index

    def __len__(self) -> int:
        return len(self.archetypes)

    def ids(self) -> tuple[str, ...]:
        """Return loaded archetype ids in deterministic order."""

        return tuple(a.archetype_id for a in self.archetypes)


__all__ = [
    "ArchetypeRepository",
]
