import math
import numpy as np
import sys
import golomb
import unary
import elias_gamma
import fibonacci
import delta

def int_to_bitarray(i):
    bitarray = np.empty(32, int)
    j = 0
    while i > 0:
        remainder = i % 2
        bitarray[j] = int(remainder)
        i = int(i / 2)
        j += 1
    bitarray = np.flipud(bitarray[0: j])
    return bitarray

def write_to_file(input_file, output_file, method):
    f = open(input_file, "rb")
    w = open(output_file, "wb")
    is_text_file = is_text(input_file)
    w.write(bytes([is_text_file]))
    w.write(bytes([method]))
    if method == 1:
        k = int(input("Divisor for Golomb function (must be a power of 2):"))
        if k % 2 != 0:
            print("Invalid value for divisor, setting divisor to default value (4)")
            k = 4
        else:
            w.write(bytes([k]))
            print("Started encoding", input_file, "into", output_file, "using Golomb method on with divisor", k)
    if method == 5:
        loaded_byte = f.read(1)

        if len(loaded_byte) < 1:
            end_of_file = True
        else:
            if is_text_file and (96 < int(ord(loaded_byte)) < 123):
                loaded_byte = bytes([int(ord(loaded_byte)) - 95])
            w.write(loaded_byte)
            last_byte = loaded_byte
    end_of_file = False
    buffer = np.empty(800000, int)
    j = 0
    buffer_size = 0
    while not end_of_file:
        loaded_byte = f.read(1)
        if len(loaded_byte) < 1:
            end_of_file = True
        else:
            if is_text_file:
                if 96 < int(ord(loaded_byte)) < 123:
                    loaded_byte = bytes([int(ord(loaded_byte)) - 95])
                elif 1 < int(ord(loaded_byte)) < 28:
                    loaded_byte = bytes([int(ord(loaded_byte)) + 95])
            if method == 1:
                codeword = golomb.encode(loaded_byte, k)
            elif method == 2:
                codeword = elias_gamma.encode(loaded_byte)
            elif method == 3:
                codeword = fibonacci.encode(loaded_byte)
            elif method == 4:
                codeword = unary.encode(loaded_byte)
            elif method == 5:
                codeword = delta.encode(loaded_byte, last_byte)
                last_byte = loaded_byte
            buffer_size += len(codeword)
            for number in codeword:
                buffer[j] = number
                j += 1
        if end_of_file or buffer_size % 8 == 0:
            codewords = bytearray(np.packbits(buffer[0: j]))
            for byte in codewords:
                w.write(bytes([byte]))
            buffer = np.empty(800000, int)
            buffer_size = 0
            j = 0
    f.close()
    w.close()


def is_text(input_file):
    file = open(input_file, "rb")
    end_of_file = False
    sum = 0
    count = 0
    while not end_of_file:
        character = file.read(1)
        if len(character) < 1:
            end_of_file = True
        else:
            sum += int(ord(character))
            count += 1
    average = sum / count
    file.close()
    return average > 65

def reduce_text_size(character):
    if 96 < character < 123:
        character -= 95
    elif 1 < character < 28:
        character += 95
    return character