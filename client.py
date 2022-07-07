import socket

# Cria o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# Não é necessário bindar a uma porta específica.
# Conectando ao socket do servidor...
client_socket.connect(('localhost', 51268))
# Recebendo mensagem do servidor e printando com decodificação ASCII
msg = client_socket.recv(1024)
print(msg.decode('ascii'))
# Enviando uma mensagem "ping". O fim da mensagem é denotado por \r\n
client_socket.send(b'ping\r\n')
# Recebendo mensagem do servidor novamente
msg = client_socket.recv(1024)
print(msg.decode('ascii'))
# Enviando mensagem de "shutdown" para desligar o servidor.
client_socket.send(b'shutdown\r\n')
# Fim da execução do socket.