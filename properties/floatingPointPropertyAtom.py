import struct
from dataclasses import dataclass

from jt_reader.properties.basePropertyAtomData import BasePropertyAtomData
from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.properties.lsgProperty import LSGProperty
from jt_reader.lsg.types import GUID


@dataclass
class FloatingPointPropertyAtom(LSGProperty):
    TYPE_ID = GUID((0x10dd1019, 0x2ac8, 0x11d1, 0x9b, 0x6b, 0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97))
    element_header: ElementHeader
    base_property_atom_data: BasePropertyAtomData
    version_number: int
    value: float

    @property
    def val(self):
        return self.value

    @classmethod
    def from_bytes(cls, e_bytes, header=None):
        base_property_atom_data = BasePropertyAtomData.from_bytes(e_bytes)
        version_number, value = struct.unpack("<hf", e_bytes.read(6))
        return FloatingPointPropertyAtom(header, base_property_atom_data, version_number, value)
