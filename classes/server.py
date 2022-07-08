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
        # Método responsável por receber uma conexão, só é válido se
        # o soquete que chama o método está bindado a uma porta e
        # no estado de "listening"
        # Recebe o soquete e o endereço do próximo cliente a se conectar.
        # Endereço é uma tupla com (IP, porta)
        c_socket, c_address = self.socket.accept()
        # Salva o cliente como uma instância de Client
        # Contendo socket e endereço
        client = Client(c_socket, c_address)
        # Inclui o cliente na lista de clientes
        self.list_of_clients.append(client)
        # Inicia uma thread para tratar a conexão do novo cliente,
        # passando o cliente como argumento.
        # A thread só é encerrada quando handle_connection termina. 
        threading.Thread(target=self.handle_connection, args=[client]).start()

    # Método chamado para tratar conexão com um cliente
    def handle_connection(self, client : Client):
        # O parâmetro "client" será passado para todos os métodos chamados
        # a partir de agora.
        # Chamada para método que envia mensagem para o cliente
        self.send_message_to_client(client, 'Hello, %s' % str(client.address))
        status = 1
        # É necessário algum mecanismo para encerrar o loop em algum momento
        # o loop será encerrado quando handle_client_message retornar um status
        # diferente de 1 (no caso, 0).
        while status == 1:
            # Método que recebe mensagem do cliente, byte a byte (char a char)
            # A variável msg é do tipo bytes.
            msg = self.receive_message_from_client(client)
            # Método que decide o que fazer com base na mensagem recebida.
            status = self.handle_client_message(client, msg)

    # Método chamado para receber a mensagem de um cliente
    def receive_message_from_client(self, client : Client):
        # Inicializa array de bytes vazio
        msg = b''
        # Loop para recuperar char a char
        while True:
            # Recebe o char
            char = client.socket.recv(1)
            # CARRIAGE RETURN -> Ignora o próximo caractere (\n, line-end)
            # e conclui a recepção
            if char == b'\r':
                client.socket.recv(1)
                break
            # BACKSPACE -> Remove o último caracetere do array de bytes
            elif char == b'\b':
                msg = msg[:-1]
            # QUALQUER OUTRO CARACTERE -> Adiciona ao array de bytes
            else:
                msg += char
        # Retorna o array de bytes recebido
        return msg
    
    # Método chamado para enviar uma mensagem ao cliente
    def send_message_to_client(self, client : Client, msg : str):
        # Transforma a string em array de bytes
        # codifica usando padrão ASCII
        msg_in_bytes = msg.encode('ascii')
        # Envia mensagem ao soquete do cliente
        client.socket.send(msg_in_bytes)
    
    # Método que encerra conexão com o cliente
    def close_connection(self, client : Client):
        # Remove cliente de lista
        self.list_of_clients.remove(client)
        # Fecha o soquete do cliente
        client.socket.close()

    # Decide o que fazer com uma mensagem recebida do cliente
    def handle_client_message(self, client : Client, msg : bytes):
        # Padrão é retornar status 1: mantém conexão
        status = 1
        if msg == b'ping':
            self.send_message_to_client(client, 'pong')
        # Caso o cliente queira desconectar
        elif msg == b'quit':
            self.send_message_to_client(client, 'Goodbye.')
            self.close_connection(client)
            # Status passa a ser zero, volta para handle_connection
            # e o loop de lá é quebrado.
            status = 0
        else:
            self.send_message_to_client(client, 'Invalid message.')
        return status