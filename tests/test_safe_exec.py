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
