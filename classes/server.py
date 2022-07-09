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
        # Construtor de um socket.
        # Necessário determinar:
        # AddressFamily: formato de endereçamento, no caso foi
        # escolhido AF_INET, referente a endereços IPv4.
        # Type: tipo de soquete, no caso foi escolhido SOCK_STREAM,
        # que faz uso do protocolo TCP.
        # Protocol: protocolo, quando o valor é 0, é escolhido
        # o protocolo padrão para o tipo de soquete escolhido, no
        # caso, o protocolo TCP.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        # O método bind da classe socket.socket associa a instância do socket
        # a um endereço (hostname ou IP) e um número arbitrário de porta.
        # No caso foi utilizado o endereço localhost (padrão, portanto pode
        # ser omitido) e a porta 51268.
        # O endereço e porta são passados como parte de uma tupla.
        self.socket.bind(('', 51268))
        # O método listen da classe socket.socket permite ao
        # soquete que ele receba conexões.
        # É possível limitar o número máximo de conexões, o que não
        # foi feito nesse caso, o número máximo de conexões será definido pela
        # quantidade máximas de Threads que podem ser criadas.
        self.socket.listen()
        # Lista de clientes, começa vazia.
        self.list_of_clients = list()
    
    # Método accept_connection é responsável por aceitar conexões.
    def accept_connection(self):
        # Método accept da classe socket.socket é responsável
        # por receber uma conexão, e só é válido se o soquete
        # que chama o método está bindado a uma porta e no
        # estado de "listening".
        # Retorna o soquete e o endereço do próximo cliente a se conectar.
        # Endereço é uma tupla com (IP, porta), como visto
        # no método bind.
        c_socket, c_address = self.socket.accept()
        # Salva o cliente como uma instância de Client
        client = Client(c_socket, c_address)
        # Inclui o cliente na lista de clientes
        self.list_of_clients.append(client)
        # Mostra mensagem de aceitação de conexão
        print('Cliente conectado: (%s:%s)' % (
            c_address[0],
            c_address[1]))
        # Inicia uma thread para tratar a conexão do novo cliente,
        # passando o cliente como argumento.
        # A thread só é encerrada quando handle_connection termina. 
        threading.Thread(target=self.handle_connection, args=[client]).start()

    # Método chamado para tratar conexão com um cliente
    def handle_connection(self, client : Client):
        # O parâmetro "client" será passado para todos os métodos chamados
        # a partir de agora.
        # Chamada para método que envia mensagem para o cliente
        self.send_message_to_client(client, 'Hello, %s\r\n' % client.address[0])
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
            # LINE FEED -> Faz tratamento para garantir compatibilidade
            # com Linux e outros SOs. Se o char anterior for um
            # CARRIAGE RETURN, o mesmo é retirado do array de bytes.
            # Conclui a recepção
            if char == b'\n':
                if msg[-1] == 13:
                    msg = msg[:-1]
                break
            # BACKSPACE -> Remove o último caracetere do array de bytes
            elif char == b'\b':
                msg = msg[:-1]
            # QUALQUER OUTRO CARACTERE -> Adiciona ao array de bytes
            else:
                msg += char
        # Mostra mensagem recebida pelo cliente
        print('Recebido do cliente (%s:%s): "%s"' % (
            client.address[0],
            client.address[1],
            msg.decode('ascii')))
        # Retorna o array de bytes recebido
        return msg
    
    # Método chamado para enviar uma mensagem ao cliente
    def send_message_to_client(self, client : Client, msg : str):
        # Transforma a string em array de bytes
        # codifica usando padrão ASCII
        msg_in_bytes = msg.encode('ascii')
        # Envia mensagem ao soquete do cliente
        client.socket.send(msg_in_bytes)
        # Mostrando a mensagem enviada no console do servidor
        # Deixa explícito onde é utilizado \r ou \n
        print('Enviado ao cliente (%s:%s): "%s"' % (
            client.address[0],
            client.address[1],
            msg.replace('\n', '\\n').replace('\r', '\\r')))
    
    # Método que encerra conexão com o cliente
    def close_connection(self, client : Client):
        # Remove cliente de lista
        self.list_of_clients.remove(client)
        # Fecha o soquete do cliente
        client.socket.close()
        # Mostra mensagem de encerramento de conexão
        print('Conexão com cliente (%s:%s) encerrada' % (
            client.address[0],
            client.address[1]))

    # Decide o que fazer com uma mensagem recebida do cliente
    def handle_client_message(self, client : Client, msg : bytes):
        # Padrão é retornar status 1: mantém conexão
        status = 1
        if msg == b'ping':
            self.send_message_to_client(client, 'pong\r\n')
        # Caso o cliente queira desconectar
        elif msg == b'quit':
            self.send_message_to_client(client, 'Goodbye.')
            self.close_connection(client)
            # Status passa a ser zero, volta para handle_connection
            # e o loop de lá é quebrado.
            status = 0
        else:
            self.send_message_to_client(client, 'Invalid message.\r\n')
        return status