import socket

# Cria o socket do cliente utilizando o construtor de socket.socket
# O funcionamento desse método construtor é explicado na classe Server.
# Resumindo: soquete com endereço IPv4 que utiliza protocolo TCP.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# Não é necessário bindar a uma porta específica.
print('Conectando-se ao servidor...')
# Conectando ao socket do servidor...
# (Aqui assume-se que o servidor está em funcionamento na porta 51268)
client_socket.connect(('localhost', 51268))
print('Conectado ao servidor!')
# Recebendo mensagem do servidor e printando com decodificação ASCII
msg = client_socket.recv(1024)
print('Servidor envia: ' + msg.decode('ascii'), end='')
print('Enviando "ping" para o servidor e aguardando resposta...')
# Enviando uma mensagem "ping". O fim da mensagem é denotado por \r\n
client_socket.send(b'ping\r\n')
# Recebendo mensagem do servidor e printando com decodificação ASCII
msg = client_socket.recv(1024)
print('Servidor envia: ' + msg.decode('ascii'), end='')
print('Enviando "quit" para o servidor e aguardando resposta...')
# Enviando mensagem de "quit" para desconectar-se do servidor.
client_socket.send(b'quit\r\n')
# Recebendo mensagem do servidor e printando com decodificação ASCII
msg = client_socket.recv(1024)
print('Servidor envia: ' + msg.decode('ascii'), end='')
# Fim da execução do socket.