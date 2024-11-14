import struct
from dataclasses import dataclass

from lsg.groupNodeData import GroupNodeData
from lsg.types import VecF32, JtVersion


@dataclass
class LODNodeData:
    group_node_data: GroupNodeData
    version_number: int
    reserved_field1: VecF32
    reserved_field2: int

    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        group_node_data = GroupNodeData.from_bytes(e_bytes, version=version)
        if version == JtVersion.V9d5:
            version_number = struct.unpack("h", e_bytes.read(2))[0]
            reserved_field1 = VecF32.from_bytes(e_bytes)
            reserved_field2 = struct.unpack("i", e_bytes.read(4))[0]
        else:
            version_number = struct.unpack("B", e_bytes.read(1))[0]
            reserved_field1 = None
            reserved_field2 = None
        return LODNodeData(group_node_data, version_number, reserved_field1, reserved_field2)
