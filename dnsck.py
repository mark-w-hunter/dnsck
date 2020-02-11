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


"""This program performs automated DNS queries from command-line input"""
import sys
import time
import timeit
from itertools import groupby
from dns import query
from dns import message
from dns import rcode
from dns import exception

AUTHOR = "Mark W. Hunter"
VERSION = "0.14"
DEFAULT_RECORD_TYPE = "A"
DEFAULT_ITERATIONS = 30


def dnsck_query_udp(dns_server, dns_query, record_type, iterations):
    """Perform a UDP DNS query for a set number of iterations"""
    result_code_list = []
    query_times = []
    response_errors = 0
    iteration_count = 0
    make_dns_query = message.make_query(dns_query, record_type.upper())
    make_dns_query.use_edns()
    print(
        f"Performing {iterations} queries to server {dns_server} for domain {dns_query}",
        f"with record type {record_type.upper()}.\n"
    )

    try:
        for iteration in range(iterations):
            print(f"[Query {iteration + 1}]")
            start_time = timeit.default_timer()
            try:
                dns_response = query.udp(make_dns_query, dns_server, timeout=10)
                if dns_response.answer:
                    for answer in dns_response.answer:
                        print(answer)
                else:
                    print("No records returned")
                result_code = rcode.to_text(dns_response.rcode())
                result_code_list.append(result_code)
                iteration_count += 1
            except exception.Timeout:
                print("Query timeout.")
                result_code = "Timeout"
                result_code_list.append(result_code)
                iteration_count += 1
                response_errors += 1
            elapsed_time = (timeit.default_timer() - start_time) * 1000
            time.sleep(1)
            query_times.append(elapsed_time)
            print(f"Response time: {round(elapsed_time, 2)} ms")
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
        f"\nTimeout errors: {response_errors}",
    )
    print(f"Average response time: {round(sum(query_times) / len(query_times), 2)} ms\n")


if __name__ == "__main__":
    # print(len(sys.argv))
    if len(sys.argv) > 4:
        if sys.argv[1] == "-s" and sys.argv[3] == "-d" and len(sys.argv) == 5:
            dnsck_query_udp(sys.argv[2], sys.argv[4], DEFAULT_RECORD_TYPE, DEFAULT_ITERATIONS)
        elif sys.argv[1] == "-s" and sys.argv[3] == "-d" and sys.argv[5] == "-t" and \
                len(sys.argv) == 7:
            dnsck_query_udp(sys.argv[2], sys.argv[4], sys.argv[6], DEFAULT_ITERATIONS)
        elif sys.argv[1] == "-s" and sys.argv[3] == "-d" and sys.argv[5] == "-i" and \
                len(sys.argv) == 7:
            dnsck_query_udp(sys.argv[2], sys.argv[4], DEFAULT_RECORD_TYPE, int(sys.argv[6]))
        elif sys.argv[1] == "-s" and sys.argv[3] == "-d" and \
                sys.argv[5] == "-t" and sys.argv[7] == "-i":
            dnsck_query_udp(sys.argv[2], sys.argv[4], sys.argv[6], int(sys.argv[8]))
        elif sys.argv[1] == "-s" and sys.argv[3] == "-d" and \
                sys.argv[5] == "-i" and sys.argv[7] == "-t":
            dnsck_query_udp(sys.argv[2], sys.argv[4], sys.argv[8], int(sys.argv[6]))
        else:
            print("Run dnsck.py -h for help.")
    elif len(sys.argv) == 1:
        print("Run dnsck.py -h for help.")
    elif sys.argv[1] == "--version" or sys.argv[1] == "-v":
        print(f"Dnsck version: {VERSION}")
    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(
            "Usage: dnsck.py -s <server ip> -d <domain name> -t <record type>",
            "-i <number of iterations>\n"
        )
        print("  --version, -v\t\t\t Display version information and exit")
        print("  --help, -h\t\t\t Display this help text and exit\n")
        print(f"Dnsck {VERSION}, {AUTHOR} (c) 2020")
    else:
        print("Error, try again.")
