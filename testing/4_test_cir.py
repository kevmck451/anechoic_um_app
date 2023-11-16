from tdt import DSPProject, DSPCircuit, DSPBuffer
from audio_abstract import Audio_Abstract

import numpy as np
import wave

try:
	project = DSPProject()
	circuit = project.load_circuit(
		circuit_name = 'Trial', 
		device_name = 'RX8')
	circuit.start()

except DSPError as e:
	print ("Error: {}".format(e))

if circuit.is_connected:
	print('Hardware is Connected')


print('Loading Buffers')
audio_sample_filepath = r'C:/Users/kmcknze1/Desktop/anechoic_um_app/testing/P20.wav'

sample_audio = Audio_Abstract(filepath=audio_sample_filepath)
sample_audio.data = sample_audio.data[1]
sample_audio.num_channels = 1

# print(sample_audio.num_channels)
# print(sample_audio.data)
# print(sample_audio.num_samples)
# sample_audio.waveform()

channel_filepath = r'C:/Users/kmcknze1/Desktop/anechoic_um_app/testing/channels.txt'
channel_list = []
with open(channel_filepath, 'r') as file:
    for line in file:
        integer = int(line.strip())
        channel_list.append(integer)
channel_array = np.array(channel_list)

dur_filepath = r'C:/Users/kmcknze1/Desktop/anechoic_um_app/testing/durations.txt'
dur_list = []
with open(channel_filepath, 'r') as file:
    for line in file:
        integer = int(line.strip())
        dur_list.append(integer)
dur_array = np.array(dur_list)

buffer_audio = circuit.get_buffer('audio', 'w')
buffer_audio.set(sample_audio.data)

buffer_ch = circuit.get_buffer('audio', 'w')
buffer_ch.set(channel_array)

buffer_dur = circuit.get_buffer('audio', 'w')
buffer_dur.set(dur_array)

print('Program is Running')
circuit.trigger(trigger='A', mode='pulse')

while(circuit.is_running):
	pass

circuit.stop()

# while(circuit.is_running):

# 	command = input()
# 	if 't' in command:
# 		print('Triggered')
# 		circuit.trigger(trigger='A', mode='pulse')

# 	if 's' in command:
# 		circuit.stop()
# 		break