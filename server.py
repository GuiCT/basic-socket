# Implementação é feita na classe Server
from classes.server import Server

# Cria uma instância da classe Server
server = Server()
while True:
  # Aceitando conexões indefinidamente
  server.accept_connection()