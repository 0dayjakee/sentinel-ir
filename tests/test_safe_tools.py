import shutil

import pytest

from sentinel import safe_exec
from sentinel.safe_exec import safe_run
from sentinel.safe_tools import grep_tree, strings_grep

needs_bins = pytest.mark.skipif(
    shutil.which("strings") is None or shutil.which("grep") is None,
    reason="binutils/grep not installed",
)


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(safe_exec, "ALLOWED_ROOTS", (tmp_path.resolve(),))
    return tmp_path


def test_outside_roots_blocked():
    assert strings_grep("/etc/passwd", "root").startswith("BLOCKED")
    assert strings_grep("/cases/../etc/passwd").startswith("BLOCKED")
    assert grep_tree("root", "/etc").startswith("BLOCKED")


def test_nul_byte_blocked():
    assert safe_run(["strings", "/cases/\x00x"]).startswith("BLOCKED")
    assert strings_grep("/cases/\x00x").startswith("BLOCKED")


@needs_bins
def test_strings_grep_filters(root):
    f = root / "a.bin"
    f.write_bytes(b"\x00\x01needle in haystack\x00\x02other junk text\x00")
    out = strings_grep(str(f), "NEEDLE")
    assert "needle in haystack" in out
    assert "other junk" not in out


@needs_bins
def test_grep_tree_finds(root):
    (root / "n.txt").write_text("Needle here\n")
    assert "Needle here" in grep_tree("needle", str(root))


@needs_bins
def test_pattern_cannot_escape_to_shell(root):
    f = root / "a.bin"
    f.write_bytes(b"hello world data\x00")
    marker = root / "pwned"
    strings_grep(str(f), f'x"; touch {marker}; echo "')
    grep_tree(f"x; touch {marker}", str(root))
    assert not marker.exists()
