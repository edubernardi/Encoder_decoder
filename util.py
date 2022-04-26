import math
import numpy as np
import sys
import golomb
import unary
import elias_gamma
import fibonacci
import delta
import crc
import hamming
import time


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
        if math.log(k, 2) % 1 != 0:
            print("Invalid value for divisor, setting divisor to default value (4)")
            k = 4
        else:
            w.write(bytes([k]))
            print("Started encoding", input_file, "into", output_file, "using Golomb method on with divisor", k)
    else:
        w.write(bytes([4]))
    if method == 5:
        loaded_byte = f.read(1)
        last_byte = loaded_byte

        if len(loaded_byte) < 1:
            end_of_file = True
        else:
            if is_text_file:
                loaded_byte = bytes([reduce_text_size(int(ord(loaded_byte)))])
            last_byte = loaded_byte
            w.write(loaded_byte)

    end_of_file = False
    buffer = np.empty(800000, int)
    j = 0
    while not end_of_file:
        loaded_byte = f.read(1)
        if len(loaded_byte) < 1:
            end_of_file = True
        else:
            if is_text_file:
                loaded_byte = bytes([reduce_text_size(int(ord(loaded_byte)))])
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
            for number in codeword:
                buffer[j] = number
                j += 1
        if end_of_file or j % 8 == 0:
            if method == 5:
                # no caso da encodificação delta, se existem bits faltando para completar um byte
                # é adicionado um stopbit 1, dessa forma os bits 0 não são considerados repetições
                # do último caractere
                if end_of_file and (j % 8) != 0:
                    buffer[j] = 1
                    j += 1
            codewords = bytearray(np.packbits(buffer[0: j]))
            for byte in codewords:
                w.write(bytes([byte]))
            buffer = np.empty(800000, int)
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
    if average > 65:
        return 1
    else:
        return 0


def reduce_text_size(character):
    if 96 < character < 123:
        character -= 95
    elif 1 < character < 28:
        character += 95
    return character


def encode_noise_control(input_file, output_file):
    f = open(input_file, "rb")
    w = open(output_file, "wb")

    # aplicando crc_8

    print("Encoding headers with crc-8" + " - Execution time: " + str(time.process_time()) + "s")
    i = 0
    headers = []
    end_of_file = False
    while i < 3 and not end_of_file:
        loaded_byte = f.read(1)
        if len(loaded_byte) < 1:
            end_of_file = True
        w.write(loaded_byte)
        headers.append(loaded_byte)
        i += 1
    i = 0
    while i < len(headers):
        w.write(bytes([crc.calculate(bytearray(headers[i]))]))
        i += 1

    # aplicando hamming

    print("Encoding data with Hamming" + " - Execution time: " + str(time.process_time()) + "s")
    buffer = np.empty(800000, int)
    j = 0
    while not end_of_file:
        loaded_byte = f.read(1)
        if len(loaded_byte) < 1:
            end_of_file = True
        if not end_of_file:
            codeword = hamming.encode(loaded_byte)
            for number in codeword:
                buffer[j] = number
                j += 1
        if end_of_file or j % 8 == 0:
            codewords = bytearray(np.packbits(buffer[0: j]))
            for byte in codewords:
                w.write(bytes([byte]))
            buffer = np.empty(800000, int)
            j = 0
    f.close()
    w.close()


def decode_noise_control(input_file, output_file):
    f = open(input_file, "rb")
    w = open(output_file, "wb")

    # verificando headers pelo crc_8
    print("Verifying headers" + " - Execution time: " + str(time.process_time()) + "s")
    i = 0
    headers = []
    end_of_file = False
    while i < 3 and not end_of_file:
        loaded_byte = f.read(1)
        if len(loaded_byte) < 1:
            end_of_file = True
        w.write(loaded_byte)
        headers.append(loaded_byte)
        i += 1

    verified_headers = True
    i = 0
    while i < len(headers):
        loaded_byte = f.read(1)
        if len(loaded_byte) < 1:
            end_of_file = True
        if int.from_bytes(loaded_byte, "big") != crc.calculate(bytearray(headers[i])):
            verified_headers = False
            print("Headers have been altered, stopping decoder")
            break
        i += 1

    # verficando hamming
    print("Verifying data" + " - Execution time: " + str(time.process_time()) + "s")
    buffer = np.empty(800000, int)
    j = 0
    while not end_of_file and verified_headers:
        loaded_bytes = bytearray(f.read(7))
        if len(loaded_bytes) < 7:
            end_of_file = True
        codeword = hamming.decode(loaded_bytes)
        for number in codeword:
            buffer[j] = number
            j += 1
        if end_of_file or j % 8 == 0:
            codewords = bytearray(np.packbits(buffer[0: j]))
            for byte in codewords:
                w.write(bytes([byte]))
            buffer = np.empty(800000, int)
            j = 0
    f.close()
    w.close()
