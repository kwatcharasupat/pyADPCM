from adpcm import ADPCM
from csv_to_wav import csv_to_data, generate_wav
import numpy as np
import wavio

tests = ["test" + str(i + 1) for i in range(4)]

for test in tests:
    wavobj = wavio.read(test + ".wav")

    adpcm = ADPCM()
    encoded = adpcm.encode(wavobj.data)
    decoded = adpcm.decode(encoded)

    wavio.write(test + "_reconstructed.wav", decoded, 4000)
