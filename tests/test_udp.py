import pytest
from dnsck import dnsck_query_udp


def test_udp_query():
    exit_status = dnsck_query_udp("8.8.8.8", "google.com", "a", 1)
    assert exit_status == 0


def test_udp_unknown_rec_type():
    with pytest.raises(SystemExit):
        assert dnsck_query_udp("8.8.8.8", "google.com", "XYZ")
