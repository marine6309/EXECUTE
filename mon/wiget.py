import psutil
import tkinter as tk
import subprocess
import time
import signal
import sys

class PerformanceWidget(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Performance Widget")
        self.geometry("300x300")
        self.attributes("-topmost", True)
        self.overrideredirect(True)  # 창의 경계를 없애기 위해 사용

        # CPU 사용량 라벨
        self.cpu_label = tk.Label(self, text="CPU Usage: ", font=("Helvetica", 14))
        self.cpu_label.pack(pady=5)

        # 메모리 사용량 라벨
        self.mem_label = tk.Label(self, text="Memory Usage: ", font=("Helvetica", 14))
        self.mem_label.pack(pady=5)

        # 디스크 사용량 라벨
        self.disk_label = tk.Label(self, text="Disk Usage: ", font=("Helvetica", 14))
        self.disk_label.pack(pady=5)

        # 네트워크 응답시간 라벨
        self.ping_label = tk.Label(self, text="Network Latency: ", font=("Helvetica", 14))
        self.ping_label.pack(pady=5)

        self.update_widget()

    def update_widget(self):
        # CPU 사용량 업데이트
        cpu_usage = psutil.cpu_percent(interval=1)
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")

        # 메모리 사용량 업데이트
        memory_info = psutil.virtual_memory()
        mem_usage = memory_info.percent
        self.mem_label.config(text=f"Memory Usage: {mem_usage}%")

        # 디스크 사용량 업데이트
        disk_info = psutil.disk_usage('/')
        disk_usage = disk_info.percent
        self.disk_label.config(text=f"Disk Usage: {disk_usage}%")

        # 네트워크 응답시간 업데이트
        ping_time = self.get_ping_time('google.com')
        self.ping_label.config(text=f"Network Latency: {ping_time} ms")

        # 주기적으로 업데이트 (1초 간격)
        self.after(1000, self.update_widget)

    def get_ping_time(self, host):
        # ping 명령어를 사용하여 네트워크 응답시간을 측정
        try:
            output = subprocess.check_output(["ping", "-n", "1", host], stderr=subprocess.STDOUT, universal_newlines=True)
            for line in output.split("\n"):
                if "time=" in line:
                    # Windows의 경우 "time=XXms" 형태로 응답 시간이 표시됨
                    return line.split("time=")[1].split("ms")[0].strip()
            return "N/A"
        except subprocess.CalledProcessError:
            return "N/A"

def signal_handler(sig, frame):
    print("Ctrl+C pressed, exiting...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C 시그널 핸들러 등록
    app = PerformanceWidget()
    app.mainloop()
