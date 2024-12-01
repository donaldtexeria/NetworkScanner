import http.client
import subprocess

import urllib.parse

def get_rootca(domain, port=443):
    cmd = ["openssl", "s_client", "-connect", f"{domain}:{port}", "-servername", domain]
    result = subprocess.check_output(cmd, input=b"", timeout=5, stderr=subprocess.STDOUT).decode('utf-8')
    print(result)
    result = result.split('\n')[0]
    res = None
    if "O = " in result:
        res = result.split("O = ")[1].split(",")[0]
    return res


if __name__ == "__main__":
    url = "imdb.com"
    root_ca = get_rootca(url)
    print(root_ca)
