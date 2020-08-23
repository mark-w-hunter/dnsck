"""Test cases for dns_query_udp function."""
import os
import subprocess
from signal import SIGINT
from time import sleep
import pytest
from dnsck.dnsck import dnsck_query_udp


def test_udp_query():
    """Tests for successful DNS query using UDP."""
    assert dnsck_query_udp("8.8.8.8", "google.com", "a", 1) == 0


def test_udp_unknown_rec_type():
    """Unknown record types should raise an exception and exit."""
    with pytest.raises(SystemExit):
        assert dnsck_query_udp("8.8.8.8", "google.com", "XYZ", 1)


def test_udp_bad_server():
    """Tests response with bad server IP address."""
    assert dnsck_query_udp("8.8.8.88", "google.com", "A", 1) == 1


def test_udp_no_records():
    """Tests response with no records returned."""
    assert dnsck_query_udp("8.8.8.8", "test.google.com", "A", 1) == 0


def test_udp_keyboard_interrupt():
    """Tests keyboard interrupt for log running processes."""
    with pytest.raises(KeyboardInterrupt):
        cmd = ["python", "dnsck/dnsck.py", "-s", "8.8.8.8", "google.com"]
        process = subprocess.Popen(cmd, shell=False)
        sleep(3)
        os.kill(process.pid, SIGINT)
        raise KeyboardInterrupt


def test_udp_alt_rectype():
    """Tests alternate record type in command-line parameter."""
    cmd = ["python", "dnsck/dnsck.py", "-s", "8.8.8.8",
           "google.com", "-t", "txt", "-i", "1"]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_udp_alt_iteration():
    """Tests alternate iteration in command-line parameter."""
    cmd = ["python", "dnsck/dnsck.py", "-s", "8.8.8.8", "google.com", "-i", "1"]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_udp_alt_rectype_and_iteration():
    """Tests alternate record type and iteration in command-line parameter."""
    cmd = ["python", "dnsck/dnsck.py", "-s", "8.8.8.8",
           "google.com", "-t", "soa", "-i", "2"]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_udp_swap_rectype_and_iteration():
    """Tests swapping record type and iteration parameters."""
    cmd = ["python", "dnsck/dnsck.py", "-s", "8.8.8.8",
           "google.com", "-i", "1", "-t", "soa"]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0
