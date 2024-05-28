import nmap
import socket

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def scan_network(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')
    
    devices = []
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            devices.append({'ip': host, 'mac': nm[host]['addresses']['mac']})
        else:
            devices.append({'ip': host, 'mac': 'N/A'})

    return devices

# Get local IP and create the IP range for scanning
local_ip = get_local_ip()
ip_range = local_ip.rsplit('.', 1)[0] + '.1/24'

devices = scan_network(ip_range)
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")
