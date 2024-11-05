import logging
import struct
from dataclasses import dataclass, field

from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.lsg.types import GUID
from jt_reader.shape.shapeElement import ShapeElement
from jt_reader.shape.vertexShapeLODData import VertexShapeLODData
import logging

logger = logging.getLogger(__name__)


@dataclass
class TriStripSetShapeLodElement(ShapeElement):
    """
    7.2.2.1.3 Tri-Strip Set Shape LOD Element

    Object Type ID: 0x10dd10ab, 0x2ac8, 0x11d1, 0x9b, 0x6b, 0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97

    A Tri-Strip Set Shape LOD Element contains the geometric shape definition data (e.g. vertices, polygons, normals,
    etc.) for a single LOD of a collection of independent and unconnected triangle strips. Each strip constitutes one
    primitive of the set and the ordering of the vertices in forming triangles, is the same as OpenGL‟s triangle strip
    definition [4]. A Tri-Strip Set Shape LOD Element is typically referenced by a Tri-Strip Set Shape Node Element
    using Late Loaded Property Atom Elements (see 7.2.1.1.1.10.3 Tri-Strip Set Shape Node Element and 0 Late Loaded
    Property Atom Element Late Loaded Property Atom Element respectively).
    """
    TYPE_ID = GUID((0x10dd10ab, 0x2ac8, 0x11d1, 0x9b, 0x6b, 0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97))
    element_header: ElementHeader
    vertex_shape_LOD_data: VertexShapeLODData = field(repr=False)
    version_number: int

    @classmethod
    def from_bytes(cls, e_bytes, header=None):
        logger.debug(f'creating {header} from bytes')
        os_begin = e_bytes.offset

        vertex_shape_lod_data = VertexShapeLODData.from_bytes(e_bytes, shape="Tri-Strip")
        version_number = struct.unpack("<h", e_bytes.read(2))[0]

        os_end = e_bytes.offset
        # e_bytes.read(6)
        logger.debug(f'TriStripSetShapeLodElement read {os_end - os_begin} bytes of {header.length}')
        return TriStripSetShapeLodElement(header, vertex_shape_lod_data, version_number)
