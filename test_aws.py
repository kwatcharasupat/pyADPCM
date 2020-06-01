import csv
from adpcm import ADPCM
import wavio
import numpy as np

csv_file = "20200601_SampleDataCompressedDataFromDevicecsv.csv"

n_seg = 10
encoded_seq = {}
with open(csv_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for r in reader:
        encoded_seq[r["sequence"]] = r["audio_data"]

rawhex = []

n = 2
for seq in sorted(encoded_seq):
    rawhex += [encoded_seq[seq][i : i + n] for i in range(0, len(encoded_seq[seq]), n)]

encoded = np.fromiter(map(lambda x: int(x, 16), rawhex), dtype=np.uint8)
decoded = ADPCM().decode(encoded)

wavio.write("aws_decoded.wav", decoded, 4000)

