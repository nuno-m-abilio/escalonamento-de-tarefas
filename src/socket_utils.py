import socket
import json
import threading
import time

HOST = 'localhost'

def send_message(port: int, data: dict):
    '''Envia um dicionário como JSON via socket para a porta informada.'''
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, port))
                s.sendall(json.dumps(data).encode())
            break
        except ConnectionRefusedError:
            time.sleep(0.1)

def start_server(my_port: int, on_message):
    '''Inicia um servidor socket na porta informada e chama on_message(data, addr) quando receber algo.'''
    def server_thread():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, my_port))
            s.listen()
            print(f"[SocketUtils] Escutando na porta {my_port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(4096)
                    if not data:
                        continue
                    try:
                        message = json.loads(data.decode())
                        on_message(message, addr)
                    except json.JSONDecodeError:
                        print("[SocketUtils] Erro ao decodificar JSON.")

    thread = threading.Thread(target=server_thread, daemon=True)
    thread.start()
