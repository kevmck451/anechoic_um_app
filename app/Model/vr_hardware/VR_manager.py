from threading import Thread
import socket
import time


class VR_Headset_Hardware:
    def __init__(self):
        self.headset_state = False
        self.client_socket = None
        self.server_socket = None
        self.selected_speaker = 0
        self.degree_error = ''
        self.time_selection_given = 0.0
        self.num_selections = 1
        self.initialize = False

    def connect_hardware(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = '0.0.0.0'
        port = 12345
        self.server_socket.bind((host, port))

        self.server_socket.listen()
        print('Waiting for Connection...')
        self.server_socket.settimeout(40)  # 10 seconds timeout

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

    def update_vr_input_values(self, stop_event, **kwargs):
        self.client_socket.setblocking(0)  # Set the socket to non-blocking

        reaction_timer = kwargs.get('reaction_timer', None)

        while not stop_event.is_set():
            try:
                message = self.client_socket.recv(1024)
                decoded_message = message.decode('utf-8')

                if not message:
                    print("Disconnecting...")
                    self.disconnect_hardware()
                    break


                selection = decoded_message.split(' ')
                self.selected_speaker = selection[0].strip()
                self.degree_error = selection[1].strip()
                self.num_selections += 1

                if reaction_timer:
                    self.time_selection_given = reaction_timer.reaction_time()

                print(f'Selected Speaker: {self.selected_speaker} | Degree Error: {self.degree_error}'
                      f' | React Time: {self.time_selection_given} | Num Sel: {self.num_selections}')

            except socket.error:
                # No data available, sleep briefly to prevent high CPU usage
                time.sleep(0.05)
                continue

        # self.selected_speaker = 0

    def update_vr_input_values_NC(self, stop_event, **kwargs):
        reaction_timer = kwargs.get('reaction_timer', None)
        while not stop_event.is_set():
            time.sleep(0.1)
        if reaction_timer:
            self.time_selection_given = reaction_timer.reaction_time()

    def get_vr_input(self):
        if self.headset_state:
            # Start the thread for receiving messages
            self.message_thread = Thread(target=self.update_vr_input_values, daemon=True)
            self.message_thread.start()






if __name__ == '__main__':
    vr_hardware = VR_Headset_Hardware()
    vr_hardware.connect_hardware()
    vr_hardware.get_vr_input()

    while True:
        pass


