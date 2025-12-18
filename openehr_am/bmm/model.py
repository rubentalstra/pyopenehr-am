from dataclasses import dataclass, field
from typing import Self


@dataclass(slots=True, frozen=True)
class Multiplicity:
    """A basic multiplicity (cardinality) constraint.

    `upper=None` represents an unbounded upper limit.

    This is a domain object; invalid values are programmer errors and therefore
    raise `ValueError`.
    """

    lower: int
    upper: int | None

    def __post_init__(self) -> None:
        if self.lower < 0:
            msg = "Multiplicity.lower must be >= 0"
            raise ValueError(msg)
        if self.upper is not None:
            if self.upper < 0:
                msg = "Multiplicity.upper must be >= 0"
                raise ValueError(msg)
            if self.upper < self.lower:
                msg = "Multiplicity.upper must be >= Multiplicity.lower"
                raise ValueError(msg)

    @property
    def is_unbounded(self) -> bool:
        return self.upper is None

    def allows(self, count: int) -> bool:
        if count < 0:
            return False
        if count < self.lower:
            return False
        if self.upper is None:
            return True
        return count <= self.upper

    @classmethod
    def exactly(cls, n: int) -> Self:
        return cls(lower=n, upper=n)

    @classmethod
    def optional(cls) -> Self:
        return cls(lower=0, upper=1)

    @classmethod
    def one(cls) -> Self:
        return cls(lower=1, upper=1)

    @classmethod
    def many(cls) -> Self:
        return cls(lower=0, upper=None)


@dataclass(slots=True, frozen=True)
class TypeRef:
    """A reference to a type in the RM schema.

    Supports generic type parameters like `LIST[DV_TEXT]`.
    """

    name: str
    parameters: tuple[Self, ...] = ()
    nullable: bool = False

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("TypeRef.name must be non-empty")

    @property
    def is_generic(self) -> bool:
        return bool(self.parameters)

    def render(self) -> str:
        base = self.name
        if self.parameters:
            base = f"{base}[{', '.join(p.render() for p in self.parameters)}]"
        if self.nullable:
            return f"{base}?"
        return base


@dataclass(slots=True, frozen=True)
class Property:
    """A property/attribute on a BMM class."""

    name: str
    type_ref: TypeRef
    multiplicity: Multiplicity = field(default_factory=Multiplicity.one)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Property.name must be non-empty")

    @property
    def is_multiple(self) -> bool:
        return self.multiplicity.upper is None or self.multiplicity.upper > 1


@dataclass(slots=True)
class Class:
    """A BMM class definition."""

    name: str
    properties: dict[str, Property] = field(default_factory=dict)
    parent: str | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Class.name must be non-empty")

    def get_property(self, name: str) -> Property | None:
        return self.properties.get(name)

    def add_property(self, prop: Property) -> None:
        self.properties[prop.name] = prop


@dataclass(slots=True)
class Package:
    """A package (namespace) containing subpackages and classes."""

    name: str
    packages: dict[str, Self] = field(default_factory=dict)
    classes: dict[str, Class] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Package.name must be non-empty")

    def add_package(self, pkg: Self) -> None:
        self.packages[pkg.name] = pkg

    def add_class(self, cls: Class) -> None:
        self.classes[cls.name] = cls

    def iter_classes(self) -> list[Class]:
        out: list[Class] = []
        out.extend(self.classes.values())
        for pkg_name in sorted(self.packages):
            out.extend(self.packages[pkg_name].iter_classes())
        return out


@dataclass(slots=True)
class Model:
    """A BMM model, consisting of a hierarchy of packages."""

    name: str
    packages: dict[str, Package] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Model.name must be non-empty")

    def add_package(self, pkg: Package) -> None:
        self.packages[pkg.name] = pkg

    def iter_classes(self) -> list[Class]:
        out: list[Class] = []
        for pkg_name in sorted(self.packages):
            out.extend(self.packages[pkg_name].iter_classes())
        return out

    def find_class(self, name: str) -> Class | None:
        matches = [cls for cls in self.iter_classes() if cls.name == name]
        if not matches:
            return None
        if len(matches) > 1:
            raise ValueError(f"Ambiguous class name: {name!r}")
        return matches[0]
