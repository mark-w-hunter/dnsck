# dnsck

[![Build Status](https://travis-ci.com/mark-w-hunter/dnsck.svg?branch=master)](https://travis-ci.com/mark-w-hunter/dnsck)
[![codecov](https://codecov.io/gh/mark-w-hunter/dnsck/branch/master/graph/badge.svg)](https://codecov.io/gh/mark-w-hunter/dnsck)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Perform automated DNS queries from command-line input

## setup

Install package dependencies

```bash
pip install -r requirements.txt
```

*Note:* Python 3.6 or higher is required

## usage

dnsck.py domain [-s server] [-t type] [-i iterations] [--tcp] [--nosleep] [-h] [-v]

The domain argument is mandatory. Additional optional arguments:

- -s, --server (default 8.8.8.8)
- -t, --type (default A)
- -i, --iter (default 30)
- --tcp (default udp)
- --nosleep (default sleep 1 second)

### Examples

Perform 300 queries to resolver 8.8.8.8 for google.com AAAA records

```bash
dnsck/dnsck.py google.com -t AAAA -i 300
```

Perfom 30 queries to resolver 1.1.1.1 for www.amazon.com A records with
no sleep between queries

```bash
python3 dnsck/dnsck.py -s 1.1.1.1 www.amazon.com --nosleep
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

dnsck_query(dns_server, dns_query, record_type, iterations)

- Perform a UDP or TCP DNS query for a set number of iterations

is_valid_ip_address(ip_addr)

- Checks input is a valid IPv4 or IPv6 address

main()

- Main program
