from dataclasses import dataclass

from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.lsg.types import GUID
from jt_reader.lsg.vertexShapeData import VertexShapeData
from jt_reader.lsg.lsgNode import LSGNode


@dataclass
class TriStripSetShapeNodeElement(LSGNode):
    TYPE_ID = GUID((0x10dd1077, 0x2ac8, 0x11d1, 0x9b, 0x6b, 0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97))
    BASE_TYPE = 2

    element_header: ElementHeader
    vertex_shape_data: VertexShapeData

    @property
    def child_node_object_id(self) -> list[int]:
        return []

    @property
    def attr_object_id(self) -> list[int]:
        return self.vertex_shape_data.base_shape_data.base_node_data.attr_object_id

    @classmethod
    def from_bytes(cls, e_bytes, header=None):
        return TriStripSetShapeNodeElement(header, VertexShapeData.from_bytes(e_bytes))
