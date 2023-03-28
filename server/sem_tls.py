import socket
import threading

HOST = '192.168.0.11'
PORT = 8883

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Servidor iniciado, esperando conexoes...")
print(f'IP do Servidor: {socket.gethostbyname(socket.gethostname())}')

def handle_connection(cliente_socket, cliente_IP):

    print("Cliente tentando se conectar:", cliente_IP)
    cliente_socket.settimeout(30)

    while True:

        try:

            data = cliente_socket.recv(1024).decode("utf-8")

            if data:

                print(f"Dados recebidos de {cliente_IP}: {data}")
                #ssl_cliente_socket.send("Mensagem recebida!".encode())
        except socket.timeout:

            print("Tempo limite atingido, fechando conexao com o cliente")
            server_socket.close()
            break

while True:

    cliente_socket, cliente_IP = server_socket.accept()
    thread = threading.Thread(target=handle_connection, args=(cliente_socket, cliente_IP))
    thread.start()