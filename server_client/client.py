import socket

# 서버 설정
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# 데이터 전송
data_to_send = "Hello, server!"
client_socket.send(data_to_send.encode())
print(f"[*] Sent data to server: {data_to_send}")

# 연결 종료
client_socket.close()
