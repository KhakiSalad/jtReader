import struct
from dataclasses import dataclass

from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.lsg.groupNodeData import GroupNodeData
from jt_reader.lsg.types import GUID, BBoxF32, JtVersion
from jt_reader.lsg.lsgNode import LSGNode

import logging
logger = logging.getLogger(__name__)


@dataclass
class PartitionNodeElement(LSGNode):
    TYPE_ID = GUID((0x10dd103e, 0x2ac8, 0x11d1, 0x9b, 0x6b, 0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97))
    BASE_TYPE = 1
    element_header: ElementHeader
    group_node_data: GroupNodeData
    partition_flags: int
    filename: str
    transformed_bbox: BBoxF32
    area: float
    v_count_range: (int, int)
    n_count_range: (int, int)
    p_count_range: (int, int)
    untransformed_bbox: BBoxF32 = None

    @property
    def child_node_object_id(self) -> list[int]:
        return self.group_node_data.child_node_object_id

    @property
    def attr_object_id(self) -> list[int]:
        return self.group_node_data.base_node_data.attr_object_id

    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        # **** group node data ****
        group_node_data = GroupNodeData.from_bytes(e_bytes, version=version)
        # print(group_node_data)
        # **** partition flags ****
        partition_flags = struct.unpack("i", e_bytes.read(4))[0]
        # **** file name ****
        s_len = struct.unpack("i", e_bytes.read(4))[0]
        filename = e_bytes.read(2 * s_len).decode('utf-16')
        logger.info(f"started loading file {filename}")
        # **** reservedField | Transformed BBox ****
        transformed_bbox = BBoxF32.from_coords(*struct.unpack("ffffff", e_bytes.read(24)))
        # **** Area ****
        area = struct.unpack("f", e_bytes.read(4))[0]
        # **** Vertex, Node, Poly Count Range ****
        v_count_min, v_count_max = struct.unpack("ii", e_bytes.read(8))
        n_count_min, n_count_max = struct.unpack("ii", e_bytes.read(8))
        p_count_min, p_count_max = struct.unpack("ii", e_bytes.read(8))
        # **** pass | Untransformed BBox ****
        if partition_flags & 0x00000001 != 0:
            untransformed_bbox = BBoxF32.from_coords(*struct.unpack("ffffff", e_bytes.read(24)))
        else:
            untransformed_bbox = None
        return PartitionNodeElement(element_header=header,
                                    group_node_data=group_node_data,
                                    partition_flags=partition_flags,
                                    filename=filename,
                                    transformed_bbox=transformed_bbox,
                                    area=area,
                                    v_count_range=(v_count_min, v_count_max),
                                    n_count_range=(n_count_min, n_count_max),
                                    p_count_range=(p_count_min, p_count_max),
                                    untransformed_bbox=untransformed_bbox)
