import struct
from dataclasses import dataclass
from jt_reader.lsg.types import JtVersion


@dataclass
class BasePropertyAtomData:
    version_number: int
    state_flags: int

    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        if version==JtVersion.V9d5:
            return BasePropertyAtomData(*struct.unpack("<hi", e_bytes.read(6)))
        return BasePropertyAtomData(*struct.unpack("<BI", e_bytes.read(5)))

