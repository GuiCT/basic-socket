from classes.server import Server

server = Server()
while True:
  server.accept_connection()