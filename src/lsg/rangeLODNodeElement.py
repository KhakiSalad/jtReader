import struct
from dataclasses import dataclass

from lsg.elementHeader import ElementHeader
from lsg.lodNodeData import LODNodeData
from lsg.types import GUID, VecF32, CoordF32, JtVersion
from lsg.lsgNode import LSGNode


@dataclass
class RangeLODNodeElement(LSGNode):
    TYPE_ID = GUID((0x10dd104c, 0x2ac8, 0x11d1, 0x9b, 0x6b,
                   0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97))
    BASE_TYPE = 1

    element_header: ElementHeader
    lod_node_data: LODNodeData
    version_number: int
    range_limit: VecF32
    center: CoordF32

    @property
    def child_node_object_id(self) -> list[int]:
        return self.lod_node_data.group_node_data.child_node_object_id

    @property
    def attr_object_id(self) -> list[int]:
        return self.lod_node_data.group_node_data.base_node_data.attr_object_id

    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        lod_node_data = LODNodeData.from_bytes(e_bytes, version=version)
        version_number = struct.unpack("h", e_bytes.read(2))[0]
        range_limit = VecF32.from_bytes(e_bytes)
        center = CoordF32(*struct.unpack("fff", e_bytes.read(12)))
        return RangeLODNodeElement(header, lod_node_data, version_number, range_limit, center)

    @property
    def group_node_data(self):
        return self.lod_node_data.group_node_data
