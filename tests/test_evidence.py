import hashlib
from pathlib import Path

import pytest

from sentinel.evidence import evidence_metadata, sha256_file


def test_sha256_file_matches_expected(tmp_path: Path) -> None:
    sample = tmp_path / "sample.bin"
    sample.write_bytes(b"sentinel-test-data")
    expected = hashlib.sha256(b"sentinel-test-data").hexdigest()
    assert sha256_file(sample) == expected


def test_sha256_file_missing_raises() -> None:
    with pytest.raises(FileNotFoundError):
        sha256_file("/tmp/definitely-missing-file.img")


def test_evidence_metadata_contains_expected_fields(tmp_path: Path) -> None:
    sample = tmp_path / "evidence.img"
    sample.write_bytes(b"abc123")
    meta = evidence_metadata(sample)

    assert meta["name"] == "evidence.img"
    assert meta["size"] == 6
    assert meta["path"].endswith("evidence.img")
