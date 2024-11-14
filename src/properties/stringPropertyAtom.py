import struct
from dataclasses import dataclass

from lsg.elementHeader import ElementHeader
from lsg.types import GUID, JtVersion
from properties.basePropertyAtomData import BasePropertyAtomData
from properties.lsgProperty import LSGProperty


@dataclass
class StringPropertyAtom(LSGProperty):
    TYPE_ID = GUID((0x10dd106e, 0x2ac8, 0x11d1, 0x9b, 0x6b,
                   0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97))

    element_header: ElementHeader
    base_property_atom_data: BasePropertyAtomData
    version_number: int
    value: str

    @property
    def val(self):
        return self.value

    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        base_property_atom_data = BasePropertyAtomData.from_bytes(
            e_bytes, version=version)
        if version == JtVersion.V9d5:
            version_number = struct.unpack("<h", e_bytes.read(2))[0]
        else:
            version_number = struct.unpack("B", e_bytes.read(1))[0]
        s_len = struct.unpack("i", e_bytes.read(4))[0]
        value = e_bytes.read(s_len * 2).decode('utf-16')
        return StringPropertyAtom(header, base_property_atom_data, version_number, value)
