import struct
from dataclasses import dataclass


@dataclass
class TopoMeshLODData:
    """
    7.2.2.1.2.2 TopoMesh LOD Data

    TopoMesh LOD Data collection contains the common items to all TopoMesh LOD elements.
    """
    version_number: int
    vertex_records: int

    @classmethod
    def from_bytes(cls, e_bytes):
        version_number, vertex_records = struct.unpack("<hi", e_bytes.read(6))
        if version_number != 1 and version_number != 2:
            raise RuntimeError(f"Version {version_number} not supported for {cls.__name__}")
        return TopoMeshLODData(version_number, vertex_records)
