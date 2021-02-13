# pyADPCM
Python Implementation of the Adaptive Differential Pulse Code Modulation


## Dependencies
```
numpy
wavio
```

## How to use

```
from adpcm import ADPCM
import numpy as np

adpcm = ADPCM()

data = np.rand(1024, 1)

encoded = adpcm.encode(data)

decoded = adpcm.decode(encoded)
```
