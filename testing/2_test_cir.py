from tdt import DSPCircuit

try:
	circuit = DSPCircuit(
						circuit_name = 'test_circuit 2', 
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

print('Program is Running')
while(circuit.is_running):
	circuit.start()

	command = input()
	if 'trigger' in command:
		circuit.trigger(trigger = 1)

	if 'stop' in command:
		circuit.stop()
		break







