import hashlib
import logging

import pytest

from sentinel import custody


@pytest.mark.parametrize("bad", ["", "../x", "a/b", "..", ".hidden", "x" * 80, "a b"])
def test_bad_case_names(bad):
    with pytest.raises(ValueError):
        custody.safe_case_name(bad)


def test_good_case_name():
    assert custody.safe_case_name("CASE-001") == "CASE-001"


def test_finalize_writes_matching_sums(tmp_path):
    case_dir = custody.prepare_case("CASE-T", root=tmp_path)
    logging.getLogger("SENTINEL").info("hello audit")
    report_path = custody.finalize(case_dir, {"ok": True})
    sums = (case_dir / "SHA256SUMS").read_text().splitlines()
    assert len(sums) == 2
    for line in sums:
        digest, name = line.split("  ")
        assert hashlib.sha256((case_dir / name).read_bytes()).hexdigest() == digest
    assert report_path.exists()


def test_sha256_file(tmp_path):
    f = tmp_path / "a.bin"
    f.write_bytes(b"abc")
    assert custody.sha256_file(f) == hashlib.sha256(b"abc").hexdigest()
