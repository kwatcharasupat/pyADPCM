import csv
import wavio
import numpy as np


def hexstr_to_signed_int16(hexstr):
    value = int(hexstr, 16)

    if value & 0x8000:
        value -= 0xFFFF
    return value


def csv_to_data(csv_file, bit_depth_idx=1, data_idx=7, base=16, dtype=np.int16):
    """ Convert raw CSV file into a numpy array of data """
    rawHex = []
    with open(csv_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=["x", "y"])

        for r in reader:
            rawHex.append(r["y"])

    bit_depth = int(rawHex[bit_depth_idx].strip("bit"))

    if np.issubdtype(dtype, np.signedinteger):
        func = hexstr_to_signed_int16
    elif np.issubdtype(dtype, np.unsignedinteger):
        func = lambda x: int(x, 16)
    else:
        raise AttributeError

    y = np.fromiter(map(func, rawHex[data_idx:]), dtype=dtype)

    return y, bit_depth


def generate_wav(csv_file, wav_file, fs=4000):
    """ Generate a mono-channel wave file at `wav_file` from `csv_file` """
    y, bit_depth = csv_to_data(csv_file)
    y = y / np.max(np.abs(y))
    wavio.write(wav_file, y, fs, sampwidth=bit_depth // 8)

