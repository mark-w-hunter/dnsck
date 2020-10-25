"""Unit test cases for IP address validation."""
import unittest
from dnsck.dnsck import is_valid_ipv4_address, is_valid_ipv6_address


class TestIPAddressValidation(unittest.TestCase):
    """Tests validation of IP address input"""

    def test_valid_ipv4(self):
        """Tests valid IPv4 address."""
        self.assertEqual(is_valid_ipv4_address("192.168.0.55"), True)

    def test_invalid_ipv4(self):
        """Tests invalid IPv4 address."""
        self.assertEqual(is_valid_ipv4_address("192.168.0.256"), False)

    def test_valid_ipv6(self):
        """Tests valid IPv6 address."""
        self.assertEqual(is_valid_ipv6_address("::1"), True)

    def test_invalid_ipv6(self):
        """Tests invalid IPv6 address."""
        self.assertEqual(is_valid_ipv6_address("::Z"), False)


# unittest.main()
