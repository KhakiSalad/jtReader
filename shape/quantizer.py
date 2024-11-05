import struct
from dataclasses import dataclass


@dataclass
class UniformQuantizerData:
    min_v: float
    max_v: float
    number_of_bits: int

    @classmethod
    def from_bytes(cls, e_bytes):
        min_v, max_v, number_of_bits = struct.unpack("<ffB", e_bytes.read(9))
        return UniformQuantizerData(min_v, max_v, number_of_bits)


@dataclass
class PointQuantizerData:
    x: UniformQuantizerData
    y: UniformQuantizerData
    z: UniformQuantizerData

    def number_of_bits(self):
        if (self.x.number_of_bits != self.y.number_of_bits) or (self.x.number_of_bits != self.z.number_of_bits):
            raise RuntimeError('Number of qunatized bits differs.')
        return self.x.number_of_bits

    @classmethod
    def from_bytes(cls, e_bytes):
        x = UniformQuantizerData.from_bytes(e_bytes)
        y = UniformQuantizerData.from_bytes(e_bytes)
        z = UniformQuantizerData.from_bytes(e_bytes)
        return PointQuantizerData(x, y, z)
