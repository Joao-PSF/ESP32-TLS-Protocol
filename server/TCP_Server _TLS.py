import ssl
import socket
import threading

HOST = 'XXX.XXX.X.XX'
PORT = 8883

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#ctx.minimum_version = ssl.TLSVersion.TLSv1_3
ctx.load_cert_chain(certfile="server.crt", keyfile="server.key")

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Servidor iniciado, esperando conexoes...")
print(f'IP do Servidor: {socket.gethostbyname(socket.gethostname())}')

def handle_connection(cliente_socket, cliente_IP):

    print("Cliente tentando se conectar:", cliente_IP)
    ssl_cliente_socket = ctx.wrap_socket(cliente_socket, server_side=True)
    ssl_cliente_socket.settimeout(10)

    while True:

        try:

            data = ssl_cliente_socket.recv(1024).decode("utf-8")

            if data:

                print(f"Dados recebidos de {cliente_IP}: {data}")
                ssl_cliente_socket.send("Mensagem recebida!".encode())

        except ssl.SSLWantReadError:

            continue
        except ssl.SSLWantWriteError:

            continue
        except socket.timeout:

            print("Tempo limite atingido, fechando conexao com o cliente")
            ssl_cliente_socket.close()
            break

while True:

    cliente_socket, cliente_IP = server_socket.accept()
    thread = threading.Thread(target=handle_connection, args=(cliente_socket, cliente_IP))
    thread.start()
