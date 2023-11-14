from tdt import DSPProject
from numpy import arange, sin, pi

try:
	project = DSPProject()
	circuit = project.load_circuit(
		circuit_name = 'test_circuit 3', 
		device_name = 'RX8')
	circuit.start()


except DSPError as e:
	print ("Error: {}".format(e))

if circuit.is_connected:
	print('Hardware is Connected')


t = arange(0, 1, circuit.fs**-1)
waveform = sin(2*pi*1e3*t)
speaker_buffer = circuit.get_buffer(data_tag='speaker', mode='w')
speaker_buffer.write(waveform)





