from jt_reader.util.bitBuffer import BitBuffer
from jt_reader.util import ByteStream
import pytest
from operator import itemgetter


@pytest.fixture
def data() -> [bytes]:
    with open(r'Z:/DS im IE/8W8_827_605____PCA_TM__010_____HALTER_HKL_________150819______________.jt', "rb") as f:
        data = f.read(512)
    bs = ByteStream(data)
    bs_bit = ByteStream(data)
    bs.seek(0xe0)
    bs_bit.seek(0xe0)
    bits = BitBuffer(bs_bit)
    bits.position = bs_bit.offset << 3
    return {"bs": bs, "bits": bits}


def test_bits_read_int_word(data):
    bs, bits = itemgetter('bs', 'bits')(data)
    v1_bits = bits.read_int(32)
    v2_bits = bits.read_int(32)
    v3_bits = bits.read_int(32)
    v4_bits = bits.read_int(32)
    v1_bytes = int.from_bytes(bs.read(4), "little")
    v2_bytes = int.from_bytes(bs.read(4), "little")
    v3_bytes = int.from_bytes(bs.read(4), "little")
    v4_bytes = int.from_bytes(bs.read(4), "little")

    assert v1_bits == v1_bytes
    assert v2_bits == v2_bytes
    assert v3_bits == v3_bytes
    assert v4_bits == v4_bytes


def test_bits_read_int_byte(data):
    bs, bits = itemgetter('bs', 'bits')(data)
    v1_bits = bits.read_int(8)
    v2_bits = bits.read_int(8)
    v3_bits = bits.read_int(8)
    v4_bits = bits.read_int(8)
    v1_bytes = int.from_bytes(bs.read(1), "little")
    v2_bytes = int.from_bytes(bs.read(1), "little")
    v3_bytes = int.from_bytes(bs.read(1), "little")
    v4_bytes = int.from_bytes(bs.read(1), "little")

    assert v1_bits == v1_bytes
    assert v2_bits == v2_bytes
    assert v3_bits == v3_bytes
    assert v4_bits == v4_bytes


def test_bits_read_int_var_bits(data):
    bs, bits = itemgetter('bs', 'bits')(data)
    v1_bits = bits.read_int(3)
    v_bits = v1_bits
    v2_bits = bits.read_int(7)
    v_bits = v_bits | ((v2_bits & 31) << 3)
    v_bits = v_bits << 8

    v3_bits = bits.read_int(4)
    v_bits = v_bits | (v3_bits << 2) | ((v2_bits & 96) >> 5)
    v4_bits = bits.read_int(6)
    v_bits = v_bits + ((v4_bits & 3) << 6)
    v_bits = v_bits << 8
    v_bits = v_bits + ((v4_bits & 60) >> 2)

    v_bytes = int.from_bytes(bs.read(3), "big") & 0xffff0f
    print(f'\n{v_bits:_b} ---- {v_bytes:_b}')
    assert v_bits == v_bytes
