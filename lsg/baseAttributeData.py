import struct
from dataclasses import dataclass
from .types import JtVersion


@dataclass
class BaseAttributeData:
    version_number: int
    state_flags: int
    field_inhibit_flags: int
    palette_index: int


    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        if version == JtVersion.V9d5: 
            return BaseAttributeData(*struct.unpack("<hBI", e_bytes.read(7)), None)
        else:
            version_number = struct.unpack("B", e_bytes.read(1))
            state_flags, field_inhibit_flags = struct.unpack("II", e_bytes.read(8))
            palette_index = None
            if version_number == 2:
                palette_index = struct.unpack("I", e_bytes.read(4))[0]
            return BaseAttributeData(version_number, state_flags, field_inhibit_flags, palette_index)
