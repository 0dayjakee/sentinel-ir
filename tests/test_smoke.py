import subprocess
import sys


def test_package_imports():
    import sentinel  # noqa: F401

def test_cli_help():
    r = subprocess.run([sys.executable, "-m", "sentinel", "--help"],
                       capture_output=True, text=True, check=False)
    assert r.returncode == 0
