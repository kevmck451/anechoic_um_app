import numpy as np
import socket
from threading import Thread



class VR_Headset_Hardware:
    def __init__(self):
        # random = np.random.choice([True, False])
        # if random:
        #     self.headset_state = True
        # else:
        #     self.headset_state = False
        self.all_input_list = []
        self.vr_input = 'None'
        self.speaker_selected = 'None'
        self.degree_error = 'None'
        self.headset_state = False
        self.first_connect = False

        self.server_thread = Thread(target=self.start_server)
        self.server_thread.start()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', 12345))
        self.server_socket.listen()
        print('Waiting for a connection...')

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} established.")
            self.first_connect = True
            self.headset_state = True

            # Update the client_socket
            self.client_socket = client_socket

            # Send confirmation to client
            self.client_socket.sendall("Connection established".encode('utf-8'))

    def check_connection(self):
        try:
            self.client_socket.sendall("ping".encode())

            # Wait for a pong response
            response = self.client_socket.recv(1024).decode()
            if response == "pong":
                self.headset_state = True
            else:
                self.headset_state = False

        except Exception as e:
            self.headset_state = False
            # Handle other exceptions like timeout, connection reset, etc.

    def get_vr_input(self):
        # random = np.random.choice([True, False])
        # return random

        try:
            while True:
                # Expecting: speaker selected, degree error
                self.vr_input = self.client_socket.recv(1024)
                print(self.vr_input)
                self.all_input_list.append(self.vr_input)

                self.speaker_selected = str(self.vr_input)
                # self.speaker_selected = str(self.vr_input).split(',')[0].strip()
                # self.degree_error = str(self.vr_input).split(',')[1].strip()

                print("Received:", self.vr_input.decode('utf-8'))
                # Process data here

        except Exception as e:
            print(f"An error occurred: {e}")
            self.headset_state = False

        finally:
            self.client_socket.close()
            print("Connection closed.")
            self.server_socket.close()
            self.headset_state = False






