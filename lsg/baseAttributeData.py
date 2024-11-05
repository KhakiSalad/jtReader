import struct
from dataclasses import dataclass


@dataclass
class BaseAttributeData:
    version_number: int
    state_flags: int
    field_inhibit_flags: int

    @classmethod
    def from_bytes(cls, e_bytes):
        return BaseAttributeData(*struct.unpack("<hBI", e_bytes.read(7)))
