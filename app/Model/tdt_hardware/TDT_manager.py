# from tdt import DSPProject
import numpy as np
import sounddevice as sd
import time


class TDT_Circuit:
    def __init__(self):

        # random = np.random.choice([True, False])
        # if random: self.circuit_state = True
        # else: self.circuit_state = False
        self.circuit_state = False

        RPvds_circuit_filepath = 'tdt_circuit.rcx'


    def connect_hardware(self):
        print('Initializing TDT Hardware')
        try:
            project = DSPProject()
            self.circuit = project.load_circuit(
                circuit_name = RPvds_circuit_filepath,
                device_name = 'RX8')
            self.circuit.start()

            if self.circuit.is_connected:
                # print('Hardware is Connected')
                self.circuit_state = True
            else: self.circuit_state = False

        # except DSPError as e:
        #     self.circuit_state = False
        #     pass

        except Exception as e:
            self.circuit_state = False


    def trigger_audio_sample_computer(self, audio_sample):
        sd.play(audio_sample.data, audio_sample.sample_rate)
        time.sleep(audio_sample.sample_length)
        # sd.wait()


    def trigger_audio_sample(self, audio_sample, channel):

        speaker_buffer = self.circuit.get_buffer(data_tag='speaker', mode='w')
        speaker_buffer.set(audio_sample.data)

        self.circuit.set_tag("chan", channel)
        self.circuit.trigger(trigger=1)

        time.sleep(audio_sample.sample_length)


