import sys
import json
import time
import subprocess
import scanner_functions

def scan_domain(domain):
    ipv4s = scanner_functions.get_ipv4(domain)
    insecure_http = scanner_functions.check_insecure_HTTP(domain)
    redirects = False if not insecure_http else scanner_functions.follow_redirects(domain)

    scan_results = {
        "scan_time": time.time(),  # Record the scan time in UNIX epoch seconds
        "ipv4_addresses": ipv4s,
        "ipv6_addresses": scanner_functions.get_ipv6(domain),
        "http_server": scanner_functions.get_server_header(domain),
        "insecure_http": insecure_http,
        "redirect_to_https": redirects,
        "hsts": scanner_functions.check_hsts(domain),
        "root_ca": scanner_functions.get_rootca(domain),
        "rdns_names": scanner_functions.get_rdns_names(ipv4s)
    }
    return scan_results

def main():
    # Ensure correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python3 scan.py [input_file.txt] [output_file.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, "r") as file:
            domains = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    # Dictionary to store the scan results
    scan_results = {}

    # Scan each domain
    for domain in domains:
        print(f"Scanning domain: {domain}")
        scan_results[domain] = scan_domain(domain)

    # Write the results to the output JSON file
    with open(output_file, "w") as file:
        json.dump(scan_results, file, sort_keys=False, indent=4)
    
    print(f"Scan results saved to '{output_file}'.")

if __name__ == "__main__":
    main()
