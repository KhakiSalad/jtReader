from dataclasses import dataclass


@dataclass
class TopoMeshCompressedRepData:
    """
    7.2.2.1.2.8 TopoMesh Compressed Rep Data V2

    TopoMesh Compressed Rep Data V2 data contains additional geometric shape data (auxiliary vertex fields) that were
    not included in V1. Auxiliary fields are parallel to the existing vertex record information and contain additional
    information pertaining to each vertex.
    """

    @classmethod
    def from_bytes(cls, e_bytes):
        raise RuntimeError(f"{cls.__name__} not implemented")
        return TopoMeshCompressedRepData()
