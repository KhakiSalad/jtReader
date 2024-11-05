import struct
from dataclasses import dataclass

from jt_reader.properties.basePropertyAtomData import BasePropertyAtomData
from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.properties.lsgProperty import LSGProperty
from jt_reader.lsg.types import GUID


@dataclass
class LateLoadedPropertyAtom(LSGProperty):
    TYPE_ID = GUID((0xe0b05be5, 0xfbbd, 0x11d1, 0xa3, 0xa7, 0x00, 0xaa, 0x00, 0xd1, 0x09, 0x54))
    element_header: ElementHeader
    base_property_atom_data: BasePropertyAtomData
    version_number: int
    segment_id: GUID
    segment_type: int
    payload_object_id: int
    reserved: int
    loaded = False

    @property
    def val(self):
        if not self.loaded:
            return self

    @classmethod
    def from_bytes(cls, e_bytes, header=None):
        base_property_atom_data = BasePropertyAtomData.from_bytes(e_bytes)
        version_number = struct.unpack("h", e_bytes.read(2))[0]
        segment_id = GUID.from_bytes(e_bytes)
        segment_type, payload_object_id, reserved = struct.unpack("iii", e_bytes.read(12))
        return LateLoadedPropertyAtom(header,
                                      base_property_atom_data,
                                      version_number,
                                      segment_id,
                                      segment_type,
                                      payload_object_id,
                                      reserved)

    def __repr__(self):
        return f"LateLoadedPropertyAtom(object_id={self.element_header.object_id}, segment_id={self.segment_id}, " \
               f"payload_object_id={self.payload_object_id}) "
