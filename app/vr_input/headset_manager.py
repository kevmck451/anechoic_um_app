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


def headset_connection():
    return False


def get_test_results():

    print('Test Result')

    # get results from warmup generator
    _, test_channel_buffer = circuit_data.load_warmup_data()

    # TODO: get input from headset
    # compare and give update of yes or no



def get_vr_input():
    random = np.random.choice([True, False])
    return random



