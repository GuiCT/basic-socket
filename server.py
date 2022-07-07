import socket
from time import sleep

# Criando o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bindando o socket a porta 51268
server_socket.bind(('', 51268))
# Colocando o socket para escutar (no máximo 1 conexões concorrentes)
server_socket.listen(1)
# Utilizando loop infinito para tratar as conexões
while True:
  client_socket, client_address = server_socket.accept()
  print('Receiving connection from %s' % str(client_address))
  # Enviando mensagem para o cliente
  client_socket.send(b'Waiting for "ping"\r\n')
  while True:
    # Recebendo mensagem do cliente
    msg = b''
    while True:
      char = client_socket.recv(1)
      if char == b'\r':
        client_socket.recv(1)
        break
      elif char == b'\b':
        msg = msg[:-1]
      else:
        msg += char
    if msg == b'ping':
      client_socket.send(b'pong\r\n')
    elif msg == b'shutdown':
      client_socket.send(b'Shutting down\r\n')
      sleep(0.5)
      client_socket.close()
      server_socket.close()
      exit()
    else:
      client_socket.send(b'Bye.\r\n')
      client_socket.close()
      print('Closing connection with %s' % str(client_address))
      break