import struct
from dataclasses import dataclass
from lsg.types import JtVersion
import logging

logger = logging.getLogger(__name__)


@dataclass
class TopoMeshLODData:
    """
    7.2.2.1.2.2 TopoMesh LOD Data
    """
    version_number: int
    vertex_records: int

    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        logger.debug(e_bytes.bytes[e_bytes.offset: e_bytes.offset+20].hex(" "))
        if version == JtVersion.V9d5:
            version_number = struct.unpack("<h", e_bytes.read(2))[0]
        else:
            version_number = struct.unpack("B", e_bytes.read(1))[0]
        vertex_records = struct.unpack("<i", e_bytes.read(4))
        if version_number != 1 and version_number != 2:
            raise RuntimeError(
                f"Version {version_number} not supported for {cls.__name__}")
        return TopoMeshLODData(version_number, vertex_records)
