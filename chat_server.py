# chat_server.py

import socket
import threading

def handle_client(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"{client_name} has left the chat.")
                break
            print(f"{client_name}: {message}")
            broadcast(f"{client_name}: {message}", client_socket)
        except Exception as e:
            print(f"Error handling client {client_name}: {e}")
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message: {e}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(2)
    print("Server listening on port 8080")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")

        client_name = client_socket.recv(1024).decode('utf-8')
        print(f"{client_name} has joined the chat.")

        clients.append(client_socket)
        client_socket.send("Welcome to the chat! Type 'exit' to leave.".encode('utf-8'))

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_name))
        client_handler.start()

clients = []

if __name__ == "__main__":
    start_server()
