# NAME : PC TIME USAGE TOOL
# 2024/05/28 - 최초 개발

import win32evtlog
import csv
from datetime import datetime, timedelta
from collections import defaultdict
import socket
import psutil

def print_header(host, ip_address):
    print("=" * 50)
    print(f"HOST : {host} | IP : {ip_address}")
    print("=" * 50)

def get_host_info():
    host = socket.gethostname()
    ip_address = socket.gethostbyname(host)
    return host, ip_address

def get_event_logs(server, logtype):
    logs = []
    hand = win32evtlog.OpenEventLog(server, logtype)
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    while True:
        try:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if not events:
                break
            for event in events:
                logs.append(event)
        except Exception as e:
            print(f"An error occurred while reading the event log: {e}")
            break
    
    return logs

def parse_event(event):
    try:
        event_data = {
            'TimeGenerated': event.TimeGenerated.Format(),
            'EventID': event.EventID & 0xFFFF,  # 16비트로 표현되는 이벤트 ID
        }
        return event_data
    except Exception as e:
        print(f"An error occurred while parsing an event: {e}")
        return None

def filter_events(events, event_ids):
    filtered_events = []
    for event in events:
        if (event.EventID & 0xFFFF) in event_ids:  # 필터링 조건 수정
            parsed_event = parse_event(event)
            if parsed_event:
                filtered_events.append(parsed_event)
    return filtered_events

def calculate_usage_times(events):
    # 날짜 형식이 'Thu May 23 17:01:27 2024' 형태일 경우
    date_format = '%a %b %d %H:%M:%S %Y'
    events.sort(key=lambda x: datetime.strptime(x['TimeGenerated'], date_format))
    usage_times = []
    start_time = None

    for event in events:
        if event['EventID'] == 6005:  # System startup
            start_time = datetime.strptime(event['TimeGenerated'], date_format)
        elif event['EventID'] == 6006 and start_time:  # System shutdown
            end_time = datetime.strptime(event['TimeGenerated'], date_format)
            usage_time = (end_time - start_time).total_seconds() / 3600.0  # 사용 시간을 시간 단위로 계산
            usage_times.append({
                'StartTime': start_time,
                'EndTime': end_time,
                'UsageTimeHours': usage_time
            })
            start_time = None

    return usage_times

def aggregate_daily_usage(usage_times):
    daily_usage = defaultdict(float)
    for usage in usage_times:
        start_date = usage['StartTime'].date()
        end_date = usage['EndTime'].date()
        if start_date == end_date:
            daily_usage[start_date] += usage['UsageTimeHours']
        else:
            # Split usage time across multiple days
            end_of_start_date = datetime.combine(start_date, datetime.max.time())
            start_of_end_date = datetime.combine(end_date, datetime.min.time())
            daily_usage[start_date] += (end_of_start_date - usage['StartTime']).total_seconds() / 3600.0
            daily_usage[end_date] += (usage['EndTime'] - start_of_end_date).total_seconds() / 3600.0
    return daily_usage

def save_usage_times_to_csv(usage_times, filename):
    if not usage_times:
        print("No usage times to save.")
        return

    keys = usage_times[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(usage_times)

def format_hours_to_hhmm(hours):
    total_minutes = int(hours * 60)
    hh = total_minutes // 60
    mm = total_minutes % 60
    return f"{hh:02}:{mm:02}"

def generate_usage_graph(hours):
    units = int(hours)
    remainder = hours - units
    if units == 0:  # 1시간 미만의 경우
        return '-'
    graph = "*" * units
    if remainder >= 0.5:
        graph += "*"
    return ' '.join([graph[i:i+5] for i in range(0, len(graph), 5)])

def get_system_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    return uptime

if __name__ == "__main__":
    host, ip_address = get_host_info()
    print_header(host, ip_address)
    server = 'localhost'
    logtype = 'System'
    event_ids = [6005, 6006]  # Event IDs for system startup (6005) and shutdown (6006)

    logs = get_event_logs(server, logtype)
    print("Number of events read:", len(logs))

    filtered_logs = filter_events(logs, event_ids)
    print("Number of filtered events:", len(filtered_logs))
    
    if filtered_logs:
        usage_times = calculate_usage_times(filtered_logs)
        # save_usage_times_to_csv(usage_times, 'system_usage_times.csv')
        # print(f"Usage times saved to 'system_usage_times.csv'")

        daily_usage = aggregate_daily_usage(usage_times)
        
        # 일별 사용 시간을 화면에 표시 (마지막 7개)
        print("\nDaily Usage Times - Last 7 Entries:")
        last_7_entries = sorted(daily_usage.items())[-7:]
        today_usage = None
        for date, hours in last_7_entries:
            formatted_hours = format_hours_to_hhmm(hours)
            graph = generate_usage_graph(hours)
            print(f"{date}: {formatted_hours} [{graph:<14}]")
            if date == datetime.today().date():
                today_usage = hours

        # 시스템 업타임 계산 및 표시
        uptime = get_system_uptime()
        uptime_hours = uptime.total_seconds() / 3600.0
        uptime_str = str(uptime).split('.')[0]  # 소수점 이하를 제외하고 출력
        print("\nUptime:", uptime_str)
        
        if today_usage is not None:
            today_total_usage = today_usage + uptime_hours
            today_total_usage_formatted = format_hours_to_hhmm(today_total_usage)
            graph = generate_usage_graph(today_total_usage)
            print(f"Today Usage: {today_total_usage_formatted} [{graph:<14}]")
        
        print()  # 한 줄 띄우기
        input("Press Enter to exit...")
    else:
        print("No events to save.")
