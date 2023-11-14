from tdt import DSPCircuit

try:
	circuit = DSPCircuit(
						circuit_name = 'test_circuit 1', 
						device_name = 'RX8',
						interface = 'GB',
						device_id = 1,
						load = True,
						start = True,
						address = None)

	circuit.start(pause=10000)
	# circuit.stop()
	
except DSPError as e:
	print ("Error: {}".format(e))
