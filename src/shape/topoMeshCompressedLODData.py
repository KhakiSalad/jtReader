import struct
from dataclasses import dataclass

from jt_reader.shape.topoMeshCompressedRepData import TopoMeshCompressedRepData
from jt_reader.shape.topoMeshLODData import TopoMeshLODData
from jt_reader.lsg.types import JtVersion


@dataclass
class TopoMeshCompressedLODData:
    """
    7.2.2.1.2.3 TopoMesh Compressed LOD Data

    TopoMesh Compressed LOD Data collection contains the common items to all TopoMesh Compressed LOD data elements.
    """
    topo_mesh_lod_data: TopoMeshLODData
    version_number: int
    topo_mesh_compressed_rep_data: TopoMeshCompressedRepData

    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        topo_mesh_lod_data = TopoMeshLODData.from_bytes(e_bytes, version=version)
        if version == JtVersion.V9d5:
            version_number = struct.unpack("<h", e_bytes.read(2))[0]
        else:
            version_number = struct.unpack("B", e_bytes.read(1))[0]
        if version_number != 1 and version_number != 2:
            raise RuntimeError(f"Version {version_number} not supported for {cls.__name__}")
        if version_number >= 2:
            # TopoMeshCompressedRepData V2
            topo_mesh_compressed_rep_data = TopoMeshCompressedRepData.from_bytes(e_bytes)
        else:
            raise RuntimeError("TopoMesh Compressed Rep Data V1 not supported.")
        return TopoMeshCompressedLODData(topo_mesh_lod_data, version_number, topo_mesh_compressed_rep_data)
