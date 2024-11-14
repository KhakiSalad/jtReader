import struct
from dataclasses import dataclass

from lsg.elementHeader import ElementHeader
from lsg.types import GUID, JtVersion
from properties.basePropertyAtomData import BasePropertyAtomData
from properties.lsgProperty import LSGProperty


@dataclass
class DummyPropertyAtom(LSGProperty):
    TYPE_ID = GUID((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,))

    element_header: ElementHeader
    base_property_atom_data: BasePropertyAtomData
    version_number: int
    value: int

    @property
    def val(self):
        return self.value

    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        return DummyPropertyAtom(header, None, -1, -1)
