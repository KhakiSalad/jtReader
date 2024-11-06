import struct
from dataclasses import dataclass

from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.lsg.baseAttributeData import BaseAttributeData
from jt_reader.lsg.types import GUID, JtVersion
from jt_reader.lsg.lsgNode import LSGNode


@dataclass
class MaterialAttributeElement(LSGNode):
    TYPE_ID = GUID((0x10dd1030, 0x2ac8, 0x11d1, 0x9b, 0x6b, 0x00, 0x80, 0xc7, 0xbb, 0x59, 0x97))
    BASE_TYPE = 3

    element_header: ElementHeader
    base_attribute_data: BaseAttributeData
    version_number: int
    data_flags: int
    ambient_color: (float, float, float, float)
    diffuse_color_and_alpha: (float, float, float, float)
    specular_color: (float, float, float, float)
    emission_color: (float, float, float, float)
    Shininess: float
    reflectivity: float

    @property
    def child_node_object_id(self) -> list[int]:
        return []

    @property
    def attr_object_id(self) -> list[int]:
        return []

    @classmethod
    def from_bytes(cls, e_bytes, header=None, version=JtVersion.V9d5):
        base_attribute_data = BaseAttributeData.from_bytes(e_bytes)
        if version == JtVersion.V9d5:
            version_number, data_flags = struct.unpack("<hH", e_bytes.read(4))
        else: 
            version_number, data_flags = struct.unpack("<BH", e_bytes.read(3))
        ambient_color = struct.unpack("ffff", e_bytes.read(16))
        diffuse_color_and_alpha = struct.unpack("ffff", e_bytes.read(16))
        specular_color = struct.unpack("ffff", e_bytes.read(16))
        emission_color = struct.unpack("ffff", e_bytes.read(16))
        shininess = struct.unpack("f", e_bytes.read(4))[0]
        reflectivity = -1
        if version_number == 2:
            reflectivity = struct.unpack("f", e_bytes.read(4))[0]
        return MaterialAttributeElement(header,
                                        base_attribute_data,
                                        version_number,
                                        data_flags,
                                        ambient_color,
                                        diffuse_color_and_alpha,
                                        specular_color,
                                        emission_color,
                                        shininess,
                                        reflectivity)
