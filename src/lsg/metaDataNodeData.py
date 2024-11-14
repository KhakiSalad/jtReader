import struct
from dataclasses import dataclass

from lsg.groupNodeData import GroupNodeData
from lsg.types import JtVersion


@dataclass
class MetaDataNodeData:
    group_node_data: GroupNodeData
    version_number: int

    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        # print("meta data ---------------------- " + str(version))
        group_node_data = GroupNodeData.from_bytes(e_bytes, version=version)
        if version == JtVersion.V9d5:
            version_number = struct.unpack("h", e_bytes.read(2))[0]
        else:
            version_number = struct.unpack("B", e_bytes.read(1))[0]
        return MetaDataNodeData(group_node_data, version_number)
