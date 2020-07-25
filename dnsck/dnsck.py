#!/usr/bin/env python3

# dnsck: Perform automated DNS queries
# author: Mark W. Hunter
# https://github.com/mark-w-hunter/dnsck
#
# The MIT License (MIT)
#
# Copyright (c) 2020 Mark W. Hunter
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""This program performs automated DNS queries from command-line input."""
import sys
import time
from itertools import groupby
from dns import query, message, rcode, exception, rdatatype

AUTHOR = "Mark W. Hunter"
VERSION = "0.21"
DEFAULT_RECORD_TYPE = "A"
DEFAULT_ITERATIONS = 30


def dnsck_query_udp(dns_server, dns_query, record_type, iterations):
    """Perform a UDP DNS query for a set number of iterations."""
    result_code_list = []
    query_times = []
    record_number = 0
    response_errors = 0
    iteration_count = 0

    try:
        make_dns_query = message.make_query(dns_query, record_type.upper(), use_edns=True)
    except rdatatype.UnknownRdatatype:
        print("Unknown record type, try again.")
        sys.exit()
    print(
        f"Performing {iterations} queries to server {dns_server} for domain {dns_query}",
        f"with record type {record_type.upper()}.\n"
    )

    try:
        for iteration in range(iterations):
            print(f"[Query {iteration + 1}]")
            try:
                dns_response = query.udp(make_dns_query, dns_server, timeout=10)
                if dns_response.answer:
                    for answer in dns_response.answer:
                        print(answer)
                        record_number = len(answer)
                else:
                    print("No records returned.")
                elapsed_time = dns_response.time * 1000
                if elapsed_time < 500:
                    result_code = rcode.to_text(dns_response.rcode())
                    result_code_list.append(result_code)
                    iteration_count += 1
                else:
                    result_code = "Degraded"
                    result_code_list.append(result_code)
                    iteration_count += 1
                    response_errors += 1
            except exception.Timeout:
                print("Query timeout.")
                result_code = "Timeout"
                result_code_list.append(result_code)
                elapsed_time = 10000
                iteration_count += 1
                response_errors += 1
            time.sleep(1)
            query_times.append(elapsed_time)
            print(f"Records returned: {record_number}")
            print(f"Response time: {elapsed_time:.2f} ms")
            print(f"Response status: {result_code}\n")
    except KeyboardInterrupt:
        print("Program terminating...")

    rcode_list_final = [(len(list(rcount)), rname) for rname, rcount in
                        groupby(sorted(result_code_list))]

    print("Response status breakdown:")
    for count, query_rcode in rcode_list_final:
        print(f"{count} {query_rcode}")
    print(
        f"\nSummary: Performed {iteration_count} queries to server {dns_server}",
        f"for domain {dns_query} with record type {record_type.upper()}.",
        f"\nResponse errors: {response_errors / iteration_count * 100:.2f}%",
    )
    print(f"Average response time: {sum(query_times) / len(query_times):.2f} ms\n")

    if response_errors:
        return 1
    else:
        return 0


def dnsck_query_tcp(dns_server, dns_query, record_type, iterations):
    """Perform a TCP DNS query for a set number of iterations."""
    result_code_list = []
    query_times = []
    record_number = 0
    response_errors = 0
    iteration_count = 0

    try:
        make_dns_query = message.make_query(dns_query, record_type.upper())
    except rdatatype.UnknownRdatatype:
        print("Unknown record type, try again.")
        sys.exit()
    print(
        f"Performing {iterations} TCP queries to server {dns_server} for domain name {dns_query}",
        f"with record type {record_type.upper()}.\n"
    )

    try:
        for iteration in range(iterations):
            print(f"[Query {iteration + 1}]")
            try:
                dns_response = query.tcp(make_dns_query, dns_server, timeout=10)
                if dns_response.answer:
                    for answer in dns_response.answer:
                        print(answer)
                        record_number = len(answer)
                else:
                    print("No records returned.")
                elapsed_time = dns_response.time * 1000
                if elapsed_time < 500:
                    result_code = rcode.to_text(dns_response.rcode())
                    result_code_list.append(result_code)
                    iteration_count += 1
                else:
                    result_code = "Degraded"
                    result_code_list.append(result_code)
                    iteration_count += 1
                    response_errors += 1
            except exception.Timeout:
                print("Query timeout.")
                result_code = "Timeout"
                result_code_list.append(result_code)
                elapsed_time = 10000
                iteration_count += 1
                response_errors += 1
            time.sleep(1)
            query_times.append(elapsed_time)
            print(f"Records returned: {record_number}")
            print(f"Response time: {elapsed_time:.2f} ms")
            print(f"Response status: {result_code}\n")
    except KeyboardInterrupt:
        print("Program terminating...")

    rcode_list_final = [(len(list(rcount)), rname) for rname, rcount in
                        groupby(sorted(result_code_list))]

    print("Response status breakdown:")
    for count, query_rcode in rcode_list_final:
        print(f"{count} {query_rcode}")
    print(
        f"\nSummary: Performed {iteration_count} TCP queries to server {dns_server}",
        f"for domain name {dns_query} with record type {record_type.upper()}.",
        f"\nResponse errors: {response_errors / iteration_count * 100:.2f}%",
    )
    print(f"Average response time: {sum(query_times) / len(query_times):.2f} ms\n")

    if response_errors:
        return 1
    else:
        return 0


if __name__ == "__main__":
    if len(sys.argv) > 3 and "--tcp" not in sys.argv:
        if sys.argv[1] == "-s" and len(sys.argv) == 4:
            dnsck_query_udp(sys.argv[2], sys.argv[3], DEFAULT_RECORD_TYPE, DEFAULT_ITERATIONS)
        elif sys.argv[1] == "-s" and sys.argv[4] == "-t" and len(sys.argv) == 6:
            dnsck_query_udp(sys.argv[2], sys.argv[3], sys.argv[5], DEFAULT_ITERATIONS)
        elif sys.argv[1] == "-s" and sys.argv[4] == "-i" and len(sys.argv) == 6:
            dnsck_query_udp(sys.argv[2], sys.argv[3], DEFAULT_RECORD_TYPE, int(sys.argv[5]))
        elif sys.argv[1] == "-s" and sys.argv[4] == "-t" and sys.argv[6] == "-i":
            dnsck_query_udp(sys.argv[2], sys.argv[3], sys.argv[5], int(sys.argv[7]))
        elif sys.argv[1] == "-s" and sys.argv[4] == "-i" and sys.argv[6] == "-t":
            dnsck_query_udp(sys.argv[2], sys.argv[3], sys.argv[7], int(sys.argv[5]))
        else:
            print("Run dnsck.py -h for help.")
    elif len(sys.argv) > 3 and "--tcp" in sys.argv:
        if sys.argv[1] == "-s" and len(sys.argv) == 5:
            dnsck_query_tcp(sys.argv[2], sys.argv[3], DEFAULT_RECORD_TYPE, DEFAULT_ITERATIONS)
        elif sys.argv[1] == "-s" and sys.argv[4] == "-t" and len(sys.argv) == 7:
            dnsck_query_tcp(sys.argv[2], sys.argv[3], sys.argv[5], DEFAULT_ITERATIONS)
        elif sys.argv[1] == "-s" and sys.argv[4] == "-i" and len(sys.argv) == 7:
            dnsck_query_tcp(sys.argv[2], sys.argv[3], DEFAULT_RECORD_TYPE, int(sys.argv[5]))
        elif sys.argv[1] == "-s" and sys.argv[4] == "-t" and sys.argv[6] == "-i":
            dnsck_query_tcp(sys.argv[2], sys.argv[3], sys.argv[5], int(sys.argv[7]))
        elif sys.argv[1] == "-s" and sys.argv[4] == "-i" and sys.argv[6] == "-t":
            dnsck_query_tcp(sys.argv[2], sys.argv[3], sys.argv[7], int(sys.argv[5]))
        else:
            print("Run dnsck.py -h for help.")
    elif len(sys.argv) == 1:
        print("Run dnsck.py -h for help.")
    elif sys.argv[1] == "--version" or sys.argv[1] == "-v":
        print(f"Dnsck version: {VERSION}")
    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(
            "Usage: dnsck.py -s <server ip> <domain name> -t <record type>",
            "-i <number of iterations> --tcp\n"
        )
        print("  --version, -v\t\t\t Display version information and exit")
        print("  --help, -h\t\t\t Display this help text and exit\n")
        print(f"Dnsck {VERSION}, {AUTHOR} (c) 2020")
    else:
        print("Error, try again.")
