import psutil
from datetime import datetime, timedelta
import time

def is_ethernet_active():
    # 네트워크 인터페이스 상태 가져오기
    net_io = psutil.net_io_counters(pernic=True)
    
    # 이더넷 네트워크 인터페이스 찾기
    ethernet_interface = None
    for interface, stats in net_io.items():
        if '이더넷 2' in interface:
            ethernet_interface = interface
            break
    
    if not ethernet_interface:
        print("이더넷 인터페이스를 찾을 수 없습니다.")
        return False
    
    # 이더넷 네트워크 인터페이스의 데이터 송수신량 체크하여 활성화 여부 판단
    return net_io[ethernet_interface].bytes_sent > 0 or net_io[ethernet_interface].bytes_recv > 0

def save_daily_network_active_time():
    # 현재 날짜 가져오기
    today_date = datetime.now().date()
    
    # 파일 이름 생성
    filename = f"network_active_time_{today_date}.txt"
    
    # 현재 네트워크 활성화 상태 확인
    active = is_ethernet_active()
    
    # 파일에 기록
    with open(filename, 'a') as file:
        file.write(f"{datetime.now()}: {'Active' if active else 'Inactive'}\n")

def display_daily_network_active_time():
    # 현재 날짜 가져오기
    today_date = datetime.now().date()
    
    # 파일 이름 생성
    filename = f"network_active_time_{today_date}.txt"
    
    # 파일 읽기
    try:
        with open(filename, 'r') as file:
            print(f"일별 네트워크 활성화 시간 ({today_date}):")
            print(file.read())
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

# 네트워크 활성화 시간 저장
save_daily_network_active_time()

# 저장된 네트워크 활성화 시간 표시
display_daily_network_active_time()

# 프로그램이 종료되지 않도록 대기
input("프로그램이 종료되지 않으려면 아무 키나 누르세요...")
