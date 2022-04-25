import math
import numpy as np
import sys
import util
import golomb
import unary
import elias_gamma
import fibonacci
import delta
import time
import os

def app_help():
    print("Usage:  encoder.py [encode] [input file name] [output file name] [method]")
    print("\tor\n\tencoder.py [decode] [input file name] [output file name]")
    print("Encoding methods supported:\n1•Golomb\n2•Elias-Gamma\n3•Fibonacci\n4•Unary\n5•Delta")


if len(sys.argv) >= 4:
    function = sys.argv[1]
    input_file = sys.argv[2]
    output_file_name = sys.argv[3]

    if function.lower() == "encode":
        output_file_name += ".cod"
        if len(sys.argv) == 5:
            method = sys.argv[4]
            current_time = " - Execution time: " + str(time.process_time()) + "s"
            if method.lower() == "golomb" or method.lower() == "1":
                util.write_to_file(input_file, output_file_name, 1)
            elif method.lower() == "elias-gamma" or method.lower() == "elias gamma" or method.lower() == "2":
                print("Started encoding", input_file, "into", output_file_name, "using Elias-Gamma method" + current_time)
                util.write_to_file(input_file, output_file_name, 2)
            elif method.lower() == "fibonacci" or method.lower() == "3":
                print("Started encoding", input_file, "into", output_file_name, "using Fibonacci method" + current_time)
                util.write_to_file(input_file, output_file_name, 3)
            elif method.lower() == "unary" or method.lower() == "4":
                print("Started encoding", input_file, "into", output_file_name, "using Unary method" + current_time)
                util.write_to_file(input_file, output_file_name, 4)
            elif method.lower() == "delta" or method.lower() == "5":
                print("Started encoding", input_file, "into", output_file_name, "using Delta method" + current_time)
                util.write_to_file(input_file, output_file_name, 5)
            #ecc
            print("Encoding finished" + " - Execution time: " + str(time.process_time()) + "s")
            print("Size change (compressed file size / input file size): " +
                  "{:.2f}".format(os.stat(output_file_name).st_size / os.stat(input_file).st_size))
            print("Generating noise control file: " + sys.argv[3] + ".ecc")
            util.encode_noise_control(output_file_name, sys.argv[3] + ".ecc")
            print("Noise control file created: " + sys.argv[3] + ".ecc" + " - Execution time: " + str(time.process_time()) + "s")
        else:
            app_help()
    elif function.lower() == "decode":
        if input_file.count(".") < 1 or (input_file.split('.')[len(input_file.split('.')) - 1] != "ecc" and input_file.split('.')[len(input_file.split('.')) - 1] != "cod"):
            print("Please provide a file with the .ecc extension as input")
        else:
            if input_file.split('.')[len(input_file.split('.')) - 1] == "cod":
                has_ecc = False
            else:
                has_ecc = True
            print("Started decoding", input_file, "into", output_file_name + " - Execution time: " + str(time.process_time()) + "s")
            if has_ecc:
                util.decode_noise_control(input_file, input_file.split('.')[0] + ".cod")
                print("Error correction completed" + " - Execution time: " + str(time.process_time()) + "s")
                input_file = input_file.split('.')[0] + ".cod"
            input_file = open(input_file, "rb")
            is_text_file = input_file.read(1)
            method = input_file.read(1)
            divisor = int.from_bytes(input_file.read(1), "big")
            if len(method) > 0:
                print("Starting decoder - Execution time: " + str(time.process_time()) + "s")
                if int.from_bytes(method, "big") == 1:
                    output_file = open(output_file_name, "wb")
                    print("Detected Golomb method with divisor", divisor)
                    golomb.decode(input_file, output_file, divisor, is_text_file)
                elif int.from_bytes(method, "big") == 2:
                    output_file = open(output_file_name, "wb")
                    print("Detected Elias-Gamma method")
                    elias_gamma.decode(input_file, output_file, is_text_file)
                elif int.from_bytes(method, "big") == 3:
                    output_file = open(output_file_name, "wb")
                    print("Detected Fibonacci method")
                    fibonacci.decode(input_file, output_file, is_text_file)
                elif int.from_bytes(method, "big") == 4:
                    output_file = open(output_file_name, "wb")
                    print("Detected Unary method")
                    unary.decode(input_file, output_file, is_text_file)
                elif int.from_bytes(method, "big") == 5:
                    output_file = open(output_file_name, "wb")
                    print("Detected Delta method")
                    delta.decode(input_file, output_file, is_text_file)
                print("Decoder finished - Execution time: " + str(time.process_time()) + "s")
    else:
        app_help()
else:
    app_help()
