import psutil
import tkinter as tk
from tkinter import Label
from functools import partial

class SystemMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        # 창 크기 설정
        self.root.geometry("400x300")

        self.cpu_value_label = Label(root, text="CPU Usage:")
        self.cpu_value_label.pack(anchor="w")  # 왼쪽 정렬

        self.memory_value_label = Label(root, text="Memory Usage:")
        self.memory_value_label.pack(anchor="w")

        self.disk_value_label = Label(root, text="Disk Usage:")
        self.disk_value_label.pack(anchor="w")

        self.network_delay_value_label = Label(root, text="Network Delay:")
        self.network_delay_value_label.pack(anchor="w")

        # functools.partial을 사용하여 메서드에 대한 참조를 생성
        self.update_labels_partial = partial(self.update_labels)

        # 최초의 호출
        self.update_labels()

    def get_network_delay(self):
        try:
            # 네트워크 응답시간(ms) 측정
            st = psutil.net_connections(kind='inet')
            delay = st[0].fd
            return delay
        except Exception as e:
            print(f"Error getting network delay: {e}")
            return None

    def update_labels(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')

        # 네트워크 응답시간(ms) 측정
        network_delay = self.get_network_delay()

        # 숫자 표시
        self.cpu_value_label.config(text=f"CPU Usage: {cpu_usage:.2f}%")
        self.memory_value_label.config(text=f"Memory Usage: {memory_info.percent:.2f}%")
        self.disk_value_label.config(text=f"Disk Usage: {disk_info.percent:.2f}%")

        if network_delay is not None:
            self.network_delay_value_label.config(text=f"Network Delay: {network_delay} ms")
        else:
            self.network_delay_value_label.config(text="Network Delay: N/A")

        # functools.partial을 사용하여 메서드에 대한 참조를 전달
        self.root.after(1000, self.update_labels_partial)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorGUI(root)
    root.mainloop()
