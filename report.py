import sys
import texttable
import json
import collections

def make_part2_table(domain_infos):
    table = texttable.Texttable()

    col_labels = ["scan_time", "ipv4_addresses", "ipv6_addresses", "http_server", "insecure_http", "redirect_to_https", "hsts", "tls_versions"]

    table.set_cols_align(["l"] * (len(col_labels) + 1))
    table.set_cols_valign(["t"] * (len(col_labels) + 1))
    first_row = col_labels[:]
    first_row.insert(0, "domain")
    table.add_row(first_row)

    rtt_info = {} #key: domain, value: [min RTT, max RTT]

    for domain in domain_infos:
        info = domain_infos[domain]
        vals = [domain]
        for col in col_labels:
            vals.append(info[col])
        table.add_row(vals)
    
    return table

def make_rtt_table(domain_infos):
    rtt_table = texttable.Texttable()
    rtt_table.set_cols_align(["l"] * 3)

    rtt_ranges = [[domain, domain_infos[domain]["rtt_range"]] for domain in domain_infos]

    sorted(rtt_ranges, key=lambda x: x[1][0])

    for rtt_range in rtt_ranges:
        rtt_table.add_row([rtt_range[0], rtt_range[1][0], rtt_range[1][1]])
    
    return rtt_table

def make_root_ca_table(domain_infos):
    certs = [info["root_ca"] for info in domain_infos.values()]
    counts = collections.Counter(certs)

    root_ca_table = texttable.Texttable()
    root_ca_table.set_cols_align(["c"] * 2)
    root_ca_table.add_row(["certificate", "# of occurrences"])

    for c in counts:
        root_ca_table.add_row([c, counts[c]])

    return root_ca_table

def make_http_server_table(domain_infos):
    servers = [info["http_server"] for info in domain_infos.values()]
    counts = collections.Counter(servers)

    http_server_table = texttable.Texttable()
    http_server_table.set_cols_align(["c"] * 2)
    http_server_table.add_row(["http server", "# of occurrences"])

    for c in counts:
        http_server_table.add_row([c, counts[c]])
    
    return http_server_table

def make_percentages_table(domain_infos):
    table = texttable.Texttable()
    table.set_cols_align(["c", "c"])
    table.add_row(["property", "% of supported domains"])

    properties = {"SSLv2" : 0, "SSLv3" : 0, "TLSv1.0" : 0, "TLSv1.1" : 0, "TLSv1.2" : 0, "TLSv1.3" : 0, "plain_http" : 0, "http_redirect": 0, "hsts" : 0, "ipv6": 0}

    for domain in domain_infos:
        info = domain_infos[domain]
        tls_versions = info["tls_versions"]

        for v in tls_versions:
            properties[v] += 1
        
        properties["plain_http"] += info["insecure_http"]
        properties["http_redirect"] += info["redirect_to_https"]
        properties["hsts"] += info["hsts"]
        properties["ipv6"] += len(info["ipv6_addresses"]) != 0
    
    num_domains = len(domain_infos)
    for p in properties:
        table.add_row([p, f"{properties[p] / num_domains * 100}%"])

    return table

def main(input_file, output_file):
    data = open(input_file)
    domain_infos = json.loads(data.read())

    info_table = make_part2_table(domain_infos)
    rtt_table = make_rtt_table(domain_infos)
    root_ca_table = make_root_ca_table(domain_infos)
    http_server_table = make_http_server_table(domain_infos)
    percentages_table = make_percentages_table(domain_infos)

    #print(info_table.draw())
    #print(rtt_table.draw())
    #print(root_ca_table.draw())
    #print(http_server_table.draw())
    #print(percentages_table.draw())

    with open(output_file, "w") as f:
        f.write("1) Domain info:\n")
        f.write(info_table.draw())

        f.write("\n\n 2) RTT Ranges:\n")
        f.write(rtt_table.draw())

        f.write("\n\n3) Root CA occurrences:\n")
        f.write(root_ca_table.draw())

        f.write("\n\n4) Web server occurrences:\n")
        f.write(http_server_table.draw())

        f.write("\n\n5) Percentages:\n")
        f.write(percentages_table.draw())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 report.py [input_file.json] [output_file.txt]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)