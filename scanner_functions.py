import subprocess
import http.client
import json
import urllib
import urllib.parse
def get_ipv4(domain):
    addresses = []
    result = subprocess.check_output(["nslookup", domain, "8.8.8.8"], timeout=2, stderr = subprocess.STDOUT).decode("utf-8")
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
        conn.request("GET", "/" + path, headers=headers)
        response = conn.getresponse()
        header = response.getheader("Server")
        conn.close()
        return header
    except Exception as e:
        return None
    
def check_insecure_HTTP(domain):
    conn = http.client.HTTPConnection(domain, timeout=5, port=80)
    try:
        conn.request("GET", "/")
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
        conn.request("GET", "/")
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
            conn.request("GET", "/")
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
        

        