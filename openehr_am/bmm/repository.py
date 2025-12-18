"""BMM model repository.

This is the primary entrypoint for working with a set of loaded BMM models.
It provides deterministic lookup helpers and basic type-reference resolution.

# Spec: https://specifications.openehr.org/releases/BASE/latest/bmm.html
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

from openehr_am.bmm.loader import load_bmm
from openehr_am.bmm.model import Class, Model, Property, TypeRef
from openehr_am.validation.issue import Issue, Severity


def _is_known_primitive_or_container(type_name: str) -> bool:
    # Minimal set used by our subset tests/fixtures.
    return type_name in {
        "String",
        "Integer",
        "Real",
        "Boolean",
        "LIST",
        "SET",
        "BAG",
        "HASH",
        "HASH_TABLE",
    }


@dataclass(slots=True, frozen=True)
class ModelRepository:
    """A deterministic repository of loaded RM/BMM models."""

    models: tuple[Model, ...]
    _class_index: dict[str, Class]
    _class_source: dict[str, str]

    @classmethod
    def load_from_dir(cls, directory: str | Path) -> tuple[Self, list[Issue]]:
        """Load all `.bmm` files in `dir`.

        Returns:
            `(repo, issues)`.

        Notes:
            - This method never raises for malformed `.bmm` contents.
            - Duplicate class names are kept deterministically (first file wins)
              and an ERROR Issue is emitted.
        """

        root = Path(directory)
        if not root.exists() or not root.is_dir():
            raise NotADirectoryError(str(root))

        issues: list[Issue] = []
        models: list[Model] = []
        class_index: dict[str, Class] = {}
        class_source: dict[str, str] = {}

        for p in sorted(root.rglob("*.bmm")):
            model, load_issues = load_bmm(p)
            issues.extend(load_issues)
            if model is None:
                continue

            models.append(model)

            for cls_obj in model.iter_classes():
                existing = class_index.get(cls_obj.name)
                if existing is not None:
                    issues.append(
                        Issue(
                            code="BMM550",
                            severity=Severity.ERROR,
                            message=(
                                f"Duplicate class name {cls_obj.name!r} across BMM files; "
                                f"keeping first definition from {class_source[cls_obj.name]!r}"
                            ),
                            file=str(p),
                        )
                    )
                    continue

                class_index[cls_obj.name] = cls_obj
                class_source[cls_obj.name] = str(p)

        repo = cls(
            models=tuple(models), _class_index=class_index, _class_source=class_source
        )

        # After indexing, check that type references resolve.
        issues.extend(repo._check_all_type_refs())

        return repo, issues

    def get_class(self, name: str) -> Class | None:
        return self._class_index.get(name)

    def get_property(self, class_name: str, property_name: str) -> Property | None:
        cls_obj = self.get_class(class_name)
        if cls_obj is None:
            return None
        return cls_obj.get_property(property_name)

    def get_property_inherited(
        self, class_name: str, property_name: str
    ) -> Property | None:
        """Return property from class or its ancestors.

        This follows the `parent` chain on `Class` objects.

        Notes:
            - If an inheritance cycle is detected, traversal stops.
            - The first matching property found in the chain is returned.
        """

        seen: set[str] = set()
        current: str | None = class_name

        while current is not None and current not in seen:
            seen.add(current)

            cls_obj = self.get_class(current)
            if cls_obj is None:
                return None

            prop = cls_obj.get_property(property_name)
            if prop is not None:
                return prop

            current = cls_obj.parent

        return None

    def resolve_type_ref(self, tref: TypeRef) -> Class | None:
        """Resolve a `TypeRef` to a loaded class, if applicable."""

        if _is_known_primitive_or_container(tref.name):
            return None
        return self.get_class(tref.name)

    def _check_all_type_refs(self) -> list[Issue]:
        issues: list[Issue] = []

        for cls_name, cls_obj in self._class_index.items():
            for prop in cls_obj.properties.values():
                issues.extend(self._check_type_ref(cls_name, prop.name, prop.type_ref))

        return issues

    def _check_type_ref(
        self, cls_name: str, prop_name: str, tref: TypeRef
    ) -> list[Issue]:
        out: list[Issue] = []

        # Base name.
        if (
            not _is_known_primitive_or_container(tref.name)
            and tref.name not in self._class_index
        ):
            out.append(
                Issue(
                    code="BMM500",
                    severity=Severity.ERROR,
                    message=(
                        f"Unknown RM type referenced: {tref.name!r} "
                        f"(in {cls_name}.{prop_name})"
                    ),
                    file=self._class_source.get(cls_name),
                )
            )

        # Generic args.
        for p in tref.parameters:
            out.extend(self._check_type_ref(cls_name, prop_name, p))

        return out
