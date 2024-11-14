import struct
from dataclasses import dataclass

from lsg.baseNodeData import BaseNodeData
from lsg.types import BBoxF32, JtVersion


@dataclass
class BaseShapeData:
    base_node_data: BaseNodeData
    version_number: int
    reserved_field1: BBoxF32
    untransformed_bbox: BBoxF32
    area: float
    v_count_min: int
    v_count_max: int
    n_count_min: int
    n_count_max: int
    p_count_min: int
    p_count_max: int
    size: int
    compression_level: float

    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        # print("VertexShapeData ---------------------- " + str(version))
        base_node_data = BaseNodeData.from_bytes(e_bytes, version=version)
        if version == JtVersion.V9d5:
            version_number = struct.unpack("h", e_bytes.read(2))[0]
        else:
            version_number = struct.unpack("B", e_bytes.read(1))[0]
        reserverd_field1 = BBoxF32.from_coords(
            *struct.unpack("ffffff", e_bytes.read(24)))
        untransformed_bbox = BBoxF32.from_coords(
            *struct.unpack("ffffff", e_bytes.read(24)))
        area = struct.unpack("f", e_bytes.read(4))[0]
        v_count_min, v_count_max = struct.unpack("ii", e_bytes.read(8))
        n_count_min, n_count_max = struct.unpack("ii", e_bytes.read(8))
        p_count_min, p_count_max = struct.unpack("ii", e_bytes.read(8))
        size, compression_level = struct.unpack("if", e_bytes.read(8))
        return BaseShapeData(base_node_data,
                             version_number,
                             reserverd_field1,
                             untransformed_bbox,
                             area,
                             v_count_min,
                             v_count_max,
                             n_count_min,
                             n_count_max,
                             p_count_min,
                             p_count_max,
                             size,
                             compression_level)
