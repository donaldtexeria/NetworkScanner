import subprocess
import http.client
import json
import urllib
import urllib.parse

def get_ipv4(domain):
    addresses = []
    result = subprocess.check_output(["nslookup", domain, "8.8.8.8"], timeout=2, stderr = subprocess.STDOUT).decode("utf-8")
    if "Non-authoritative answer:" in result:
        result = result.split("Non-authoritative answer:")[1]
    else:
        return addresses
    result = result.split('\n')
    for line in result:
        if "Address:" in line:
            address = line.split("Address:")[1].strip()
            addresses.append(address)
    return addresses

def get_ipv6(domain):
    addresses = []
    result = subprocess.check_output(["nslookup", "-type=AAAA", domain, "8.8.8.8"], timeout=2, stderr = subprocess.STDOUT).decode("utf-8")
    result = result.split('\n')
    for line in result:
        if "has AAAA address" in line:
            address = line.split("has AAAA address")[1].strip()
            addresses.append(address)
    return addresses

def get_server_header(domain):
    url = domain
    if "://" in url:
        url = url.split("://")[1]
    host, path = url.split("/", 1) if "/" in url else (url, "")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    conn = http.client.HTTPSConnection(host, timeout=5)
    try:
        conn.request("HEAD", "/" + path, headers=headers)
        response = conn.getresponse()
        header = response.getheader("Server")
        conn.close()
        return header
    except Exception as e:
        return None
    
def check_insecure_HTTP(domain):
    conn = http.client.HTTPConnection(domain, timeout=5, port=80)
    try:
        conn.request("HEAD", "/")
        response = conn.getresponse()
        conn.close()
        return True
    except:
        return False
    
def follow_redirects(domain, port = 80):
    current_redirects = 0
    while current_redirects < 10:
        #print("redirect number:", current_redirects)
        conn = http.client.HTTPConnection(domain, port, timeout=5)
        conn.request("HEAD", "/")
        response = conn.getresponse()
        location = response.getheader("Location")
        if location:
            loc = urllib.parse.urlparse(location)
            if loc.scheme == "https":
                return True
            domain = loc.netloc
            port = 80 if loc.scheme == 'http' else 443
            current_redirects += 1
        else:
            conn.close()
            break
        conn.close()
    return False

def check_hsts(domain, port=80):
    current_redirects = 0
    try:
        while current_redirects < 10:
            #print("redirect number:", current_redirects)
            if port == 80:
                conn = http.client.HTTPConnection(domain, port, timeout=5)
            else:
                conn = http.client.HTTPSConnection(domain, port, timeout=5)
            conn.request("HEAD", "/")
            response = conn.getresponse()
            location = response.getheader("Location")
            if location:
                loc = urllib.parse.urlparse(location)
                domain = loc.netloc
                if loc.port:
                    domain = domain.split(":")[0]
                #port = 80 if loc.scheme == 'http' else 443
                port = loc.port if loc.port else (80 if loc.scheme == 'http' else 443)

                current_redirects += 1
            else:
                hsts = response.getheader("Strict-Transport-Security")
                if hsts:
                    return True
                return False
        return False
    except:
        return False

def get_tls_versions(domain):
    tls_versions = {"TLSv1.0": "-tls1", "TLSv1.1": "-tls1_1", "TLSv1.2": "-tls1_2", "TLSv1.3": "-tls1_3"}
    try:
        supported_versions = []
        for version, option in tls_versions.items():
            cmd = ["openssl", "s_client", option, "-connect", f"{domain}:443"]
            try:
                result = subprocess.check_output(cmd, input=b'', timeout=2, stderr=subprocess.STDOUT).decode('utf-8')
                supported_versions.append(version)
            except:
                #print("Version", version, "not supported")
                pass
        return supported_versions
    except:
        return []
def get_rootca(domain, port=443):
    cmd = f"echo | openssl s_client -connect {domain}:{port} -servername {domain}"
    result = subprocess.check_output(cmd, timeout=5, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    #print(result)
    result = result.split('\n')[0]
    res = None
    if "O = " in result:
        res = result.split("O = ")[1].split(",")[0]
    return res

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