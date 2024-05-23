import psutil
import socket
import tkinter as tk
from tkinter import ttk

def get_host_info():
    # 호스트 이름과 IP 주소 가져오기
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return f"호스트 이름: {host_name}\nIP 주소: {ip_address}"

def get_system_status():
    # 시스템 리소스 수집
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent

    # 호스트 정보 업데이트
    host_info_text.set(get_host_info())

    # 시스템 상태 업데이트
    status_text.set(f"CPU 사용률: {cpu_percent}%\n메모리 사용률: {memory_percent}%\n디스크 사용률: {disk_percent}%")

    # 일정 시간마다 업데이트 호출
    root.after(1000, get_system_status)

# 메인 창 설정
root = tk.Tk()
root.title("실시간 서버 모니터링")

# 창 크기 설정 (50x30)
root.geometry("400x300")

# 호스트 정보 표시 레이블
host_info_text = tk.StringVar()
host_info_label = ttk.Label(root, textvariable=host_info_text, font=('Helvetica', 10, 'bold'))
host_info_label.grid(column=0, row=0, padx=20, pady=10)

# 상태 정보 표시 레이블
status_text = tk.StringVar()
status_label = ttk.Label(root, textvariable=status_text, font=('Helvetica', 12))
status_label.grid(column=0, row=1, padx=20, pady=20)

# 최초 업데이트 호출
get_system_status()

# 창 실행
root.mainloop()
