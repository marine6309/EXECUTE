import os

def convert_bytes_to_mb(bytes):
    mb = bytes / (1024 * 1024)
    return mb

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except FileNotFoundError:
                print(f"파일을 찾을 수 없습니다: {fp}")
    return total_size

def display_folder_contents(folder_path):
    print(f"폴더 경로: {folder_path}")
    print("하위 폴더와 파일:")
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for dirname in dirnames:
            print(os.path.join(dirpath, dirname))
        for filename in filenames:
            print(os.path.join(dirpath, filename))
    print()

def display_drive_contents(drive):
    print(f"디스크 루트: {drive}")
    print("디스크 내 하위 폴더와 파일:")
    for dirpath, dirnames, filenames in os.walk(drive):
        for dirname in dirnames:
            print(os.path.join(dirpath, dirname))
        for filename in filenames:
            print(os.path.join(dirpath, filename))
    print()

def main():
    folder_path = input("폴더 경로를 입력하세요: ")
    if not os.path.exists(folder_path):
        print("입력한 경로가 존재하지 않습니다.")
        return
    
    if os.path.isdir(folder_path):
        if os.path.splitdrive(folder_path)[1] == '\\':
            drive = os.path.splitdrive(folder_path)[0]
            display_drive_contents(drive)
        else:
            display_folder_contents(folder_path)
            total_size = get_folder_size(folder_path)
            total_size_mb = convert_bytes_to_mb(total_size)
            print(f"폴더 크기: {total_size_mb:.2f} MB")
    else:
        print("폴더 경로를 입력해주세요.")

if __name__ == "__main__":
    main()
