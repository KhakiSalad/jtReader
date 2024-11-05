from dataclasses import dataclass

from jt_reader.util.bitBuffer import BitBuffer


@dataclass
class CntxEntry:
    """
    8.1.2.1.1 Int32 Probability Context Table Entry Mk. 2
    """
    symbol: int
    count: int
    value: int

    @classmethod
    def from_bits(cls,
                  bits,
                  n_symbol_bits,
                  n_occurrencce_count_bits,
                  n_value_bits,
                  minimum_value):
        symbol = bits.read_int(n_symbol_bits) - 2
        count = bits.read_int(n_occurrencce_count_bits)
        value = bits.read_int(n_value_bits) + minimum_value
        return CntxEntry(symbol, count, value)


@dataclass
class ProbabilityContext:
    total_count: int
    num_entries: int
    table: list[CntxEntry]

    @classmethod
    def from_bytes(cls, e_bytes):
        bit_buffer = BitBuffer(e_bytes, endianness="big")
        bit_buffer.position = e_bytes.offset << 3

        probability_context_table_entry_count = bit_buffer.read_int(16)
        num_symbol_bits = bit_buffer.read_int(6)
        num_occurrence_count_bits = bit_buffer.read_int(6)
        number_value_bits = bit_buffer.read_int(6)
        min_value = bit_buffer.read_int(32)
        probability_context_table_entries = []
        for i in range(probability_context_table_entry_count):
            probability_context_table_entries.append(CntxEntry.from_bits(
                bit_buffer,
                num_symbol_bits,
                num_occurrence_count_bits,
                number_value_bits,
                min_value
            ))
        num_alignment_bits = bit_buffer.position % 8
        if num_alignment_bits > 0:
            bit_buffer.read_int(8 - num_alignment_bits)
            assert (bit_buffer.position % 8 == 0)
        read_bytes = ((bit_buffer.position >> 3) - e_bytes.offset)
        e_bytes.offset += read_bytes
        return ProbabilityContext(0, probability_context_table_entry_count, probability_context_table_entries)

    def accumulated_probability_counts(self):
        acc = 0
        entry_by_acc_count = {}
        for i, r in enumerate(self.table):
            acc += r.count
            entry_by_acc_count[acc - 1] = i
        return acc, entry_by_acc_count

    @classmethod
    def entry_and_symbol_range_by_rescaled_code(cls, rescaled_code, entry_by_acc_count):
        val = entry_by_acc_count[rescaled_code - 1]
