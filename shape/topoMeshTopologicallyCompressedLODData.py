import struct

from jt_reader.shape.topoMeshCompressedLODData import TopoMeshCompressedLODData
from jt_reader.shape.topoMeshLODData import TopoMeshLODData
from jt_reader.shape.topologicallyCompressedRepData import TopologicallyCompressedRepData


class TopoMeshTopologicallyCompressedLODData:
    """
    7.2.2.1.2.4 TopoMesh Topologically Compressed LOD Data

    TopoMesh Topologically Compressed LOD Data collection contains the common items to all TopoMesh Topologically
    Compressed LOD data elements.
    """
    topo_mesh_lod_data: TopoMeshLODData
    version_number: int
    topo_mesh_compressed_rep_data: TopologicallyCompressedRepData

    @classmethod
    def from_bytes(cls, e_bytes):
        topo_mesh_lod_data = TopoMeshLODData.from_bytes(e_bytes)
        version_number = struct.unpack("<h", e_bytes.read(2))[0]

        topo_mesh_compressed_rep_data = TopologicallyCompressedRepData.from_bytes(e_bytes)

        return TopoMeshCompressedLODData(topo_mesh_lod_data, version_number, topo_mesh_compressed_rep_data)
