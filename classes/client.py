import socket

# A classe Client atua como uma dataclasse, apenas
# armazenando soquete e endereço de um cliente conectado ao servidor.
class Client:
    def __init__(self, socket : socket.socket, address : tuple):
        self.socket = socket
        self.address = address