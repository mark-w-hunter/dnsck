"""Test cases for dns_query_udp function."""
import pytest
from dnsck import dnsck_query_udp


def test_udp_query():
    """Tests for successful DNS query using UDP."""
    assert dnsck_query_udp("8.8.8.8", "google.com", "a", 1) == 0


def test_udp_unknown_rec_type():
    """Unknown record types should raise an exception and exit."""
    with pytest.raises(SystemExit):
        assert dnsck_query_udp("8.8.8.8", "google.com", "XYZ", 1)
