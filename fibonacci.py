import math
import numpy as np
import sys
import util

def encode(character):
    value = int(ord(character)) + 1 # somando 1 pois nao codifica o 0
    fibonacci_numbers = [1, 2]
    while fibonacci_numbers[len(fibonacci_numbers) - 1] < value:
        fibonacci_numbers.append(fibonacci_numbers[len(fibonacci_numbers) - 1] +
                                 fibonacci_numbers[len(fibonacci_numbers) - 2])
    i = len(fibonacci_numbers) - 2
    codeword = np.empty(len(fibonacci_numbers), int)
    codeword[i + 1] = 1
    while i >= 0:
        if fibonacci_numbers[i] <= value:
            value -= fibonacci_numbers[i]
            codeword[i] = 1
            if i > 0:
                codeword[i - 1] = 0
            i -= 1
        else:
            codeword[i] = 0
        i -= 1
    return codeword

def decode(encoded_file, decoded_file, is_text_file):
    value = 0
    fibonacci_numbers = [1, 2]
    last_bit = 0
    end_of_file = False
    while not end_of_file:
        buffer = encoded_file.read(1)
        if len(buffer) < 1:
            end_of_file = True
        bits = np.unpackbits(bytearray(buffer))
        for bit in bits:
            if bit == 1 and last_bit == 1:
                if is_text_file:
                    value = util.reduce_text_size(value)
                decoded_file.write(bytes([value - 1])) # subtraindo 1 pois nao codifica o 0
                last_bit = 0
                fibonacci_numbers = [1, 2]
                value = 0
            else:
                last_bit = bit
                value += bit * (fibonacci_numbers[len(fibonacci_numbers) - 2])
                fibonacci_numbers.append(fibonacci_numbers[len(fibonacci_numbers) - 1] +
                                         fibonacci_numbers[len(fibonacci_numbers) - 2])

