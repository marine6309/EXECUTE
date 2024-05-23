import psutil
import time
import socket
import os
from datetime import datetime

# console size 
def set_console_size(width, height):
    os.system(f"mode con: cols={width} lines={height}")
set_console_size(80, 15)

# cpu, memory, disk, network usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('C:').percent

def get_network_response_time(host="www.naver.com", port=80):
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

# hostname, time
def get_host_ip():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return host_name, ip_address

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# header print
def print_header(host, ip_address):
    os.system('cls' if os.name == 'nt' else 'clear')  # Windows 및 Unix 시스템에서 화면을 지웁니다.
    print("=" * 80)
    print(f"호스트: {host} | IP 주소: {ip_address} | 현재 시간: {get_current_time()}")
    print("=" * 80)

# main loop
host, ip_address = get_host_ip()
print_header(host, ip_address)

while True:
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    network_response_time = get_network_response_time()
    
    print_header(host, ip_address)
    print(f"CPU 사용률: {cpu_usage}%")
    print(f"메모리 사용률: {memory_usage}%")
    print(f"디스크 사용률: {disk_usage}%")
    print(f"네트워크 응답시간: {network_response_time}ms")
    
    time.sleep(1)  # 1초마다 업데이트
