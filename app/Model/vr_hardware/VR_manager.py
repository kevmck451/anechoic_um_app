import numpy as np


class VR_Headset_Hardware:
    def __init__(self):
        print('Initializing VR Hardware')
        self.headset_state = bool

        try:
            # connect to headset
            self.headset_state = True

        except Exception as e:
            self.headset_state = False


    def get_vr_input(self):
        random = np.random.choice([True, False])
        return random






