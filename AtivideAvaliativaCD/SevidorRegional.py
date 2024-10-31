import socket
import threading
import time
import json


CENTRAL_SERVER_HOST = 'localhost'
CENTRAL_SERVER_PORT = 5000

def enviar_alerta(evento):
    """Envia o alerta formatado em JSON para o servidor central"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CENTRAL_SERVER_HOST, CENTRAL_SERVER_PORT))
        mensagem = json.dumps(evento)
        s.sendall(mensagem.encode())
        print(f"Alerta enviado: {mensagem}")

def monitorar_eventos():
    
    while True:
        evento = {"tipo": "inundação", "regiao": "Norte", "gravidade": "alta"}
        enviar_alerta(evento)
        time.sleep(10)  

if __name__ == "__main__":
    
    monitor_thread = threading.Thread(target=monitorar_eventos)
    monitor_thread.start()
