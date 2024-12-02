import http.client
import subprocess

import urllib.parse

def get_rtt(ips):
    min_rtt = float('inf')
    max_rtt = 0
    for ip in ips:
        cmd = f"sh -c \"time echo -e \'\\x1dclose\\x0d\' | telnet {ip} 443\""
        result = subprocess.check_output(cmd, timeout=2, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        time = result.split('real')[1].split('\n')[0].strip()
        time = float(time[2:-1])
        time = int(time * 1000)
        if time > max_rtt:
            max_rtt = time
        if time < min_rtt:
            min_rtt = time
    return [min_rtt, max_rtt] 


if __name__ == "__main__":
    ips = [
            "104.21.4.169",
            "172.67.132.72"
        ]
    rtt = get_rtt(ips)
    print(rtt)