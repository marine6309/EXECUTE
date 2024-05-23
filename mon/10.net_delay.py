import socket
import time
import os

def get_network_latency(host="google.com", port=80):
    try:
        start_time = time.time()
        sock = socket.create_connection((host, port))
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)  # 밀리초 단위로 변환
        return latency
    except Exception as e:
        print(f"Error while measuring network latency: {e}")
        return "N/A"

def get_network_response_time(host="google.com", port=80):
    try:
        start_time = time.time()
        sock = socket.create_connection((host, port), timeout=5)  # 연결 시도, timeout 설정으로 연결 시간을 제한할 수 있습니다.
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)  # 밀리초 단위로 변환
        sock.close()  # 소켓 닫기
        return response_time
    except Exception as e:
        print(f"Error while measuring network response time: {e}")
        return "N/A"

while True:
    os.system('cls' if os.name == 'nt' else 'clear')  # 윈도우와 리눅스/맥OS에 따라 clear 명령어가 다릅니다.
    
    network_latency = get_network_latency()
    network_response_time = get_network_response_time()

    print(f"네트워크 지연시간: {network_latency}ms")
    print(f"네트워크 응답시간: {network_response_time}ms")
    
    time.sleep(1)
