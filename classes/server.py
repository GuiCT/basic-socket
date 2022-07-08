# Módulo socket contém a implementação da API de Soquetes Berkeley
import socket
# Módulo threading permite a criação de vários processos em paralelo,
# o que permite a execução de várias conexões simultâneas.
import threading
# Classe Client armazena informações do cliente.
from classes.client import Client

class Server:
    # Construtor da classe Server
    def __init__(self):
        # socket.socket é uma classe, e abaixo está uma chamada para
        # o construtor dessa classe.
        # Descrição de socket.socket pela documentação do Python
        # (traduzida para o português)
        #######################################################################
        # class socket.socket(family=AF_INET, type=SOCK_STREAM,
        #   proto=0, fileno=None)
        # Cria um novo soquete a partir de um tipo de endereço (family),
        # tipo de soquete (type) e protocolo (proto).
        # AF_INET indica um endereço IPv4, SOCK_STREAM indica um soquete
        # que utiliza protocolo TCP/IP ou um pipe no caso de sistemas UNIX.
        # Protocolo 0 indica que o sistema deve escolher o protocolo.
        # Essa chamada para a criação de um socket é padronizada independente
        # da linguagem de programação que seja utilizada. As explicações
        # abaixo são referentes ao Python, mas pode ser aplicado para qualquer
        # outra linguagem de programação.
        #######################################################################
        # Referências:
        # Documentação do Python (em inglês)
        # https://docs.python.org/3/library/socket.html#socket.socket
        # Página da IBM explicando os tipos de soquete
        # https://www.ibm.com/docs/en/aix/7.1?topic=protocols-socket-types
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        # O método bind da classe socket.socket associa a instância do socket
        # a um endereço (hostname ou IP) e um número arbitrário de porta.
        # No caso foi utilizado o endereço localhost (padrão, portanto pode
        # ser omitido) e a porta 51268.
        #######################################################################
        # Referências:
        # Documentação do Python (em inglês)
        # https://docs.python.org/3/library/socket.html#socket.socket.bind
        self.socket.bind(('', 51268))
        # O método listen permite ao soquete que ele receba conexões.
        # É possível limitar o número máximo de conexões, o que não
        # foi feito nesse caso, o número máximo de conexões será definido pela
        # quantidade máximas de Threads que podem ser criadas.
        self.socket.listen()
        # Lista de clientes, começa vazia.
        self.list_of_clients = list()
    
    # Método accept_connection é responsável por aceitar conexões.
    def accept_connection(self):
        # Recebe o soquete e o endereço do próximo cliente a se conectar.
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