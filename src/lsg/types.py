import struct
from dataclasses import dataclass
from enum import Enum


JtVersion = Enum('JtVersion', ["V9d5", "V10d5", "unsupported"])

@dataclass
class GUID:
    guid: (int, int, int, int, int, int, int, int, int, int, int)

    def __repr__(self):
        guid_str = "{" + f"{self.guid[0]:08X}-{self.guid[1]:04X}-{self.guid[2]:04X}-" + \
                   "-".join([f"{self.guid[i]:02X}" for i in range(3, 11)]) + "}"
        return guid_str

    @classmethod
    def from_bytes(cls, e_bytes):
        guid_bytes = e_bytes.read(16)
        if guid_bytes == b'':
            return GUID((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        guid = GUID(struct.unpack("IHHBBBBBBBB", guid_bytes))
        return guid


@dataclass
class CoordF32:
    x: float
    y: float
    z: float


@dataclass
class BBoxF32:
    min_corner: CoordF32
    max_corner: CoordF32

    @classmethod
    def from_coords(cls, f1, f2, f3, f4, f5, f6):
        return BBoxF32(CoordF32(f1, f2, f3), CoordF32(f4, f5, f6))


@dataclass
class VecF32:
    count: int
    data: list[int]

    @classmethod
    def from_bytes(cls, e_bytes):
        count = struct.unpack("i", e_bytes.read(4))[0]
        data = list(*struct.unpack("i" * count, e_bytes.read(4 * count)))
        return VecF32(count, data)


@dataclass
class QuantizationParameters:
    bits_per_vertex: int
    normal_bits_factor: int
    bits_per_texture_coord: int
    bits_per_color: int

    @classmethod
    def from_bytes(cls, e_bytes):
        return QuantizationParameters(*struct.unpack("BBBB", e_bytes.read(4)))
