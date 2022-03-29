import math
import numpy as np
import sys
import util

def encode(character, last_character):
    value_char = int(ord(character))
    value_last = int(ord(last_character))
    delta = value_last - value_char
    codeword = np.empty(10, int)
    if delta == 0:
        codeword = np.ndarray(0)
    else:
        codeword[0] = 1
        if delta > 0:
            delta = util.int_to_bitarray(delta)
            i = 1
            while i < (10 - len(delta)):
                codeword[i] = 0
                i += 1

            while i < 10:
                codeword[i] = delta[i - (10 - len(delta))]
                i += 1
        elif delta < 0:
            delta = util.int_to_bitarray(- delta)
            codeword[1] = 1 # assinando o valor pois é negativo
            i = 2
            while i < (10 - len(delta)):
                codeword[i] = 0
                i += 1

            while i < 10:
                codeword[i] = delta[i - (10 - len(delta))]
                i += 1
    return codeword


def decode(encoded_file, decoded_file, is_text):
    delta = 0
    last_value = 0
    digits_read = 0
    positive = True
    end_of_file = False
    stop_bit = False
    buffer = encoded_file.read(1)
    if len(buffer) < 1:
        end_of_file = True
    else:
        last_value = int(ord(buffer))
        decoded_file.write(bytes([last_value]))
    while not end_of_file:
        buffer = encoded_file.read(1)
        if len(buffer) < 1:
            end_of_file = True
        bits = np.unpackbits(bytearray(buffer))
        for bit in bits:
            if not stop_bit:
                if bit == 0:
                    decoded_file.write(bytes([last_value]))
                if bit == 1:
                    stop_bit = True
            else:
                if digits_read == 0:
                    if bit == 0:
                        positive = True
                    else:
                        positive = False
                    digits_read += 1
                else:
                    delta += bit * (2 ** (8 - digits_read))
                    digits_read += 1
                    if digits_read == 9:
                        if positive:
                            value = last_value - delta
                        else:
                            value = last_value + delta
                        if is_text:
                            decoded_file.write(bytes([util.reduce_text_size(value)]))
                        else:
                            decoded_file.write(bytes([value]))
                        last_value = value
                        delta = 0
                        digits_read = 0
                        positive = True
                        stop_bit = False

