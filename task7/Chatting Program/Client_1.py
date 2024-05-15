import socket
import threading

def connect_to_server():
    client_name = input("Enter your name: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    print("Connected to server.")

    receive_thread = threading.Thread(target=receive_messages, args=(client_name, client_socket))
    receive_thread.start()

    while True:
        recipient, message = input("Enter (Recipient's name:Message): ").split(':', 1)  
        send_message(client_name + "->" + recipient.strip(), message.strip(), client_socket)

def receive_messages(client_name, client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        sender, received_message = message.split('->', 1)
        recipient, received_message = received_message.split(':', 1)
        if recipient.strip() == client_name:
            print(f"{sender}-> {client_name}: {received_message}")

def send_message(recipient, message, client_socket):
    client_socket.send((recipient + ':' + message).encode('utf-8'))

if __name__ == "__main__":
    connect_to_server()
