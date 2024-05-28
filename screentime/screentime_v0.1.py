import psutil
import time
import datetime
import json

# 애플리케이션 사용 시간을 저장할 데이터 구조
usage_data = {}

def get_active_window():
    try:
        import win32gui
        import win32process
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            process_name = psutil.Process(pid).name()
            return process_name
        except psutil.NoSuchProcess:
            return None
    except ImportError:
        print("win32gui or win32process module is not installed.")
        return None

def record_usage():
    active_app = get_active_window()
    if active_app:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if current_date not in usage_data:
            usage_data[current_date] = {}
        if active_app not in usage_data[current_date]:
            usage_data[current_date][active_app] = 0
        usage_data[current_date][active_app] += 1

def save_usage_data(filename="usage_data.json"):
    with open(filename, "w") as f:
        json.dump(usage_data, f, indent=4)

def load_usage_data(filename="usage_data.json"):
    global usage_data
    try:
        with open(filename, "r") as f:
            usage_data = json.load(f)
    except FileNotFoundError:
        usage_data = {}

def get_system_uptime():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    now = datetime.datetime.now()
    uptime = now - boot_time
    return uptime

def format_uptime(uptime):
    days, seconds = uptime.days, uptime.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{days} days, {hours} hours, {minutes} minutes"

def print_usage_report():
    print("System Uptime:", format_uptime(get_system_uptime()))
    print("\nDaily Usage Report:")
    for date, apps in usage_data.items():
        print(f"\nDate: {date}")
        for app, seconds in apps.items():
            print(f"  {app}: {seconds // 60} minutes {seconds % 60} seconds")
    print("\nWeekly Usage Report:")
    weekly_usage = calculate_weekly_usage()
    for week, apps in weekly_usage.items():
        print(f"\nWeek starting {week}:")
        for app, seconds in apps.items():
            print(f"  {app}: {seconds // 60} minutes {seconds % 60} seconds")

def calculate_weekly_usage():
    weekly_usage = {}
    for date, apps in usage_data.items():
        week_start = datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=datetime.datetime.strptime(date, "%Y-%m-%d").weekday())
        week_start_str = week_start.strftime("%Y-%m-%d")
        if week_start_str not in weekly_usage:
            weekly_usage[week_start_str] = {}
        for app, seconds in apps.items():
            if app not in weekly_usage[week_start_str]:
                weekly_usage[week_start_str][app] = 0
            weekly_usage[week_start_str][app] += seconds
    return weekly_usage

def main():
    load_usage_data()
    try:
        while True:
            record_usage()
            time.sleep(1)  # 1초마다 체크
    except KeyboardInterrupt:
        print("Exiting and saving usage data...")
        save_usage_data()
        print_usage_report()

if __name__ == "__main__":
    main()
