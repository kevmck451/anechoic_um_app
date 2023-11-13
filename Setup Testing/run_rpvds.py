from tdt import DSPCircuit

try:
	circuit = DSPCircuit(
						circuit_name = 'test_circuit', 
						device_name = 'RX8',
						interface = 'GB',
						device_id = 1,
						load = True,
						start = False,
						address = None)

except DSPError as e:
	print ("Error: {}".format(e))

if circuit.is_connected:
	print('Hardware is Connected')

if circuit.is_loaded:
	print('Microcode Loaded')

if circuit.is_running:
	print('Running')

print(circuit)

circuit.print_tag_info()



