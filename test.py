import http.client
import subprocess

import urllib.parse

def get_rdns_names(ips):
    names = []
    for ip in ips:
        cmd = ["dig", "-x", ip]
        result = subprocess.check_output(cmd, timeout=2, stderr=subprocess.STDOUT).decode('utf-8')
        if "ANSWER SECTION" not in result:
            continue
        result = result.split("ANSWER SECTION:")[1].strip().split('\n')
        for line in result:
            if "PTR" not in line:
                break
            name = line.split("PTR")[1].strip()
            names.append(name)
    return names


if __name__ == "__main__":
    ips = [
            "8.8.8.8#53",
            "142.250.65.174"
        ]
    names = get_rdns_names(ips)
    print(names)
