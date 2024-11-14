import struct
from dataclasses import dataclass

from codec.i32Cdp2 import I32CDP2


@dataclass
class CompressedVertexFlagArray:
    vertex_flag_count: int
    vertex_flags: list

    @classmethod
    def from_bytes(cls, e_bytes):
        vertex_flag_count = struct.unpack("<I", e_bytes.read(4))[0]
        vertex_flags = I32CDP2.read_vec_i_32(e_bytes)
        return CompressedVertexFlagArray(vertex_flag_count, vertex_flags)
