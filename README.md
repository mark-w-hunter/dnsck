# Dnsck

[![Build Status](https://travis-ci.com/mark-w-hunter/dnsck.svg?branch=devel)](https://travis-ci.com/mark-w-hunter/dnsck)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This program performs automated DNS queries from command-line input

## usage

dnsck.py -s server_ip domain_name -t record_type -i num_iterations --tcp

Note: -s and domain_name parameters are mandatory, -t (default A), -i (default 30) and --tcp (default udp) are optional.

Python 3.6 or higher required.

### Examples

Perform 300 queries to resolver 8.8.8.8 for foo.org AAAA records

```bash
./dnsck.py -s 8.8.8.8 foo.org -t AAAA -i 300
```

Perfom 30 queries to resolver 1.1.1.1 for www.foo.org A records

```bash
python3 dnsck.py -s 1.1.1.1 www.foo.org
```

Perfom 10 TCP queries to resolver 192.168.0.1 for local.org TXT records

```bash
./dnsck.py -s 192.168.0.1 local.org -t txt -i 10 --tcp
```

Display help

```bash
./dnsck.py --help
```

## functions

dnsck_query_udp(dns_server, dns_query, record_type, iterations)

- Perform a UDP DNS query for a set number of iterations  
