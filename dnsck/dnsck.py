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
import argparse
from itertools import groupby
import socket
from dns import query, message, rcode, exception, rdatatype

AUTHOR = "Mark W. Hunter"
VERSION = "0.25"


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
            print(f"[Query {iteration + 1} of {iterations}]")
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

    return response_errors


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
        sys.exit(1)
    print(
        f"Performing {iterations} TCP queries to server {dns_server} for domain name {dns_query}",
        f"with record type {record_type.upper()}.\n"
    )

    try:
        for iteration in range(iterations):
            print(f"[Query {iteration + 1} of {iterations}]")
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

    return response_errors


def is_valid_ipv4_address(address):
    """Checks input is a valid IPv4 address."""
    # credit Stack Overflow user tzot
    # https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python/319298#319298
    try:
        socket.inet_pton(socket.AF_INET, address)
    except socket.error:
        return False
    return True


def is_valid_ipv6_address(address):
    """Checks input is a valid IPv6 address."""
    # credit Stack Overflow user tzot
    # https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python/319298#319298
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    return True


def main():
    """Run main program."""
    dnsck_parser = argparse.ArgumentParser(
        description="Perform automated DNS queries from command-line input"
    )
    dnsck_parser.add_argument("domain", type=str, help="domain name to query")
    dnsck_parser.add_argument("-s",
                              "--server",
                              type=str,
                              help="ip address of server [default: 8.8.8.8]",
                              default="8.8.8.8")
    dnsck_parser.add_argument("-t",
                              "--type",
                              type=str,
                              help="record type [default: A]",
                              default="A")
    dnsck_parser.add_argument("-i",
                              "--iter",
                              type=int,
                              help="number of iterations [default: 30]",
                              default=30)
    dnsck_parser.add_argument("--tcp", help="use tcp", action="store_true")
    dnsck_parser.add_argument("-v",
                              "--version",
                              action="version",
                              version="%(prog)s " + VERSION + ", " + AUTHOR + " (c) 2020")
    args = dnsck_parser.parse_args()

    if not is_valid_ipv4_address(args.server) and not is_valid_ipv6_address(args.server):
        print("Invalid ip address, try again.")
        sys.exit(2)

    if args.tcp:
        dnsck_query_tcp(args.server, args.domain, args.type, args.iter)
    else:
        dnsck_query_udp(args.server, args.domain, args.type, args.iter)


if __name__ == "__main__":
    main()
