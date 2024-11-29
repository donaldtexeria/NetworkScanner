import http.client

import http.client
import urllib.parse

def check_hsts(domain, port=80):
    current_redirects = 0
    while current_redirects < 10:
        print("redirect number:", current_redirects)
        
        # Use the appropriate connection type based on the port
        if port != 443:
            conn = http.client.HTTPConnection(domain, port, timeout=15)
        else:
            conn = http.client.HTTPSConnection(domain, port, timeout=15)
        
        # Make the request
        print("\nDomain:", domain)
        print("a")
        conn.request("GET", "/")
        print("b")
        response = conn.getresponse()
        print("c")
        location = response.getheader("Location")
        
        if location:
            # Parse the Location header to extract the domain and port
            loc = urllib.parse.urlparse(location)
            
            domain = loc.netloc
            if loc.port:
                domain = domain.split(":")[0]
                
            print("new domain:", location)
            
            # Extract port from the location, if specified (default is None)
            port = loc.port if loc.port else (80 if loc.scheme == 'http' else 443)
            current_redirects += 1
        else:
            # Check for HSTS header
            hsts = response.getheader("Strict-Transport-Security")
            if hsts:
                return True
            return False
        conn.close()
    
    return False


if __name__ == "__main__":
    url = "homedepot.com"
    server_header = check_hsts(url)
    print(f"hst? {url}: {server_header}")
