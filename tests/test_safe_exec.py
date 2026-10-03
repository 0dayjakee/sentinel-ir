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


@pytest.mark.parametrize(
    "argv",
    [
        ["vol", "-f", "image.raw", "windows.pslist"],
        ["vol", "-f", "/cases/x.raw", "windows.pslist", "-c", "/tmp/evil.json"],
        ["vol", "-f", "/cases/x.raw", "windows.pslist", "--config=/tmp/evil.json"],
        [
            "vol",
            "-f",
            "/cases/x.raw",
            "windows.pslist",
            "--remote-isf-url",
            "http://evil/x",
        ],
        ["vol", "-f", "/cases/x.raw", "windows.pslist", "-f", "/etc/passwd"],
        [
            "vol",
            "-f",
            "/cases/x.raw",
            "windows.pslist",
            "--single-location=http://evil",
        ],
    ],
)
def test_vol_more_bypasses(argv):
    from sentinel.safe_exec import safe_run

    assert safe_run(argv).startswith("BLOCKED")


def test_vol_args_split_shape_is_safe():
    """Same shape as run_volatility: cmd + args.split() from an LLM string."""
    from sentinel.safe_exec import safe_run

    args = "--pid 4 ; rm -rf /cases && -o /tmp"
    cmd = ["vol", "-f", "/cases/x.raw", "windows.pslist", *args.split()]
    assert safe_run(cmd).startswith("BLOCKED")


def test_vol_flag_in_plugin_position_blocked():
    from sentinel.safe_exec import safe_run

    assert safe_run(
        ["vol", "-f", "/cases/x.raw", "-c", "/tmp/e.json", "windows.pslist"]
    ).startswith("BLOCKED")


def test_vol_valid_call_passes_validation(monkeypatch, tmp_path):
    """Valid call dapat pumasa sa _validate (hindi tumatakbo ang vol)."""
    from sentinel import safe_exec

    monkeypatch.setattr(safe_exec, "ALLOWED_ROOTS", (tmp_path.resolve(),))
    img = tmp_path / "x.raw"
    assert (
        safe_exec._validate(["vol", "-f", str(img), "windows.pslist", "--pid", "4"])
        is None
    )
