import math
import numpy as np
import sys
import util
import golomb


def app_help():
    print("Usage:  encoder.py [encode] [input file name] [output file name] [method]")
    print("\tor\n\tencoder.py [decode] [input file name] [output file name]")
    print("Encoding methods supported:\n1•Golomb\n2•Elias-Gamma\n3•Fibonacci\n4•Unary\n5•Delta")


if len(sys.argv) == 5:
    function = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    method = sys.argv[4]

    if function.lower() == "encode":
        if method.lower() == "golomb" or function.lower() == "1":
            k = int(input("Divisor for Golomb function (must be a power of 2):"))
            if k % 2 != 0:
                print("Invalid value for divisor")
            else:
                f = open(input_file, "rb")
                w = open(output_file, "wb")
                w.write(bytes([1]))
                w.write(bytes([k]))
                end_of_file = False
                buffer = np.empty(8000, int)
                j = 0
                buffer_size = 0
                while not end_of_file:
                    loaded_byte = f.read(1)
                    if len(loaded_byte) < 1:
                        end_of_file = True
                    else:
                        codeword = golomb.encode(loaded_byte, k)
                        buffer_size += len(codeword)
                        for number in codeword:
                            buffer[j] = number
                            j += 1
                    if end_of_file or buffer_size % 8 == 0:
                        codewords = bytearray(np.packbits(buffer[0: j]))
                        for byte in codewords:
                            w.write(bytes([byte]))
                        buffer = np.empty(8000, int)
                        buffer_size = 0
                        j = 0
                f.close()
                w.close()
        elif method.lower() == "elias-gamma" or method.lower() == "elias gamma" or function.lower() == "2":
            print("Elias gama ainda não implmentado")
        elif method.lower() == "fibonacci" or function.lower() == "3":
            print("Fibonacci gama ainda não implmentado")
        elif method.lower() == "unary" or function.lower() == "4":
            print("Unary gama ainda não implmentado")
        elif method.lower() == "delta" or function.lower() == "5":
            print("Delta gama ainda não implmentado")
    elif function.lower() == "decode":
        input_file = open(input_file, "rb")
        method = input_file.read(1)
        if len(method) > 0:
            if int.from_bytes(method, "big") == 1:
                divisor = int.from_bytes(input_file.read(1), "big")
                output_file = open(output_file, "wb")
                golomb.decode(input_file, output_file, divisor)
            elif int.from_bytes(method, "big") == 2:
                print("Elias gama ainda não implmentado")
            elif int.from_bytes(method, "big") == 3:
                print("Fibonacci gama ainda não implmentado")
            elif int.from_bytes(method, "big") == 4:
                print("Unary gama ainda não implmentado")
            elif int.from_bytes(method, "big") == 5:
                print("Delta gama ainda não implmentado")
else:
    app_help()
