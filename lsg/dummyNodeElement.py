from dataclasses import dataclass

from jt_reader.lsg.elementHeader import ElementHeader
from .baseNodeData import BaseNodeData
from jt_reader.lsg.types import GUID, JtVersion
from jt_reader.lsg.lsgNode import LSGNode


@dataclass
class DummyNodeElement(LSGNode):
    element_header: ElementHeader
    base_node_data: BaseNodeData

    TYPE_ID = GUID((0,0,0,0,0,0,0,0,0,0))
    BASE_TYPE = -1

    def __init__(self, header=None):
        self.element_header = header
        self.base_node_data = BaseNodeData(0,0,0,0)
        pass


    @property
    def child_node_object_id(self) -> list[int]:
        return []

    @property
    def attr_object_id(self) -> list[int]:
        return []

    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        return DummyNodeElement()
