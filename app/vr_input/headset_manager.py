import numpy as np

import circuit_data



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



