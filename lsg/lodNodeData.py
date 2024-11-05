import struct
from dataclasses import dataclass

from jt_reader.lsg.groupNodeData import GroupNodeData
from jt_reader.lsg.types import VecF32


@dataclass
class LODNodeData:
    group_node_data: GroupNodeData
    version_number: int
    reserved_field1: VecF32
    reserved_field2: int

    @classmethod
    def from_bytes(cls, e_bytes):
        group_node_data = GroupNodeData.from_bytes(e_bytes)
        version_number = struct.unpack("h", e_bytes.read(2))[0]
        reserved_field1 = VecF32.from_bytes(e_bytes)
        reserved_field2 = struct.unpack("i", e_bytes.read(4))[0]
        return LODNodeData(group_node_data, version_number, reserved_field1, reserved_field2)
