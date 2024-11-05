import datetime
import struct
from dataclasses import dataclass

from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.lsg.types import GUID
from jt_reader.metadata.metadataElement import MetadataElement


@dataclass
class PropertyProxyMetaDataElement(MetadataElement):
    TYPE_ID = GUID((0xce357247, 0x38fb, 0x11d1, 0xa5, 0x6, 0x0, 0x60, 0x97, 0xbd, 0xc6, 0xe1))
    element_header: ElementHeader
    version_number: int
    _properties: dict[str, object]

    def __init__(self, element_header, version_number, properties):
        self.element_header = element_header
        self.version_number = version_number
        self._properties = properties

    @property
    def properties(self) -> dict:
        return self._properties

    @classmethod
    def from_bytes(cls, e_bytes, header=None):
        version_number = struct.unpack("<h", e_bytes.read(2))[0]
        properties = {}
        s_len = struct.unpack("i", e_bytes.read(4))[0]
        property_key = e_bytes.read(2 * s_len).decode('utf-16')
        while property_key != "":
            value_type = struct.unpack("<B", e_bytes.read(1))[0]
            property_val = None
            if value_type == 1:
                # string
                s_len = struct.unpack("i", e_bytes.read(4))[0]
                property_val = e_bytes.read(2 * s_len).decode('utf-16')
            elif value_type == 2:
                # I32
                property_val = struct.unpack("I", e_bytes.read(4))
            elif value_type == 3:
                # F32
                property_val = struct.unpack("f", e_bytes.read(4))
            elif value_type == 4:
                # date year, month, day, hour, minute, second
                property_val = datetime.datetime(*struct.unpack("<hhhhhh", e_bytes.read(12)))

            properties[property_key] = property_val
            s_len = struct.unpack("i", e_bytes.read(4))[0]
            property_key = e_bytes.read(2 * s_len).decode('utf-16')
        return PropertyProxyMetaDataElement(header, version_number, properties)
