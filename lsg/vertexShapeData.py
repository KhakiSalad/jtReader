import struct
from dataclasses import dataclass

from jt_reader.lsg.baseShapeData import BaseShapeData
from jt_reader.lsg.types import QuantizationParameters, JtVersion
import sys


@dataclass
class VertexShapeData:
    base_shape_data: BaseShapeData
    version_number: int
    vertex_binding: int
    quantization_parameters: QuantizationParameters
    vertex_binding: int

    @classmethod
    def from_bytes(cls, e_bytes, version=JtVersion.V9d5):
        # print("VertexShapeData ---------------------- " + str(version))
        base_shape_data = BaseShapeData.from_bytes(e_bytes, version=version)
        if version == JtVersion.V9d5:
            version_number, vertex_binding = struct.unpack("<hQ", e_bytes.read(10))
        else:
            version_number, vertex_binding = struct.unpack("<BQ", e_bytes.read(9))

        quantization_parameters = QuantizationParameters.from_bytes(e_bytes)
        if version_number != 1:
            vertex_binding = struct.unpack("Q", e_bytes.read(8))[0]
        return VertexShapeData(base_shape_data, version_number, vertex_binding, quantization_parameters)
