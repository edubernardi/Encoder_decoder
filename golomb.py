import math
import numpy as np
import sys
import util


def encode(character, divisor):
    digits = math.log(divisor, 2)
    prefix = int(ord(character) / divisor)
    sufix = int(ord(character) % divisor)
    i = 0
    j = 0
    codeword = np.empty(128, int)
    while i < prefix:
        codeword[j] = 0
        j += 1
        i += 1
    codeword[j] = 1
    j += 1
    sufix = util.int_to_bitarray(sufix)

    if sufix.size < digits:
        i = 0
        while i < digits - sufix.size:
            codeword[j] = 0
            j += 1
            i += 1

    for number in sufix:
        codeword[j] = number
        j += 1
    # print(j)
    return codeword[0: j]


def decode(coded, result, divisor):
    end_of_file = False
    reading_prefix = True
    prefix = 0
    sufix = 0
    sufix_digits_read = 0
    while not end_of_file:
        j = 0
        loaded_byte = coded.read(1)
        if len(loaded_byte) < 1:
            end_of_file = True
        else:
            buffer = loaded_byte
            j += 1

            digits = math.log(divisor, 2)
            bits = np.unpackbits(bytearray(buffer))
            decoded = bytearray()
            for bit in bits:
                if reading_prefix:
                    if bit == 1:
                        reading_prefix = False
                    else:
                        prefix += 1
                else:
                    sufix_digits_read += 1
                    sufix += bit * (2 ** (digits - sufix_digits_read))
                    if sufix_digits_read >= digits:
                        decoded.append(int(prefix * divisor + sufix))
                        reading_prefix = True
                        for byte in decoded:
                            print(byte)
                            result.write(bytes([byte]))
                        prefix = 0
                        sufix = 0
                        sufix_digits_read = 0
