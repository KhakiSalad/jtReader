from dataclasses import dataclass

from lsg.elementHeader import ElementHeader
from lsg.groupNodeData import GroupNodeData
from lsg.types import GUID, JtVersion
from lsg.lsgNode import LSGNode


@dataclass
class GroupNodeElement(LSGNode):
    element_header: ElementHeader
    group_node_data: GroupNodeData

    TYPE_ID = GUID((0x10dd101b, 0x2ac8, 0x11d1, 0x9b, 0x6b,
                   0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97))
    BASE_TYPE = 1

    def __init__(self, element_header, group_node_data):
        self.element_header = element_header
        self.group_node_data = group_node_data

    @property
    def child_node_object_id(self) -> list[int]:
        return self.group_node_data.child_node_object_id

    @property
    def attr_object_id(self) -> list[int]:
        return self.group_node_data.base_node_data.attr_object_id

    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        return GroupNodeElement(header, GroupNodeData.from_bytes(e_bytes, version=version))
