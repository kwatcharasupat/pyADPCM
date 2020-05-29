import numpy as np
from typing import List


class ADPCMState:
    def __init__(self):
        super().__init__()
        self.prev_sample = 0
        self.prev_idx = 0


class ADPCM:
    def __init__(self):
        super().__init__()
        self.index_table = np.array(
            [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8,], dtype=np.int16
        )
        self.step_size_table = np.array(
            [
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                16,
                17,
                19,
                21,
                23,
                25,
                28,
                31,
                34,
                37,
                41,
                45,
                50,
                55,
                60,
                66,
                73,
                80,
                88,
                97,
                107,
                118,
                130,
                143,
                157,
                173,
                190,
                209,
                230,
                253,
                279,
                307,
                337,
                371,
                408,
                449,
                494,
                544,
                598,
                658,
                724,
                796,
                876,
                963,
                1060,
                1166,
                1282,
                1411,
                1552,
                1707,
                1878,
                2066,
                2272,
                2499,
                2749,
                3024,
                3327,
                3660,
                4026,
                4428,
                4871,
                5358,
                5894,
                6484,
                7132,
                7845,
                8630,
                9493,
                10442,
                11487,
                12635,
                13899,
                15289,
                16818,
                18500,
                20350,
                22385,
                24623,
                27086,
                29794,
                32767,
            ],
            dtype=np.int16,
        )

    def decode(self, data):
        state = ADPCMState()

        data = np.array(data).astype(np.uint8)

        decoded = []

        for code in data:
            decoded.append(self.decode_sample(code, state))

        decoded = np.array(decoded).astype(np.int16)

        return decoded

    def decode_sample(self, code: np.uint8, state: ADPCMState):
        # Restore previous values of predicted sample and quantizer step size index
        pred_sample = state.prev_sample
        index = state.prev_idx

        # Find quantizer step size from lookup table using index
        step = self.step_size_table[index]

        # Inverse quantize the ADPCM code into a difference using the quantizer step size
        diffq = step >> 3

        if code & 4:
            diffq += step

        if code & 2:
            diffq += step >> 1

        if code & 1:
            diffq += step >> 2

        # Add the difference to the predicted sample

        if code & 8:
            pred_sample -= diffq
        else:
            pred_sample += diffq

        # clip to signed int16 range
        if pred_sample > 32767:
            pred_sample = 32767
        elif pred_sample < -32768:
            pred_sample = -32768

        # Find new quantizer step size by adding the old index and a table lookup using the ADPCM code
        index += self.index_table[code]

        if index < 0:
            index = 0

        if index > 88:
            index = 88

        state.prev_sample = pred_sample
        state.prev_idx = index

        return np.int16(pred_sample)

    def encode(self, samples):
        state = ADPCMState()

        data = np.array(samples).astype(np.int16)

        encoded = []

        for sample in samples:
            encoded.append(self.encode_sample(sample, state))

        encoded = np.array(encoded).astype(np.uint8)

        return encoded

    def encode_sample(self, sample, state):
        predsample = state.prev_sample
        index = state.prev_idx
        step = self.step_size_table[index]

        diff = sample - predsample
        if diff >= 0:
            code = 0
        else:
            code = 8
            diff = -diff

        diffq = step >> 3
        if diff >= step:
            code |= 4
            diff -= step
            diffq += step

        step >>= 1
        if diff >= step:
            code |= 2
            diff -= step
            diffq += step

        step >>= 1
        if diff >= step:
            code |= 1
            diff -= step
            diffq += step

        if code & 8:
            predsample -= diffq
        else:
            predsample += diffq

        if predsample > 32767:
            predsample = 32767
        elif predsample < -32768:
            predssample = -32768

        # Find new quantizer step size by adding the old index and a table lookup using the ADPCM code
        index += self.index_table[code]

        if index < 0:
            index = 0

        if index > 88:
            index = 88

        state.prev_sample = predsample
        state.prev_idx = index

        return np.uint8(code & 0x0F)

