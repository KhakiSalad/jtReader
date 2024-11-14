import struct
from dataclasses import dataclass
from lsg.types import JtVersion


@dataclass
class BaseNodeData:
    version_number: int
    node_flags: int
    attr_count: int
    attr_object_id: list[int]

    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        if version == JtVersion.V9d5:
            version_number, node_flags, attr_count = struct.unpack(
                "<hIi", e_bytes.read(2 + 4 + 4)
            )
        else:
            version_number, node_flags, attr_count = struct.unpack(
                "<BIi", e_bytes.read(1 + 4 + 4)
            )
        attr_obj_id = list(
            struct.unpack("i" * attr_count, e_bytes.read(attr_count * 4))
        )
        base_node_data = BaseNodeData(
            version_number, node_flags, attr_count, attr_obj_id
        )
        return base_node_data
