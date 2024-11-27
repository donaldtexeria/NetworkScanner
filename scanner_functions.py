import subprocess
def get_ipv4(domain):
    addresses = []
    result = subprocess.check_output(["nslookup", domain, "8.8.8.8"], timeout=2, stderr = subprocess.STDOUT).decode("utf-8")
    result = result.split('\n')
    for line in result:
        if "Address:" in line:
            address = line.split("Address:")[1].strip()
            addresses.append(address)
    return addresses