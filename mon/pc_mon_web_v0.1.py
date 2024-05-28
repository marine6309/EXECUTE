import psutil
import time
import socket
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('/').percent

def get_network_response_time(host="www.naver.com", port=80):
    try:
        start_time = time.time()
        sock = socket.create_connection((host, port), timeout=5)  
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)  
        sock.close()  
        return response_time
    except Exception as e:
        print(f"Error while measuring network response time: {e}")
        return "N/A"

def get_host_ip():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return host_name, ip_address

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def index():
    host, ip_address = get_host_ip()
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    network_response_time = get_network_response_time()
    current_time = get_current_time()
    return render_template('index.html', host=host, ip_address=ip_address, 
                           cpu_usage=cpu_usage, memory_usage=memory_usage, 
                           disk_usage=disk_usage, network_response_time=network_response_time, 
                           current_time=current_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
