import subprocess

def main():
    result = subprocess.check_output(["nslookup", "yahoo.com", "8.8.8.8"], timeout=2, stderr = subprocess.STDOUT).decode("utf-8")
    print(result)
    
if __name__ == "__main__":
    main()