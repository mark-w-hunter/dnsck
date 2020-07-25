"""Test cases for dns_query_tcp function."""
import pytest
from dnsck.dnsck import dnsck_query_tcp


def test_tcp_query():
    """Tests for successful DNS query using UDP."""
    assert dnsck_query_tcp("8.8.8.8", "google.com", "AAAA", 1) == 0


def test_tcp_unknown_rec_type():
    """Unknown record types should raise an exception and exit."""
    with pytest.raises(SystemExit):
        assert dnsck_query_tcp("8.8.8.8", "google.com", "abc", 1)
