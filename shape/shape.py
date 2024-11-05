import logging
from dataclasses import dataclass

from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.shape.triStripSetShapeLODElement import TriStripSetShapeLodElement

logger = logging.getLogger(__name__)
@dataclass
class Shape:
    SEGMENT_TYPE_ID = 6


def read_shape_segment(ds_bytes):
    end_of_elements = False
    shapes = {}
    while ds_bytes.remaining() > 0 and not end_of_elements:
        e_header = ElementHeader.from_bytes(ds_bytes)
        if e_header.object_type_id == TriStripSetShapeLodElement.TYPE_ID:
            pre_offset = ds_bytes.offset
            shape = TriStripSetShapeLodElement.from_bytes(ds_bytes, header=e_header)
            post_offset = ds_bytes.offset
            length = post_offset - pre_offset
            remaining = e_header.length - 25 - length
            ds_bytes.read(remaining)
            ds_bytes.read(4)
        elif e_header.object_type_id == ElementHeader.END_OF_ELEMENTS:
            shape = None
            end_of_elements = True
        else:
            shape = None
            logger.error(f'Found unsupported element type {e_header.object_type_id} while reading shape segment.')
            ds_bytes.read(e_header.length - 21)
        shapes[e_header.object_id] = shape
    return shapes