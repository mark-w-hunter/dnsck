"""Test cases for command-line input."""
import subprocess


def test_cli_help():
    """Tests help command-line parameter."""
    cmd = ["python", "dnsck/dnsck.py", "-h"]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_cli_help_alt():
    """Tests help command-line parameter."""
    cmd = ["python", "dnsck/dnsck.py", "--help"]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_cli_version():
    """Tests version command-line parameter."""
    cmd = ["python", "dnsck/dnsck.py", "-v"]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_cli_version_alt():
    """Tests help command-line parameter."""
    cmd = ["python", "dnsck/dnsck.py", "--version"]
    process = subprocess.run(cmd, shell=False, check=True)
    assert process.returncode == 0


def test_cli_no_param():
    """Tests command-line input with no parameters."""
    cmd = ["python", "dnsck/dnsck.py"]
    process = subprocess.run(cmd, shell=False, check=False)
    assert process.returncode == 2


def test_cli_extra_param():
    """Tests command-line input with extra parameter."""
    cmd = ["python", "dnsck/dnsck.py", "-s", "8.8.8.8", "google.com", "-x"]
    process = subprocess.run(cmd, shell=False, check=False)
    assert process.returncode == 2


def test_cli_extra_param_tcp():
    """Tests command-line input with extra parameter and --tcp specified."""
    cmd = ["python", "dnsck/dnsck.py", "-s", "2001:4860:4802:34::a", "google.com", "--tcp", "-y"]
    process = subprocess.run(cmd, shell=False, check=False)
    assert process.returncode == 2


def test_cli_invalid_param():
    """Tests command-line input with invalid parameter."""
    cmd = ["python", "dnsck/dnsck.py", "-x", "8.8.8.8"]
    process = subprocess.run(cmd, shell=False, check=False)
    assert process.returncode == 2


def test_cli_invalid_ipv4_address():
    """Tests command-line input with invalid IPv4 address."""
    cmd = ["python", "dnsck/dnsck.py", "-s", "8.8.8", "google.com"]
    process = subprocess.run(cmd, shell=False, check=False)
    assert process.returncode == 2


def test_cli_invalid_ipv6_address():
    """Tests command-line input with invalid IPv6 address."""
    cmd = ["python", "dnsck/dnsck.py", "-s", "2001:4860:4802:34::ag", "google.com"]
    process = subprocess.run(cmd, shell=False, check=False)
    assert process.returncode == 2


def test_cli_valid_ipv6_address():
    """Tests command-line input with valid IPv6 address."""
    cmd = [
        "python", "dnsck/dnsck.py", "-s", "::1", "google.com"
    ]
    process = subprocess.run(cmd, shell=False, check=False)
    assert process.returncode == 0
