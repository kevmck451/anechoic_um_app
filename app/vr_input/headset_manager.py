import numpy as np
import socket
from threading import Thread
import time



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
        self.list_length = 0
        self.state_changed = False

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

            # self.check_connection()
            input_thread = Thread(target=self.get_vr_input).start()
            check_input = Thread(target=self.check_if_input).start()


    def check_connection(self):
        print('check connection')
        if self.headset_state:
            try:
                self.client_socket.sendall("ping".encode())

                # Set a timeout for the response
                self.client_socket.settimeout(0.1)  # Timeout in seconds

                # Wait for a pong response
                response = self.client_socket.recv(1024).decode()
                if response == "pong":
                    # print('pong')
                    self.headset_state = True
                else:
                    print('no pong')
                    self.headset_state = False

            except Exception as e:
                print("Exception:", e)
                self.headset_state = False

            finally:
                # Reset timeout to None or original value
                self.client_socket.settimeout(None)

    def get_vr_input(self):

        # random = np.random.choice([True, False])
        # return random
        if self.headset_state:
            try:
                while True:
                    # Expecting: speaker selected, degree error
                    vr_input = self.client_socket.recv(1024)
                    if not vr_input:
                        continue
                    self.vr_input = vr_input.decode('utf-8')
                    print("Received:", self.vr_input)
                    self.all_input_list.append(self.vr_input)
                    self.speaker_selected = str(self.vr_input)
                    # self.speaker_selected = str(self.vr_input).split(',')[0].strip()
                    # self.degree_error = str(self.vr_input).split(',')[1].strip()

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                self.client_socket.close()
                print("Connection closed.")
                self.server_socket.close()



    def check_if_input(self):
        while True:
            if self.headset_state:
                current_list_length = len(self.all_input_list)
                if current_list_length > self.list_length:
                    self.list_length = current_list_length
                    self.state_changed = True



