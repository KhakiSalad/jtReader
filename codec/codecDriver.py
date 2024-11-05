from dataclasses import dataclass, field

from jt_reader.util.bitBuffer import BitBuffer
from jt_reader.codec.arithmetic.probabilityContext import ProbabilityContext
from jt_reader.util.byteStream import ByteStream


@dataclass
class CodecDriver:
    code_text: bytes
    code_text_length: int
    value_count: int
    int_32_probability_contexts: ProbabilityContext
    out_of_band_values: list
    bit_buffer: BitBuffer = field(default=None)
    bits_read: int = field(default=0)

    def __post_init__(self):
        self.bit_buffer = BitBuffer(ByteStream(self.code_text))

    def get_next_code_text(self):
        n_bits = min(32, (self.code_text_length - self.bits_read))
        u_code_text = self.bit_buffer.read_int(n_bits)

        if n_bits < 32:
            u_code_text = u_code_text << (32 - n_bits)
        self.bits_read += n_bits

        return u_code_text, n_bits
