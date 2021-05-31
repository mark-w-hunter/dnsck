"""Test cases for dns_query_tcp function."""
import os
import subprocess
from signal import SIGINT
from time import sleep
import pytest
from dnsck.dnsck import dnsck_query


def test_tcp_query():
    """Tests for successful DNS query using tcp."""
    assert dnsck_query("8.8.8.8", "google.com", "AAAA", 1, True) == 0


def test_tcp_unknown_rec_type():
    """Unknown record types should raise an exception and exit."""
    with pytest.raises(SystemExit):
        assert dnsck_query("8.8.8.8", "google.com", "abc", 1, True)


def test_tcp_bad_server():
    """Tests response with bad server IP address."""
    assert dnsck_query("8.8.8.88", "google.com", "A", 1, True) == 1


def test_tcp_no_records():
    """Tests response with no records returned."""
    assert dnsck_query("8.8.8.8", "test.google.com", "A", 1, True) == 0


def test_tcp_keyboard_interrupt():
    """Tests keyboard interrupt for log running processes."""
    with pytest.raises(KeyboardInterrupt):
        cmd = ["python", "dnsck/dnsck.py", "-s", "8.8.8.8", "google.com", "--tcp"]
        process = subprocess.Popen(cmd, shell=False)
        sleep(3)
        os.kill(process.pid, SIGINT)
        raise KeyboardInterrupt


def test_tcp_alt_rectype():
    """Tests alternate record type in command-line parameter."""
    cmd = [
        "python",
        "dnsck/dnsck.py",
        "-s",
        "8.8.8.8",
        "google.com",
        "-t",
        "txt",
        "--tcp",
        "--iter",
        "1",
    ]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_tcp_alt_iteration():
    """Tests alternate iteration in command-line parameter."""
    cmd = [
        "python",
        "dnsck/dnsck.py",
        "-s",
        "8.8.8.8",
        "google.com",
        "-i",
        "2",
        "--tcp",
    ]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_tcp_alt_rectype_and_iteration():
    """Tests alternate record type and iteration in command-line parameter."""
    cmd = [
        "python",
        "dnsck/dnsck.py",
        "-s",
        "8.8.8.8",
        "google.com",
        "-t",
        "NS",
        "-i",
        "1",
        "--tcp",
    ]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_tcp_swap_rectype_and_iteration():
    """Tests swapping record type and iteration parameters."""
    cmd = [
        "python",
        "dnsck/dnsck.py",
        "-s",
        "8.8.8.8",
        "google.com",
        "-i",
        "1",
        "-t",
        "NS",
        "--tcp",
    ]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0
