import struct
from dataclasses import dataclass


@dataclass
class BasePropertyAtomData:
    version_number: int
    state_flags: int

    @classmethod
    def from_bytes(cls, e_bytes):
        return BasePropertyAtomData(*struct.unpack("<hi", e_bytes.read(6)))
