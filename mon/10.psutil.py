import psutil

# CPU 정보 얻기
cpu_count = psutil.cpu_count()  # 논리 CPU 코어 수
print("CPU 코어 수:", cpu_count)

cpu_percent = psutil.cpu_percent()  # 현재 CPU 사용량
print("현재 CPU 사용량:", cpu_percent)

# 시스템 메모리 정보 얻기
mem = psutil.virtual_memory()
print("총 메모리:", mem.total)
print("사용 가능한 메모리:", mem.available)

# 디스크 정보 얻기
disk_usage = psutil.disk_usage('/')
print("디스크 사용량:", disk_usage.used)
print("디스크 총 용량:", disk_usage.total)

# 네트워크 정보 얻기
net_io = psutil.net_io_counters()
print("네트워크 송신량:", net_io.bytes_sent)
print("네트워크 수신량:", net_io.bytes_recv)

# # 모든 프로세스 리스트 얻기
# for proc in psutil.process_iter():
#     print(proc.name())

# # 특정 프로세스 CPU 사용량 얻기
# pid = 0  # 프로세스 ID
# process = psutil.Process(pid)
# cpu_usage = process.cpu_percent()
# print("프로세스 CPU 사용량:", cpu_usage)
