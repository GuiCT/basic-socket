import socket
import threading
from classes.client import Client

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.socket.bind(('', 51268))
        self.socket.listen()
        self.list_of_clients = list()
    
    def accept_connection(self):
        c_socket, c_address = self.socket.accept()
        client = Client(c_socket, c_address)
        self.list_of_clients.append(client)
        threading.Thread(target=self.handle_connection, args=[client]).start()

    def handle_connection(self, client : Client):
        self.send_message_to_client(client, 'Hello, %s' % str(client.address))
        status = 1
        while status == 1:
            msg = self.receive_message_from_client(client)
            status = self.handle_client_message(client, msg)

    def receive_message_from_client(self, client : Client):
        msg = b''
        while True:
            char = client.socket.recv(1)
            if char == b'\r':
                client.socket.recv(1)
                break
            elif char == b'\b':
                msg = msg[:-1]
            else:
                msg += char
        return msg
    
    def send_message_to_client(self, client : Client, msg : str):
        msg_in_bytes = msg.encode('ascii')
        client.socket.send(msg_in_bytes)
    
    def close_connection(self, client : Client):
        self.list_of_clients.remove(client)
        client.socket.close()

    def handle_client_message(self, client : Client, msg : bytes):
        status = 1
        if msg == b'ping':
            self.send_message_to_client(client, 'pong')
        elif msg == b'quit':
            self.send_message_to_client(client, 'Goodbye.')
            self.close_connection(client)
            status = 0
        else:
            self.send_message_to_client(client, 'Invalid message.')
        return status