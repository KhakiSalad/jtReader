def decode_arithmetic(codec_driver):
    0x0000
    low = 0x0000
    high = 0xffff
    oob_counter = 0
    decoded_symbols = []
    symbol_count = codec_driver.value_count
    out_of_band_values = codec_driver.out_of_band_values
    results = codec_driver.get_next_code_text()
    if results is None:
        raise RuntimeError("ERROR: No more code bytes available!")
    else:
        code_text, n_bits = results

    code = (code_text >> 16) & 0xffff
    code_text = (code_text << 16) & 0xffffffff
    n_bits = 16
    acc_counts, entry_by_acc_count = codec_driver.int_32_probability_contexts.accumulated_probability_counts()

    for i in range(symbol_count):
        rescaled_code = ((((code - low) + 1) * acc_counts - 1) // (((high - low) & 0xffff) + 1))
        # find interval for scales symbol and retrieve original value
        key = list(filter(lambda k: k > rescaled_code - 1, entry_by_acc_count.keys()))
        if len(key) == 0:
            key = max(entry_by_acc_count.keys())
        else:
            key = min(key)
        val = entry_by_acc_count[key]
        cntx_entry = codec_driver.int_32_probability_contexts.table[val]
        if cntx_entry.symbol == -2:
            dec_sym = out_of_band_values[oob_counter]
            oob_counter += 1
        else:
            dec_sym = cntx_entry.value
        decoded_symbols.append(dec_sym)

        # remove symbol from stream
        # first, the range is expanded to account for the symbol removal
        symbol_range_new = [0, 0, 0]
        symbol_range_new[0] = (key + 1 - cntx_entry.count)
        symbol_range_new[1] = key + 1
        symbol_range_new[2] = symbol_count

        symbol_range = high - low + 1
        high = (low + ((symbol_range * symbol_range_new[1]) // symbol_range_new[2] - 1)) & 0xfffff
        low = (low + ((symbol_range * symbol_range_new[0]) // symbol_range_new[2])) & 0xfffff

        # next, any possible bits are shipped out
        while True:
            if (((~(high ^ low)) & 0xffff) & 0x8000) != 0:
                # If the most signif digits match, the bits will be shifted out.
                pass
            elif (low & 0x4000) > 0 and (high & 0x4000) == 0:
                # Underflow is threatening, shift out 2nd most signif digit.
                code ^= 0x4000
                low &= 0x3fff
                high |= 0x4000
                high &= 0xffff
            else:
                # Nothing can be shifted out, so break.
                break
            low = (low << 1) & 0xffff
            high = (high << 1) & 0xffff
            high |= 1
            code = (code << 1) & 0xffff

            if n_bits == 0:
                results = codec_driver.get_next_code_text()
                code_text = results[0]
                n_bits = results[1]
            code = code | (code_text >> 31)
            code_text = (code_text << 1) & 0xffffffff
            n_bits -= 1

    return decoded_symbols
