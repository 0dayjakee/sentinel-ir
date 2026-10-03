import pytest

from sentinel.safe_exec import run_command


@pytest.mark.parametrize(
    "cmd",
    [
        "rm -rf /",
        "cat /etc/passwd",
        "strings /etc/passwd",
        "strings /cases/../etc/passwd",
        "file --magic-file=/etc/passwd x",
        "",
        "strings 'unterminated",
        "bash -c id",
    ],
)
def test_blocked(cmd):
    assert run_command(cmd).startswith("BLOCKED")


def test_pipe_is_not_interpreted():
    out = run_command("file x | cat /etc/passwd")
    assert "root:" not in out


@pytest.mark.parametrize(
    "argv",
    [
        ["vol", "-f", "/cases/x.raw", "windows.dumpfiles"],
        ["vol", "-f", "/cases/x.raw", "windows.pslist", "-o", "/tmp"],
        ["vol", "-f", "/cases/x.raw", "windows.pslist", "--output-dir=/tmp"],
        ["vol", "-f", "/cases/x.raw", "windows.pslist", "-o/tmp"],
        ["vol", "--plugin-dirs", "/tmp", "-f", "/cases/x.raw", "windows.pslist"],
        ["vol", "-f", "/etc/passwd", "windows.pslist"],
        ["rm", "-rf", "/cases"],
    ],
)
def test_safe_run_blocked(argv):
    from sentinel.safe_exec import safe_run

    assert safe_run(argv).startswith("BLOCKED")
