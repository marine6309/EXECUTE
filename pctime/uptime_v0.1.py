import psutil
import datetime
import os

def get_boot_time():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    return boot_time

def calculate_uptime():
    current_time = datetime.datetime.now()
    boot_time = get_boot_time()
    return current_time - boot_time

def load_uptime_data(file_path):
    uptime_data = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                uptime_data.append(line.strip())
    return uptime_data

def record_and_display_uptime(file_path):
    current_time = datetime.datetime.now()
    boot_time = get_boot_time()
    uptime_today = current_time - boot_time
    hours, remainder = divmod(uptime_today.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    current_date_str = current_time.strftime('%Y-%m-%d')
    current_uptime_str = f"{current_date_str} - {hours:02}:{minutes:02}"

    # 이전 업타임 정보 로드
    uptime_data = load_uptime_data(file_path)

    # 새로운 업타임 정보 추가
    uptime_data.append(current_uptime_str)

    # 파일에 업타임 정보 추가
    with open(file_path, 'w') as file:
        total_hours = 0
        total_minutes = 0
        for uptime_entry in uptime_data:
            file.write(uptime_entry + "\n")
            # 업타임 정보 분석
            entry_date_str, entry_time_str = uptime_entry.split(" - ")
            entry_date = datetime.datetime.strptime(entry_date_str, '%Y-%m-%d')
            entry_hours, entry_minutes = map(int, entry_time_str.split(":"))
            # 현재 날짜의 업타임이 아니면 총 업타임에 추가
            if entry_date.date() != current_time.date():
                total_hours += entry_hours
                total_minutes += entry_minutes

        # 현재 업타임 시간과 기존의 업타임 시간 더하기
        total_hours += hours
        total_minutes += minutes
        # 분 단위가 60 이상이면 시간에 추가
        total_hours += total_minutes // 60
        total_minutes = total_minutes % 60

        # 화면에 총 업타임 표시
        print(f"Total uptime: {total_hours:02} hours {total_minutes:02} minutes")

if __name__ == "__main__":
    log_file_path = "uptime_log.txt"
    record_and_display_uptime(log_file_path)
