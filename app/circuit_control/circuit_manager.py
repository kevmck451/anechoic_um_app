# from tdt import DSPProject
import numpy as np
import sounddevice as sd



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
        sd.play(audio_sample.data, audio_sample.sample_rate)
        sd.wait()

    def stop_audio(self):
        sd.stop()
