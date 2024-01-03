import numpy as np
import socket



class VR_Headset_Hardware:
    def __init__(self):
        self.headset_state = False
        self.client_socket = None
        self.server_socket = None

    def connect_hardware(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = '0.0.0.0'
        port = 12345
        self.server_socket.bind((host, port))

        self.server_socket.listen()
        print('Waiting for Connection...')
        self.server_socket.settimeout(10)  # 10 seconds timeout

        try:
            self.client_socket, addr = self.server_socket.accept()
            self.server_socket.settimeout(None)  # Remove the timeout after connection
            print(f"Connection from {addr} has been established.")
            self.headset_state = True
        except socket.timeout:
            print("Connection attempt timed out.")
            self.headset_state = False
        except socket.error as e:
            print(f"Socket error: {e}")
            self.headset_state = False

    def disconnect_hardware(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            self.headset_state = False
        print("Disconnected from client.")


    def get_vr_input(self):
        random = np.random.choice([True, False])
        return random






