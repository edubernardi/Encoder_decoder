import math
import numpy as np
import sys
import util


def encode(character, divisor):
    digits = math.log(divisor, 2)
    prefix = int(ord(character) / divisor)
    suffix = int(ord(character) % divisor)
    i = 0
    j = 0
    codeword = np.empty(8000, int)
    while i < prefix:
        codeword[j] = 0
        j += 1
        i += 1
    codeword[j] = 1
    j += 1
    suffix = util.int_to_bitarray(suffix)

    if suffix.size < digits:
        i = 0
        while i < digits - suffix.size:
            codeword[j] = 0
            j += 1
            i += 1

    for number in suffix:
        codeword[j] = number
        j += 1
    return codeword[0: j]


def decode(encoded_file, decoded_file, divisor, is_text_file):
    end_of_file = False
    reading_prefix = True
    prefix = 0
    suffix = 0
    suffix_digits_read = 0
    while not end_of_file:
        j = 0
        loaded_byte = encoded_file.read(1)
        if len(loaded_byte) < 1:
            end_of_file = True
        else:
            buffer = loaded_byte
            j += 1
            digits = math.log(divisor, 2)
            bits = np.unpackbits(bytearray(buffer))
            #decoded = bytearray()
            for bit in bits:
                if reading_prefix:
                    if bit == 1:
                        reading_prefix = False
                    else:
                        prefix += 1
                else:
                    suffix_digits_read += 1
                    suffix += bit * (2 ** (digits - suffix_digits_read))
                    if suffix_digits_read >= digits:
                        decoded = bytearray() #isso aqui tava na linha 51, movi pois nao fazia sentido
                        decoded.append(int(prefix * divisor + suffix))
                        reading_prefix = True
                        for byte in decoded:
                            if is_text_file:
                                byte = util.reduce_text_size(byte)
                            decoded_file.write(bytes([byte]))
                        prefix = 0
                        suffix = 0
                        suffix_digits_read = 0
