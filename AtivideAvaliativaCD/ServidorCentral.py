# servidor_central.py
import socket
import threading
import json
import asyncio
import websockets 

# Configurações do servidor central
CENTRAL_SERVER_HOST = 'localhost'
CENTRAL_SERVER_PORT = 5000
WEBSOCKET_PORT = 6789

# Lista de clientes WebSocket conectados
clientes_websocket = []

async def broadcast_alert(alerta):
    """Envia o alerta a todos os clientes WebSocket conectados"""
    if clientes_websocket:
        await asyncio.wait([cliente.send(alerta) for cliente in clientes_websocket])

def processar_alerta(client_socket):
    """Recebe e processa alertas dos servidores regionais"""
    while True:
        alerta = client_socket.recv(1024).decode()
        if alerta:
            print("Alerta recebido:", alerta)
            asyncio.run(broadcast_alert(alerta))
        else:
            break
    client_socket.close()

def iniciar_servidor_central():
    """Configura o servidor central para aceitar conexões de servidores regionais"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((CENTRAL_SERVER_HOST, CENTRAL_SERVER_PORT))
    server_socket.listen(5)
    print(f"Servidor Central de Alertas iniciado em {CENTRAL_SERVER_HOST}:{CENTRAL_SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=processar_alerta, args=(client_socket,)).start()

async def websocket_handler(websocket, path):
    """Gerencia as conexões WebSocket com clientes"""
    clientes_websocket.append(websocket)
    try:
        await websocket.wait_closed()  # Aguarda a desconexão
    finally:
        clientes_websocket.remove(websocket)

async def iniciar_servidor_websocket():
    """Inicia o servidor WebSocket para comunicação com a interface"""
    print(f"Servidor WebSocket iniciado em ws://localhost:{WEBSOCKET_PORT}")
    async with websockets.serve(websocket_handler, "localhost", WEBSOCKET_PORT):
        await asyncio.Future()  # Mantém o WebSocket ativo

if __name__ == "__main__":
    # Inicia o servidor central e o WebSocket
    threading.Thread(target=iniciar_servidor_central).start()
    asyncio.run(iniciar_servidor_websocket())
