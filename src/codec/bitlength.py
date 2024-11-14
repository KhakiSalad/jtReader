import logging
from codec.codecDriver import CodecDriver

logger = logging.getLogger(__name__)
# logger.setLevel("INFO")


def get_bit_field_width(symbol: int):
    symbol = abs(symbol)
    if symbol == 0:
        return 0
    i = 1
    bit_field_width = 0
    while i <= symbol and bit_field_width < 31:
        i += i
        bit_field_width += 1
    return bit_field_width


def decode_bitlength2(codec_driver: CodecDriver):
    encoded_bits = codec_driver.bit_buffer
    decoded_symbols = []

    expected_values = codec_driver.value_count
    total_bits = codec_driver.code_text_length
    logger.debug(f"{encoded_bits.position=}")

    # Handle fixed width
    if encoded_bits.read_int(1) == 0:
        logger.debug(f"{encoded_bits.position=}")
        logger.debug(
            f"starting fixed length decode of {codec_driver.code_text.hex(' ')}")
        db_str = " ".join([f"{int(b):08b}" for b in codec_driver.code_text])
        logger.debug(db_str)

        # Read the min and max symbols from the stream
        num_bits_from_min_symbol = 0
        num_bits_from_max_symbol = 0
        cNibbles = 0
        while True:
            tmp = encoded_bits.read_int(4)
            num_bits_from_min_symbol |= (tmp << (cNibbles * 4))
            more_bits = encoded_bits.read_int(1)
            if more_bits != 1:
                sw = cNibbles * 4
                if sw < 32:
                    num_bits_from_min_symbol <<= 32 - sw
                    num_bits_from_min_symbol >>= 32 - sw
                break
        cNibbles = 0
        while True:
            tmp = encoded_bits.read_int(4)
            num_bits_from_max_symbol |= (tmp << (cNibbles * 4))
            more_bits = encoded_bits.read_int(1)
            if more_bits != 1:
                sw = cNibbles * 4
                if sw < 32:
                    num_bits_from_max_symbol <<= 32 - sw
                    num_bits_from_max_symbol >>= 32 - sw
                break
        # num_bits_from_min_symbol = encoded_bits.read_int(n)
        # num_bits_from_max_symbol = encoded_bits.read_int(n)
        #   min_symbol = encoded_bits.read_signed_int(num_bits_from_min_symbol)
        #   max_symbol = encoded_bits.read_signed_int(num_bits_from_max_symbol)
        min_symbol = (num_bits_from_min_symbol)
        max_symbol = (num_bits_from_max_symbol)
        # bit_width = get_bit_field_width(max_symbol - min_symbol)

        def nlz(x):
            x = x | (x >> 1)
            x = x | (x >> 2)
            x = x | (x >> 4)
            x = x | (x >> 8)
            x = x | (x >> 16)
            return popcnt(~x)

        def popcnt(x):
            x = x - ((x >> 1) & 0x55555555)
            x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
            x = (x + (x >> 4)) & 0x0f0f0f0f
            x = x + (x >> 8)
            x = x + (x >> 16)
            return x & 0x3f

        bit_width = (max_symbol - min_symbol)
        bit_width = bit_width ^ (bit_width >> 31)
        bit_width = 33 - nlz(bit_width)
        logger.debug(f"{bit_width=} {min_symbol=} {max_symbol=}")
        logger.debug(f"{encoded_bits.position}")
        db_str = "".join([f"{int(b):08b}" for b in codec_driver.code_text])
        logger.debug(f"{db_str[encoded_bits.position:]=}, {total_bits=}")

        # Read each fixed-width field and output the value
        while encoded_bits.position < total_bits or len(decoded_symbols) < expected_values:
            decoded_symbol = encoded_bits.read_int(bit_width)
            decoded_symbol += min_symbol
            decoded_symbols.append(decoded_symbol)
        logger.debug("finished fixed length decode")
        logger.debug(f"{decoded_symbols=}")
    # Handle variable width
    else:
        # Write out the mean value
        logger.debug(
            f"starting variable width decode of {codec_driver.code_text.hex(' ')}")
        mean_value = encoded_bits.read_int(32)
        block_val_bits = encoded_bits.read_int(3)
        block_len_bits = encoded_bits.read_int(3)

        # Set the initial field-width
        max_field_decr = -(1 << (block_val_bits - 1))  # -ve number
        max_field_incr = (1 << (block_val_bits - 1)) - 1  # +ve number
        current_field_width = 0

        i = 0
        while i < expected_values:
            # Adjust the current field width to the target field width
            delta_field_width = encoded_bits.read_signed_int(block_val_bits)
            current_field_width += delta_field_width
            while delta_field_width == max_field_decr or delta_field_width == max_field_incr:
                delta_field_width = encoded_bits.read_signed_int(
                    block_val_bits)
                current_field_width += delta_field_width

            # Read in the run length
            run_length = encoded_bits.read_int(block_len_bits)

            # Read in the data bits for the run
            for j in range(i, i + run_length):
                decoded_symbols.append(encoded_bits.read_signed_int(
                    current_field_width) + mean_value)

            # Advance to the end of the run
            i += run_length
        logger.debug("finished variable length debug")
    if encoded_bits.position != total_bits or len(decoded_symbols) != expected_values:
        logger.error(
            f"{encoded_bits.position=} {total_bits=} {len(decoded_symbols)=} {expected_values=}")
        # raise ValueError("BitlengthCodec2 didn't consume all bits!")

    return decoded_symbols
