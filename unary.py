import math
import numpy as np
import sys
import util


def encode(character):
    length = int(ord(character))
    codeword = np.empty(length + 1, int)
    i = 0
    while i < length:
        codeword[i] = 0
        i += 1
    codeword[length] = 1
    return codeword

def decode(encoded_file, decoded_file):
    end_of_file = False
    value = 0
    while not end_of_file:
        buffer = encoded_file.read(1)
        if len(buffer) < 1:
            end_of_file = True
        bits = np.unpackbits(bytearray(buffer))
        for bit in bits:
            if bit == 0:
                value += 1
            elif bit == 1:
                decoded_file.write(bytes([value]))
                value = 0