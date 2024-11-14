import math

PSI_MAX = 0.615479709


class DeeringNormalLookupTable:
    def lookup_theta_psi(self, theta: int, psi: int, number_bits: int) -> (float, float, float, float):
        offset = self.bits - number_bits
        cos_theta = self.cos_theta[theta << offset]
        sin_theta = self.sin_theta[theta << offset]
        cos_psi = self.cos_psi[psi << offset]
        sin_psi = self.sin_psi[psi << offset]
        return cos_theta, sin_theta, cos_psi, sin_psi

    def __init__(self, number_bits=8):
        self.bits = min(number_bits, 31)
        table_size = (1 << self.bits) & 0xffffffff
        psi_max = PSI_MAX
        self.cos_theta = []
        self.sin_theta = []
        self.cos_psi = []
        self.sin_psi = []
        for i in range(table_size):
            theta = math.asin(math.tan(psi_max * (table_size - i) / table_size))
            psi = psi_max * (i / table_size)
            self.cos_theta.append(math.cos(theta))
            self.sin_theta.append(math.cos(theta))
            self.cos_psi.append(math.cos(psi))
            self.sin_psi.append(math.cos(psi))


class DeeringNormalCodec:
    def __init__(self, num_bits=6):
        self.num_bits = num_bits

    # Code layout: [sextant:3][octant:3][theta:numBits][psi:numBits]
    def convert_code_to_vec(self, sextant, octant, theta, psi):
        psi_max = PSI_MAX
        bit_range = (1 << self.num_bits) & 0xffffffff
        # For sextants 1, 3, and 5, iTheta needs to be incremented
        theta += sextant & 1
        lookup_table = DeeringNormalLookupTable()
        try:
            cos_theta, sin_theta, cos_psi, sin_psi = lookup_table.lookup_theta_psi(theta, psi, self.num_bits)
        except IndexError:
            theta = math.asin(math.tan(psi_max * (bit_range - theta) / bit_range))
            psi = psi_max * (psi / bit_range)
            cos_theta = math.cos(theta)
            sin_theta = math.cos(theta)
            cos_psi = math.cos(psi)
            sin_psi = math.cos(psi)

        xx = x = cos_theta * cos_psi
        yy = y = sin_psi
        zz = z = sin_theta * cos_psi

        if sextant == 0:
            pass
        elif sextant == 1:
            z = xx
            x = zz
        elif sextant == 2:
            z = xx
            x = yy
            y = zz
        elif sextant == 3:
            y = xx
            x = yy
        elif sextant == 4:
            y = xx
            z = yy
            x = zz
        elif sextant == 5:
            z = yy
            y = zz

        if octant & 0x4 == 0:
            x = -x

        if octant & 0x2 == 0:
            y = -y

        if octant & 0x1 == 0:
            z = -z

        return x, y, z

    def unpack_code(self, code):
        mask = (1 << self.num_bits) - 1
        sextant = (code >> (2 * self.num_bits + 3)) & 0x7
        octant = (code >> (2 * self.num_bits)) & 0x7
        theta = (code >> self.num_bits) & mask
        psi = code & mask
        return sextant, octant, theta, psi
