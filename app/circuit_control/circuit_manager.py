# from tdt import DSPProject
import numpy as np


stimulus_number = int()


class TDT_Circuit:
    def __init__(self):
        random = np.random.choice([True, False])
        if random: self.circuit_state = True
        else: self.circuit_state = False
        # try:
        #     project = DSPProject()
        #     circuit = project.load_circuit(
        #         circuit_name = RPvds_circuit_name,
        #         device_name = 'RX8')
        #     circuit.start()
        #
        #     if circuit.is_connected:
        #         print('Hardware is Connected')
        #         return circuit
        #
        #
        # except DSPError as e:
        #     print ("Error: {}".format(e))



    def trigger_audio_sample(self, audio_sample, channel):
        print('Playing Audio')

