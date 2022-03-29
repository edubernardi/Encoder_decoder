import math
import numpy as np
import sys
import util

def encode(character):
    value = int(ord(character)) + 1 #somando um pois nao codifica 0
    i = 0
    while 2 ** i <= value:
        i += 1
    i -= 1
    codeword = np.empty((i * 2) + 1, int)
    j = 0
    while j < i:
        codeword[j] = 0
        j += 1
    codeword[j] = 1
    j += 1
    remainder = util.int_to_bitarray(value % (2 ** i))

    difference = j + i - len(remainder)
    while j < difference:  #  appending 0s so that the suffix is same size as suffix
        codeword[j] = 0
        j += 1

    for number in remainder:
        codeword[j] = number
        j += 1
    return codeword


def decode(encoded_file, decoded_file, is_text_file):
    end_of_file = False
    prefix = 0
    suffix = 0
    suffix_digits_read = 0
    found_stop_bit = False
    while not end_of_file:
        buffer = encoded_file.read(1)
        if len(buffer) < 1:
            end_of_file = True
        bits = np.unpackbits(bytearray(buffer))
        for bit in bits:
            if not found_stop_bit:
                if bit == 0:
                    prefix += 1
                elif bit == 1:
                    found_stop_bit = True
            else:
                suffix_digits_read += 1
                suffix += bit * (2 ** (prefix - suffix_digits_read))
                if suffix_digits_read >= prefix:
                    decoded = bytearray()
                    decoded.append(int(2 ** prefix + suffix - 1)) # subtraindo 1 pois nao codifica 0
                    found_stop_bit = False
                    for byte in decoded:
                        if is_text_file:
                            byte = util.reduce_text_size(byte)
                        decoded_file.write(bytes([byte]))
                    prefix = 0
                    suffix = 0
                    suffix_digits_read = 0