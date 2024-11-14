import struct
from dataclasses import dataclass
from lsg.types import GUID


@dataclass
class ElementHeader:
    END_OF_ELEMENTS = GUID(
        (0xffffffff, 0xffff, 0xffff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff))

    length: int
    object_type_id: GUID
    object_base_type: int
    object_id: int

    @classmethod
    def from_bytes(cls, e_bytes):
        length = struct.unpack("i", e_bytes.read(4))[0]
        guid = GUID.from_bytes(e_bytes)
        if guid == cls.END_OF_ELEMENTS:
            return ElementHeader(length, guid, -1, -1)
        base_type = int.from_bytes(e_bytes.read(1), byteorder="little")
        texture_coord = struct.unpack("i", e_bytes.read(4))[0]
        return ElementHeader(length, guid, base_type, texture_coord)
