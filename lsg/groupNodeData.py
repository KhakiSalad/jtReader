import struct
from dataclasses import dataclass

from jt_reader.lsg.baseNodeData import BaseNodeData
from jt_reader.lsg.types import JtVersion


@dataclass
class GroupNodeData:
    base_node_data: BaseNodeData
    version_number: int
    child_count: int
    child_node_object_id: list[int]

    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        print("GroupNodeData ---------------------- " + str(version))
        base_node_data = BaseNodeData.from_bytes(e_bytes, version=version)
        if version == JtVersion.V9d5:
            version_number, child_count = struct.unpack("<hi", e_bytes.read(6))
        else:
            version_number, child_count = struct.unpack("<Bi", e_bytes.read(5))
        child_node_object_id = struct.unpack("i" * child_count, e_bytes.read(4 * child_count))
        if version == JtVersion.V10d5:
            # warum auch immer, aber scheint zu funktionieren
            e_bytes.read(1)
        return GroupNodeData(base_node_data,
                             version_number,
                             child_count,
                             [*child_node_object_id])
