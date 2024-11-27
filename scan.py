import sys
import json
import time

def scan_domain(domain):
    """
    Perform a basic scan on the domain and return a dictionary of results.
    Currently, this function only records the scan time.
    """
    scan_results = {
        "scan_time": time.time(),  # Record the scan time in UNIX epoch seconds
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
        # Read domains from the input file
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
        json.dump(scan_results, file, sort_keys=True, indent=4)
    
    print(f"Scan results saved to '{output_file}'.")

if __name__ == "__main__":
    main()
