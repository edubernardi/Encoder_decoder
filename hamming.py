import numpy as np

def encode(data):
    data = np.unpackbits(bytearray(data))
    codewords = [np.ndarray(7, int), np.ndarray(7, int)]
    i = 0
    while i < len(data):
        if i < 4:
            codewords[0][i] = data[i]
        else:
            codewords[1][i - 4] = data[i]
        i += 1

    i = 0
    while i < 2:
        codewords[i][4] = (codewords[i][0] + codewords[i][1] + codewords[i][2]) % 2
        codewords[i][5] = (codewords[i][1] + codewords[i][2] + codewords[i][3]) % 2
        codewords[i][6] = (codewords[i][0] + codewords[i][2] + codewords[i][3]) % 2
        i += 1

    result = np.ndarray(14, int)
    i = 0
    while i < len(result):
        if i < 7:
            result[i] = codewords[0][i]
        else:
            result[i] = codewords[1][i - 7]
        i += 1

    return result

def decode(data):
    bits = np.unpackbits(data)
    if len(bits) % 7 != 0: # removendo bits filler do fim do byte
        temp = bits
        bits = np.ndarray(int(len(temp)/7) * 7, int)
        i = 0
        while i < len(bits):
            bits[i] = temp[i]
            i += 1
    codewords = []
    i = 0
    while i < len(bits) / 7:
        codewords.append(np.ndarray(7, int))
        j = 0
        while j < 7:
            codewords[i][j] = bits[i * 7 + j]
            j += 1
        i += 1

    i = 0
    while i < len(bits) / 7:
        flags = [False] * 3
        if codewords[i][4] != (codewords[i][0] + codewords[i][1] + codewords[i][2]) % 2:
            flags[0] = True
            print("Hamming error")
        if codewords[i][5] != (codewords[i][1] + codewords[i][2] + codewords[i][3]) % 2:
            flags[1] = True
            print("Hamming error")
        if codewords[i][6] != (codewords[i][0] + codewords[i][2] + codewords[i][3]) % 2:
            flags[2] = True
            print("Hamming error")
        if flags[0]:
            if flags[1]:
                if flags[2]:
                    codewords[i][2] = (codewords[i][2] + 1) % 2
                else:
                    codewords[i][1] = (codewords[i][2] + 1) % 2
            else:
                codewords[i][0] = (codewords[i][2] + 1) % 2
        elif flags[1] or flags[2]:
            codewords[i][3] = (codewords[i][2] + 1) % 2
        i += 1

    result = np.ndarray(int((4 * len(bits))/7), int)
    i = 0
    while i < len(bits) / 7:
        j = 0
        while j < 4:
            result[i * 4 + j] = codewords[i][j]
            j += 1
        i += 1
    return result
