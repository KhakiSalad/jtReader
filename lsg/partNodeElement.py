import struct
from dataclasses import dataclass

from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.lsg.metaDataNodeData import MetaDataNodeData
from jt_reader.lsg.types import GUID, JtVersion
from jt_reader.lsg.lsgNode import LSGNode


@dataclass
class PartNodeElement(LSGNode):
    TYPE_ID = GUID((0xce357244, 0x38fb, 0x11d1, 0xa5, 0x6, 0x0, 0x60, 0x97, 0xbd, 0xc6, 0xe1))
    BASE_TYPE = 1

    element_header: ElementHeader
    metadata_node_data: MetaDataNodeData
    version_number: int
    res: int

    @property
    def child_node_object_id(self) -> list[int]:
        return self.metadata_node_data.group_node_data.child_node_object_id

    @property
    def attr_object_id(self) -> list[int]:
        return self.metadata_node_data.group_node_data.base_node_data.attr_object_id

    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        metadata_node_data = MetaDataNodeData.from_bytes(e_bytes)
        if version == JtVersion.V9d5:
            version_number, res = struct.unpack("<hi", e_bytes.read(6))
        elif version == JtVersion.V10d5:
            version_number, res = struct.unpack("<Bi", e_bytes.read(5))
        return PartNodeElement(header, metadata_node_data, version_number, res)

    @property
    def group_node_data(self):
        return self.metadata_node_data.group_node_data
