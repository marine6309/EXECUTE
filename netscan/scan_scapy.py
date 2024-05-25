from scapy.all import ARP, Ether, srp
import socket

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def scan_network(ip_range):
    # Create ARP request packet
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

# Get local IP and create the IP range for scanning
local_ip = get_local_ip()
ip_range = local_ip.rsplit('.', 1)[0] + '.1/24'

devices = scan_network(ip_range)
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")
