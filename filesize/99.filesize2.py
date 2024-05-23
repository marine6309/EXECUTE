import os
import shutil

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
    print(f"{size / (1024*1024):.2f} MB")

def main():
    path = input("폴더의 경로를 입력하세요 (예: C:\\): ")
    if os.path.exists(path):
        total_size = 0
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            size = get_size(item_path) if os.path.isdir(item_path) else os.path.getsize(item_path)
            print(f"{item}: ", end="")
            print_size(size)
            total_size += size
        print("\n검색한 드라이브의 총 용량: ", end="")
        print_size(shutil.disk_usage(path).total)
        print("검색한 드라이브의 여유 공간: ", end="")
        print_size(shutil.disk_usage(path).free)
    else:
        print(f"경로를 찾을 수 없습니다: {path}")

if __name__ == '__main__':
    main()
