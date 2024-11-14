from dataclasses import dataclass
import struct
import logging

from .elementHeader import ElementHeader
from .baseNodeData import BaseNodeData
from .types import GUID, JtVersion
from .lsgNode import LSGNode
logger = logging.getLogger(__name__)

@dataclass
class InstanceNodeElement(LSGNode):
    element_header: ElementHeader
    base_node_data: BaseNodeData
    version_number: int
    _child_node_object_id: list[int]

    TYPE_ID = GUID((0x10dd102a, 0x2ac8, 0x11d1, 0x9b, 0x6b, 0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97))
    BASE_TYPE = 1

    @property
    def child_node_object_id(self):
        return self._child_node_object_id

    @property
    def attr_object_id(self) -> list[int]:
        return self.base_node_data.attr_object_id
 
    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        logger.debug(f"{version=}")
        base_node_data = BaseNodeData.from_bytes(e_bytes, version=version)
        version_number = struct.unpack("B", e_bytes.read(1))[0]
        child_node_object_id = struct.unpack("I", e_bytes.read(4))
        return InstanceNodeElement(header, base_node_data, version_number, child_node_object_id)
