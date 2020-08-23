# dnsck

[![Build Status](https://travis-ci.com/mark-w-hunter/dnsck.svg?branch=master)](https://travis-ci.com/mark-w-hunter/dnsck)
[![codecov](https://codecov.io/gh/mark-w-hunter/dnsck/branch/master/graph/badge.svg)](https://codecov.io/gh/mark-w-hunter/dnsck)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Perform automated DNS queries from command-line input

## setup

Install package dependencies

```bash
pip install -r requirements.txt
```

*Note:* Python 3.6 or higher is required

## usage

dnsck.py domain [-s server] [-t type] [-i iterations] [--tcp] [-h] [-v]

Domain name argument is mandatory. Arguments for server -s, --server (default 8.8.8.8), type -t, --type (default A), Iteration -i, --iter (default 30) and --tcp (default udp) are optional.

### Examples

Perform 300 queries to resolver 8.8.8.8 for google.com AAAA records

```bash
dnsck/dnsck.py google.com -t AAAA -i 300
```

Perfom 30 queries to resolver 1.1.1.1 for www.amazon.com A records

```bash
python3 dnsck/dnsck.py -s 1.1.1.1 www.amazon.com
```

Perfom 10 TCP queries to resolver 192.168.0.1 for change.org TXT records

```bash
dnsck/dnsck.py -s 192.168.0.1 change.org -t txt -i 10 --tcp
```

Display help

```bash
dnsck/dnsck.py --help
```

Display version

```bash
dnsck/dnsck.py --version
```

## functions

dnsck_query_udp(dns_server, dns_query, record_type, iterations)

- Perform a UDP DNS query for a set number of iterations

dnsck_query_tcp(dns_server, dns_query, record_type, iterations)

- Perform a TCP DNS query for a set number of iterations

main()

- Main program
