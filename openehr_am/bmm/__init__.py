"""BMM (Basic Meta-Model) structures.

This package contains lightweight domain objects used when loading openEHR
Reference Model schemas expressed in BMM (typically serialized as ODIN).

The loader/repository logic is intentionally separate from validation rules.
"""

from openehr_am.bmm.loader import load_bmm
from openehr_am.bmm.model import Class, Model, Multiplicity, Package, Property, TypeRef
from openehr_am.bmm.repository import ModelRepository

__all__ = [
    "Class",
    "Model",
    "ModelRepository",
    "Multiplicity",
    "Package",
    "Property",
    "TypeRef",
    "load_bmm",
]
