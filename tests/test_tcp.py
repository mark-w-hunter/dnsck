import pytest
from dnsck import dnsck_query_tcp


def test_tcp_query():
    exit_status = dnsck_query_tcp("8.8.8.8", "google.com", "AAAA", 1)
    assert exit_status == 0


def test_tcp_unknown_rec_type():
    with pytest.raises(SystemExit):
        assert dnsck_query_tcp("8.8.8.8", "google.com", "ABC")
