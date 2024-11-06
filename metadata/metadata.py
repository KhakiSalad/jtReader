from dataclasses import dataclass

from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.metadata.metadataElement import MetadataElement
from jt_reader.metadata.propertyProxyMetaDataElement import PropertyProxyMetaDataElement


@dataclass
class Metadata:
    SEGMENT_TYPE_ID = 4
    data: list[MetadataElement]


def read_metadata_segment(ds_bytes, version):
    metadata = []
    end_of_elements = False
    while ds_bytes.remaining() > 0 and not end_of_elements:
        e_header = ElementHeader.from_bytes(ds_bytes)
        if e_header.object_type_id == PropertyProxyMetaDataElement.TYPE_ID:
            metadata.append(PropertyProxyMetaDataElement.from_bytes(ds_bytes, e_header, version=version))
        elif e_header.object_type_id == ElementHeader.END_OF_ELEMENTS:
            end_of_elements = True
        else:
            print(f'Found unsupported element type {e_header.object_type_id} while reading metadata segment.')
            ds_bytes.read(e_header.length - 21)
    return Metadata(metadata)
