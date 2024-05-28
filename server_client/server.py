import socket

# 서버 설정
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5555

# 소켓 생성 및 바인딩
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

# 클라이언트 연결 대기
client_socket, client_address = server_socket.accept()
print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

while True:
    # 클라이언트로부터 데이터 수신
    client_data = client_socket.recv(1024).decode()
    if not client_data:
        break
    
    # 수신된 데이터 출력
    print(f"Received data from client: {client_data}")

# 연결 종료
client_socket.close()
server_socket.close()
