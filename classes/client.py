import socket

class Client:
    def __init__(self, socket : socket.socket, address):
        self.socket = socket
        self.address = address