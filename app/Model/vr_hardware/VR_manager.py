import numpy as np


class VR_Headset_Hardware:
    def __init__(self):

        self.headset_state = False

    def connect(self):
        print('Initializing VR Hardware')
        try:
            # connect to headset
            self.headset_state = True

        except Exception as e:
            self.headset_state = False


    def get_vr_input(self):
        random = np.random.choice([True, False])
        return random






