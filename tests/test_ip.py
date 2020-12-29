"""Test cases for IP address validation."""
from dnsck.dnsck import is_valid_ip_address


def test_valid_ipv4():
    """Tests valid IPv4 address."""
    assert is_valid_ip_address("192.168.0.55") is True


def test_invalid_ipv4():
    """Tests invalid IPv4 address."""
    assert is_valid_ip_address("192.168.0.256") is False


def test_valid_ipv6():
    """Tests valid IPv6 address."""
    assert is_valid_ip_address("::1") is True


def test_invalid_ipv6():
    """Tests invalid IPv6 address."""
    assert is_valid_ip_address("::Z") is False
