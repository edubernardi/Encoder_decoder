import math
import numpy as np
import sys
import golomb
import unary
import elias_gamma
import fibonacci
import delta


def calculate(data):
    bits = np.ndarray(len(data) * 8 * 2, int)
    data = np.unpackbits(data)
    i = 0
    while i < len(bits):
        if i < len(data):
            bits[i] = data[i]
        else:
            bits[i] = 0
        i += 1

    crc_8 = [1, 0, 0, 0, 0, 0, 1, 1, 1]

    end_loop = False
    while not end_loop:
        i = 0
        found_msb = -1
        while i < len(bits):
            if bits[i] == 1 and found_msb == -1:
                found_msb = i
                break
            i += 1

        if found_msb + len(crc_8) > len(bits):
            end_loop = True
            break

        i = found_msb
        while i - found_msb < len(crc_8):
            if bits[i] == crc_8[i - found_msb]:  # xor
                bits[i] = 0
            else:
                bits[i] = 1
            i += 1
    return int(np.packbits(bits[len(bits) - 8: len(bits)]))
