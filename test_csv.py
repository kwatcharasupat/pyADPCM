from adpcm import ADPCM
from csv_to_wav import csv_to_data, generate_wav
import numpy as np
import wavio

generate_wav('originaldata.csv', 'original.wav')

encoded, _ = csv_to_data('encodeddata.csv', dtype=np.uint8)
adpcm = ADPCM()
decoded = adpcm.decode(encoded)
wavio.write('decoded.wav', decoded, 4000)

