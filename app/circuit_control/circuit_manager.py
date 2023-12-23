from tdt import DSPProject


stimulus_number = int()



# Function to start TDT Connection
def TDT_connection(RPvds_circuit_name):
    try:
        project = DSPProject()
        circuit = project.load_circuit(
            circuit_name = RPvds_circuit_name, 
            device_name = 'RX8')
        circuit.start()

        if circuit.is_connected:
            print('Hardware is Connected')
            return circuit


    except DSPError as e:
        print ("Error: {}".format(e))


    




