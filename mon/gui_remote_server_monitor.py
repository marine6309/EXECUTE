# gui_remote_server_monitor.py

import tkinter as tk
from tkinter import ttk, messagebox
import paramiko

def get_system_status(remote_host, remote_id, remote_password):
    try:
        # SSH 연결
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_host, username=remote_id, password=remote_password)

        # 시스템 리소스 수집 (원격 서버에서 실행하는 명령어)
        command = "mpstat 1 1 | awk '$NF ~ /cpu/ {print 100 - $NF}'"
        stdin, stdout, stderr = ssh.exec_command(command)
        cpu_percent = float(stdout.read().decode('utf-8').strip())

        command = "free | awk '/Mem:/ {print $3/$2*100}'"
        stdin, stdout, stderr = ssh.exec_command(command)
        memory_percent = float(stdout.read().decode('utf-8').strip())

        command = "df -h / | awk '$NF==\"/\" {print $5}'"
        stdin, stdout, stderr = ssh.exec_command(command)
        disk_percent = float(stdout.read().decode('utf-8').strip().replace("%", ""))

        # 결과를 문자열로 반환
        host_info_text.set(f"호스트 이름: {remote_host}\nIP 주소: {remote_host}")
        status_text.set(f"CPU 사용률: {cpu_percent:.2f}%\n메모리 사용률: {memory_percent:.2f}%\n디스크 사용률: {disk_percent:.2f}%")

        ssh.close()
    except Exception as e:
        error_message = f"연결 실패: {e}"
        messagebox.showerror("에러", error_message)
        host_info_text.set(error_message)
        status_text.set("")

def connect_to_remote():
    remote_host = host_entry.get()
    remote_id = id_entry.get()
    remote_password = password_entry.get()
    
    # 원격 서버에 연결하여 시스템 정보 가져오기
    get_system_status(remote_host, remote_id, remote_password)

# 메인 창 설정
root = tk.Tk()
root.title("원격 서버 모니터링")

# 호스트 정보 표시 레이블
host_info_text = tk.StringVar()
host_info_label = ttk.Label(root, textvariable=host_info_text, font=('Helvetica', 10, 'bold'))
host_info_label.grid(column=0, row=0, padx=20, pady=10)

# 입력창과 레이블 (IP, ID, PASSWORD)
host_label = ttk.Label(root, text="원격 호스트 IP:")
host_label.grid(column=0, row=1, padx=20, pady=5)
host_entry = ttk.Entry(root)
host_entry.grid(column=1, row=1, padx=20, pady=5)

id_label = ttk.Label(root, text="사용자 ID:")
id_label.grid(column=0, row=2, padx=20, pady=5)
id_entry = ttk.Entry(root)
id_entry.grid(column=1, row=2, padx=20, pady=5)

password_label = ttk.Label(root, text="비밀번호:")
password_label.grid(column=0, row=3, padx=20, pady=5)
password_entry = ttk.Entry(root, show="*")
password_entry.grid(column=1, row=3, padx=20, pady=5)

# 상태 정보 표시 레이블
status_text = tk.StringVar()
status_label = ttk.Label(root, textvariable=status_text, font=('Helvetica', 12))
status_label.grid(column=0, row=4, padx=20, pady=20)

# 연결 버튼
connect_button = ttk.Button(root, text="원격 서버에 연결", command=connect_to_remote)
connect_button.grid(column=1, row=4, pady=10)

# 창 실행
root.mainloop()
