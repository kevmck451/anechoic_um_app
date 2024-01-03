import numpy as np

import circuit_data


class VR_Headset_Hardware:
    def __init__(self):
        random = np.random.choice([True, False])
        if random:
            self.headset_state = True
        else:
            self.headset_state = False

    def get_vr_input(self):
        random = np.random.choice([True, False])
        return random






