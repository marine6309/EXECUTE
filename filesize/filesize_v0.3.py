# NAME : FILE SIZE CHECK TOOL
# 2024/05/23 - 용량천단위구분,시작종료경과시간,폴더와파일구분

import os
import shutil
import time

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                try:
                    total_size += os.path.getsize(fp)
                except FileNotFoundError:
                    pass  # 파일을 찾을 수 없는 경우 건너뛰기
    return total_size

def print_size(size):
    print(f"{size / (1024*1024):,.2f} MB")

def main():
    path = input("폴더의 경로를 입력하세요 (예: C:\\): ")
    
    start_time = time.time()  # 시작 시간 기록
    
    if os.path.exists(path):
        total_size = 0
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print(f"[D] {item}: ", end="")
                size = get_size(item_path)
            else:
                print(f"[F] {item}: ", end="")
                size = os.path.getsize(item_path)
            print_size(size)
            total_size += size
        
        total, used, free = shutil.disk_usage(path)
        
        print("\n검색한 드라이브 총 용량: ", end="")
        print_size(total)
        print("검색한 드라이브 여유 공간: ", end="")
        print_size(free)
        print("검색한 드라이브 사용 공간: ", end="")
        print_size(used)
        print(f"검색한 드라이브 사용률: {used / total * 100:.2f}%")
        
        end_time = time.time()  # 종료 시간 기록
        
        elapsed_time = end_time - start_time  # 경과 시간 계산
        
        # 경과 시간을 HH:MM:SS 형식으로 변환
        elapsed_time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        
        print(f"시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
        print(f"종료 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        print(f"경과 시간: {elapsed_time_str}")
   
        # 종료 전에 사용자 입력을 기다림
        input("계속하려면 Enter 키를 누르세요...")

    else:
        print(f"경로를 찾을 수 없습니다: {path}")

if __name__ == '__main__':
    main()
