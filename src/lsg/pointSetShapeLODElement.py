import struct
from dataclasses import dataclass
from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.lsg.types import GUID, VecF32, CoordF32, JtVersion
from jt_reader.lsg.lsgNode import LSGNode
from jt_reader.shape.vertexShapeLODData import VertexShapeLODData


@dataclass
class PointSetShapeLODElement(LSGNode):
    TYPE_ID = GUID((0x98134716, 0x0011, 0x0818, 0x19, 0x98, 0x08, 0x00, 0x09, 0x83, 0x5d, 0x5a))
    BASE_TYPE = 1

    element_header: ElementHeader
    vertex_shape_lod_data: VertexShapeLODData
    version_number: int


    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        vertex_shape_lod_data = VertexShapeLODData.from_bytes(e_bytes, version=version)
        version_number = struct.unpack("B", e_bytes.read(1))[0]
        return PointSetShapeLODElement(header, vertex_shape_lod_data, version_number)
