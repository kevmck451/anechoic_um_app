import socket
from threading import Thread

def send_messages(sock):
    while True:
        message = input("Enter Speaker: ")
        sock.sendall(message.encode('utf-8'))

def receive_messages(sock):
    while True:
        try:
            response = sock.recv(1024).decode()
            if not response:  # Check if response is empty
                print("Server has disconnected.")
                break
            if response == "ping":
                sock.sendall("pong".encode())
            else:
                print("Received from server:", response)
        except Exception as e:
            print("Error receiving message:", e)
            break

def main():
    server_ip = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
        print("Connected to the server successfully.")

        # Create threads for sending and receiving messages
        # send_thread = Thread(target=send_messages, args=(client_socket,))
        # receive_thread = Thread(target=receive_messages, args=(client_socket,))
        #
        # receive_thread.start()
        # send_thread.start()
        #
        # receive_thread.join()
        # send_thread.join()

    except Exception as e:
        print(f"Failed to connect to the server: {e}")

    finally:
        client_socket.close()
        print("Disconnected from server.")

if __name__ == "__main__":
    main()






