from tdt import DSPProject
from numpy import arange, sin, pi

try:
	project = DSPProject()
	circuit = project.load_circuit(
		circuit_name = 'test_circuit 3 ex', 
		device_name = 'RX8')
	circuit.start()


except DSPError as e:
	print ("Error: {}".format(e))

if circuit.is_connected:
	print('Hardware is Connected')


t = arange(0, 1, circuit.fs**-1)
waveform = sin(2*pi*1e3*t)
speaker_buffer = circuit.get_buffer(data_tag='speaker', mode='w')
# print(f"sample rate is {circuit.fs}")
# print(f"sample count: {len(waveform)} of type {waveform.dtype}")
# print(type(speaker_buffer))
# print(dir(speaker_buffer))
waveform[-5000:] = 0
speaker_buffer.set(waveform)

import time
print("quiet...")

time.sleep(2)

print("beep!")

circuit.set_tag("chan",8)

circuit.trigger(trigger = 1)

print("quiet")
time.sleep(5)