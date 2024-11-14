import abc

from lsg.elementHeader import ElementHeader


class LSGNode(abc.ABC):
    TYPE_ID = 0
    BASE_TYPE = 0

    element_header: ElementHeader
    child_nodes: list["LSGNode"]
    attributes: list["LSGNode"]
    properties: dict

    @property
    @abc.abstractmethod
    def child_node_object_id(self) -> list[int]:
        pass

    @property
    @abc.abstractmethod
    def attr_object_id(self) -> list[int]:
        pass

    @abc.abstractmethod
    def from_bytes(self, e_bytes, header):
        pass
