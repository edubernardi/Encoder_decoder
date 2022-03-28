import math
import numpy as np
import sys
import util
import golomb
import unary
import elias_gamma
import fibonacci
import delta


def app_help():
    print("Usage:  encoder.py [encode] [input file name] [output file name] [method]")
    print("\tor\n\tencoder.py [decode] [input file name] [output file name]")
    print("Encoding methods supported:\n1•Golomb\n2•Elias-Gamma\n3•Fibonacci\n4•Unary\n5•Delta")


if len(sys.argv) >= 4:
    function = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]


    if function.lower() == "encode":
        if len(sys.argv) == 5:
            method = sys.argv[4]
            if method.lower() == "golomb" or function.lower() == "1":
                util.write_to_file(input_file, output_file, 1)
            elif method.lower() == "elias-gamma" or method.lower() == "elias gamma" or function.lower() == "2":
                util.write_to_file(input_file, output_file, 2)
            elif method.lower() == "fibonacci" or function.lower() == "3":
                util.write_to_file(input_file, output_file, 3)
            elif method.lower() == "unary" or function.lower() == "4":
                util.write_to_file(input_file, output_file, 4)
            elif method.lower() == "delta" or function.lower() == "5":
                util.write_to_file(input_file, output_file, 5)
        else:
            app_help()
    elif function.lower() == "decode":
        print("Started decoding", input_file, "into", output_file)
        input_file = open(input_file, "rb")
        method = input_file.read(1)
        if len(method) > 0:
            if int.from_bytes(method, "big") == 1:
                divisor = int.from_bytes(input_file.read(1), "big")
                output_file = open(output_file, "wb")
                print("Detected Golomb method with divisor", divisor)
                golomb.decode(input_file, output_file, divisor)
            elif int.from_bytes(method, "big") == 2:
                output_file = open(output_file, "wb")
                print("Detected Elias-Gamma method")
                elias_gamma.decode(input_file, output_file)
            elif int.from_bytes(method, "big") == 3:
                output_file = open(output_file, "wb")
                print("Detected Fibonacci method")
                fibonacci.decode(input_file, output_file)
            elif int.from_bytes(method, "big") == 4:
                output_file = open(output_file, "wb")
                print("Detected Unary method")
                unary.decode(input_file, output_file)
            elif int.from_bytes(method, "big") == 5:
                output_file = open(output_file, "wb")
                print("Detected Delta method")
                delta.decode(input_file, output_file)
    else:
        app_help()
else:
    app_help()
