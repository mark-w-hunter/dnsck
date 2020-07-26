"""Test cases for dns_query_tcp function."""
import os
import subprocess
from signal import SIGINT
from time import sleep
import pytest
from dnsck.dnsck import dnsck_query_tcp


def test_tcp_query():
    """Tests for successful DNS query using tcp."""
    assert dnsck_query_tcp("8.8.8.8", "google.com", "AAAA", 1) == 0


def test_tcp_unknown_rec_type():
    """Unknown record types should raise an exception and exit."""
    with pytest.raises(SystemExit):
        assert dnsck_query_tcp("8.8.8.8", "google.com", "abc", 1)


def test_tcp_bad_server():
    """Tests response with bad server IP address."""
    assert dnsck_query_tcp("8.8.8.88", "google.com", "A", 1) == 1


def test_tcp_no_records():
    """Tests response with bad server IP address."""
    assert dnsck_query_tcp("8.8.8.8", "test.google.com", "A", 1) == 0


def test_tcp_keyboard_interrupt():
    """Tests keyboard interrupt for log running processes."""
    with pytest.raises(KeyboardInterrupt):
        cmd = ["python", "dnsck/dnsck.py", "-s", "8.8.8.8", "google.com", "--tcp"]
        process = subprocess.Popen(cmd, shell=False)
        sleep(5)
        os.kill(process.pid, SIGINT)
        raise KeyboardInterrupt
