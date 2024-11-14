import logging
from dataclasses import dataclass, field
from typing import Literal

from util.byteStream import ByteStream

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


@dataclass
class BitBuffer:
    e_bytes: ByteStream
    position: int = field(default=0)
    endianness: Literal["little", "big"] = field(default="big")

    def read_int(self, num_bits):
        num_bytes = (((self.position % 8) + num_bits + 7) // 8)
        num_buff = self.get_number_buf_as_int(num_bytes, (self.position >> 3))
        if self.endianness == "big":
            shift_bits = 7 - ((num_bits + self.position + 7) % 8)
        else:
            shift_bits = self.position % 8
        right_shifted = num_buff >> shift_bits
        if num_bytes <= 4:
            mask = 0xFFFFFFFF >> (32 - num_bits)
        else:
            mask = 0xFFFFFFFFFFFFFFFF >> (64 - num_bits)
        result = mask & right_shifted
        self.position += num_bits
        logger.debug(
            f"finished read int {num_bits=} {num_bytes=} {num_buff=} {shift_bits=} {right_shifted=} {result=}")
        return result

    def get_number_buf_as_int(self, num_bytes, first_byte_pos):
        result = 0
        0

        for i in range(num_bytes):
            byte_part = 0xFF & self.e_bytes.bytes[first_byte_pos]
            if self.endianness == "big":
                result = (byte_part << ((num_bytes - i - 1) << 3)) | result
            else:
                result = result | (byte_part << (i << 3))
            first_byte_pos += 1
        return result

    def read_signed_int(self, num_bits):
        result = self.read_int(num_bits)
        sign_bit = 1 << (num_bits-1)
        result = result | (-(result & sign_bit))
        return result
