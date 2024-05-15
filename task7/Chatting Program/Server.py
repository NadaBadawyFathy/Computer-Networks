import socket
import threading

clients = {}

def start_server():
    global clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    print("Server started. Waiting for clients...")

    while True:
        client_socket, client_address = server_socket.accept()
        clients[client_socket] = client_address
        threading.Thread(target=client_handler, args=(client_socket,)).start()

def client_handler(client_socket):
    global clients
    client_address = clients[client_socket]
    client_name = client_address[0]
    print(f"Client connected: {client_name}")

    while True:
        message = client_socket.recv(1024).decode('utf-8')

        if message.lower() == "exit":
            del clients[client_socket]
            client_socket.close()
            print(f"Client disconnected: {client_name}")
            break

        print(f"Message from {client_name}: {message}")
        broadcast_message(message, client_socket)

def broadcast_message(message, sender_socket):
    global clients
    for client_socket in clients.keys():
        if client_socket != sender_socket:
            client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_server()
