import struct
from dataclasses import dataclass

from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.lsg.types import GUID, JtVersion
from jt_reader.properties.basePropertyAtomData import BasePropertyAtomData
from jt_reader.properties.lsgProperty import LSGProperty


@dataclass
class DummyPropertyAtom(LSGProperty):
    TYPE_ID = GUID((0,0,0,0,0,0,0,0,0,0,0,))

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
