import struct
from dataclasses import dataclass
from lsg.elementHeader import ElementHeader
from lsg.types import GUID, JtVersion
from lsg.lsgNode import LSGNode
from lsg.vertexShapeData import VertexShapeData


@dataclass
class PointSetShapeNodeElement(LSGNode):
    TYPE_ID = GUID((0x98134716, 0x0010, 0x0818, 0x19, 0x98,
                   0x08, 0x00, 0x09, 0x83, 0x5d, 0x5a))
    BASE_TYPE = 1

    element_header: ElementHeader
    vertex_shape_data: VertexShapeData
    version_number: int
    area_factor: float
    vertex_binding: int

    @property
    def child_node_object_id(self) -> list[int]:
        return []

    @property
    def attr_object_id(self) -> list[int]:
        return self.vertex_shape_data.base_shape_data.base_node_data.attr_object_id

    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        vertex_shape_data = VertexShapeData.from_bytes(
            e_bytes, version=version)
        version_number, area_factor = struct.unpack("<Bf", e_bytes.read(5))
        if version_number != 1:
            vertex_binding = struct.unpack("Q", e_bytes.read(8))[0]
        return PointSetShapeNodeElement(header, vertex_shape_data, version_number, area_factor, vertex_binding)
