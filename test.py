from adpcm import ADPCM
import wavio

wavObj = wavio.read('original.wav')

samples = wavObj.data

adpcm = ADPCM()

encoded = adpcm.encode(samples)

print(encoded)

decoded = adpcm.decode(encoded)

wavio.write('comdecom.wav', decoded, wavObj.rate, sampwidth=wavObj.sampwidth)