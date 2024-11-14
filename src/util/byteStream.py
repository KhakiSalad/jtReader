import struct


class ByteStream:
    bytes: bytes
    offset: int

    def __init__(self, b, offset=0):
        self.bytes = b
        self.offset = offset

    def read(self, length: int):
        if self.offset + length >= len(self.bytes):
            return self.bytes[self.offset:]
        data = self.bytes[self.offset: self.offset + length]
        self.offset += length
        return data

    def get(self, index: int):
        self.offset = index + 1
        return self.bytes[self.offset-1]

    def seek(self, i: int):
        self.offset = i

    def remaining(self):
        return len(self.bytes) - self.offset


def read_vec_i_32(byte_stream):
    count = int.from_bytes(byte_stream.read(4), "little")
    return list(struct.unpack("<" + "i" * count, byte_stream.read(count * 4)))


def read_vec_u_32(byte_stream):
    count = int.from_bytes(byte_stream.read(4), "little")
    return list(struct.unpack("<" + "I" * count, byte_stream.read(count * 4)))
